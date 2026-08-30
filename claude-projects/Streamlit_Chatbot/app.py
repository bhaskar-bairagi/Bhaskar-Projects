import base64
import mimetypes
from datetime import date

import anthropic
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Setup: load API key from .env and configure the Streamlit page
# ---------------------------------------------------------------------------
load_dotenv()

st.set_page_config(page_title="Simple Chatbot", page_icon="💬", layout="centered")
st.title("💬 Claude Chatbot")

client = Anthropic()  # Reads ANTHROPIC_API_KEY from the environment automatically

# Friendly labels shown in the UI, mapped to actual API model IDs
MODEL_OPTIONS = {
    "Claude Sonnet 5 (balanced)": "claude-sonnet-5",
    "Claude Opus 5 (most capable)": "claude-opus-5",
    "Claude Haiku 4.5 (fastest)": "claude-haiku-4-5-20251001",
}


# ---------------------------------------------------------------------------
# Helper: extract plain text from a message's content as a plain string, 
# OR a list of content blocks (text/image/document) as attachment
# ---------------------------------------------------------------------------
def extract_text(content):
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        if block.get("type") == "text":
            parts.append(block["text"])
        elif block.get("type") == "image":
            parts.append("[attached image]")
        elif block.get("type") == "document":
            parts.append("[attached document]")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Helper: combine typed text or an attached file into supporting content format.
# PDFs become "document" blocks, everything else (png/jpg/webp) becomes an "image" block.
# ---------------------------------------------------------------------------
def build_user_content(text, file):
    if file is None:
        return text  # No attachment — just send plain text as before

    file_bytes = file.getvalue()
    b64_data = base64.b64encode(file_bytes).decode("utf-8")
    media_type = file.type or mimetypes.guess_type(file.name)[0]

    if media_type == "application/pdf":
        file_block = {
            "type": "document",
            "source": {"type": "base64", "media_type": media_type, "data": b64_data},
        }
    else:
        file_block = {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": b64_data},
        }

    # Claude expects a LIST of content blocks when mixing text + a file
    return [file_block, {"type": "text", "text": text}]


# ---------------------------------------------------------------------------
# Helpers: append a turn to the running conversation history as context
# ---------------------------------------------------------------------------
def add_user_message(messages, content):
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


# ---------------------------------------------------------------------------
# Core API call: streams Claude's response token-by-token instead of
# waiting for the full answer, and enables real-time web search.
# ---------------------------------------------------------------------------
def stream_chat(messages, model):
    today_str = date.today().strftime("%A, %B %d, %Y")

    # Give Claude today's real date, and tell it when to use web search
    system = (
        f"Today's date is {today_str}. Use the web_search tool whenever a "
        f"question needs current, real-time, or recent information you "
        f"wouldn't otherwise know."
    )

    with client.messages.stream(
        model=model,
        max_tokens=1500,
        system=system,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],  # Anthropic-hosted search tool
        messages=messages,
    ) as stream:
        # stream.text_stream yields ONLY text chunks, automatically skipping
        # over any tool-call / search-result blocks in between
        for text in stream.text_stream:
            yield text

        # After streaming finishes, save the full response object to pull 
        # citation URLs out of it afterward 
        st.session_state.last_final_message = stream.get_final_message()


# ---------------------------------------------------------------------------
# Helper: show source links under an answer, if web search was used
# ---------------------------------------------------------------------------
def render_citations(final_message):
    if final_message is None:
        return

    sources = {}
    for block in final_message.content:
        if getattr(block, "type", None) == "text" and getattr(block, "citations", None):
            for c in block.citations:
                url = getattr(c, "url", None)
                title = getattr(c, "title", url)
                if url:
                    sources[url] = title  # dict dedupes repeated URLs automatically

    if sources:
        with st.expander(f"📎 Sources ({len(sources)})"):
            for url, title in sources.items():
                st.markdown(f"- [{title}]({url})")


# ---------------------------------------------------------------------------
# Sidebar UI: model selector, file upload, and chat export
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()))
    model = MODEL_OPTIONS[model_label]

    st.divider()
    st.header("Attach a file (optional)")
    uploaded_file = st.file_uploader(
        "PDF or image", type=["pdf", "png", "jpg", "jpeg", "webp"]
    )

    st.divider()
    # Only show the export button once there's actually something to export
    if "messages" in st.session_state and st.session_state.messages:
        export_lines = ["# Chat Export\n"]
        for msg in st.session_state.messages:
            role = "**You**" if msg["role"] == "user" else "**Claude**"
            export_lines.append(f"{role}: {extract_text(msg['content'])}\n")
        st.download_button(
            "⬇️ Export chat as Markdown",
            data="\n".join(export_lines),
            file_name="chat_export.md",
            mime="text/markdown",
        )


# ---------------------------------------------------------------------------
# Session state: keeps conversation history alive across Streamlit reruns
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_final_message" not in st.session_state:
    st.session_state.last_final_message = None

# Re-render the full conversation history on every rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(extract_text(msg["content"]))

# Chat input box pinned to the bottom of the page
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Combine typed text with any uploaded file into one content payload
    content = build_user_content(user_input, uploaded_file)

    # Show the user's own message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.caption(f"📎 Attached: {uploaded_file.name}")

    add_user_message(st.session_state.messages, content)

    # Get Claude's (streamed) response, with error handling for common
    # API failure modes so the app degrades gracefully instead of crashing
    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(stream_chat(st.session_state.messages, model))
            render_citations(st.session_state.last_final_message)
        except anthropic.RateLimitError:
            st.error("Rate limit hit — please wait a moment and try again.")
            answer = None
        except anthropic.APIConnectionError:
            st.error("Couldn't connect to the Claude API — check your internet connection.")
            answer = None
        except anthropic.APIStatusError as e:
            st.error(f"API error ({e.status_code}): {e.message}")
            answer = None
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            answer = None

    # Only save the assistant's turn to history if the call actually succeeded
    if answer:
        add_assistant_message(st.session_state.messages, answer)