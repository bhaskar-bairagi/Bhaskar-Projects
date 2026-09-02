# Streamlit Chatbot — Claude API

A full-featured, web-based chatbot built on Streamlit and the Anthropic Claude API. Supports real-time streaming responses, live web search with citations, file/image analysis, multi-model selection, conversation export, and graceful error handling.

## Overview

This project evolved from a simple command-line, notebook-based chatbot into a polished web application. It demonstrates practical, hands-on use of the Claude API beyond basic request/response calls — including streaming, server-side tool use (web search), multimodal input, and production-style error handling.

## Features

| Feature | Description |
|---|---|
| 💬 **Streaming responses** | Answers appear token-by-token in real time instead of waiting for the full response |
| 🔍 **Live web search** | Claude automatically searches the web for current/real-time information when needed, using Anthropic's server-side web search tool |
| 📎 **Source citations** | When search is used, source links are displayed in a collapsible panel under the answer |
| 📄 **File & image upload** | Attach a PDF or image alongside a question; Claude analyzes it directly as part of the conversation |
| 🧠 **Model picker** | Switch between Claude Sonnet 5, Opus 5, and Haiku 4.5 per conversation, trading off speed vs. capability |
| ⬇️ **Chat export** | Download the full conversation as a Markdown file |
| 🛡️ **Error handling** | Rate limits, connection issues, and API errors are caught and shown as clean, user-facing messages instead of crashing the app |
| 🗓️ **Date awareness** | The current date is injected into the system prompt on every call, so Claude always knows "today" |

## Tech Stack

| Component | Purpose |
|---|---|
| Python 3.13 | Core language |
| Streamlit | Web UI framework |
| Anthropic SDK | Claude API client, including streaming and server-side tools |
| python-dotenv | Loads the API key from a shared `.env` file |

## Prerequisites

- Python 3.13+
- An Anthropic API key ([console.anthropic.com](https://console.anthropic.com/settings/keys))
- Streamlit (`pip install streamlit`)

## Setup

1. **Navigate to the project folder:**
   ```bash
   cd claude-projects/Streamlit_Chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit anthropic python-dotenv
   ```

3. **API key:** this project reads `ANTHROPIC_API_KEY` from a `.env` file at the repository root (`Bhaskar-Projects/.env`), shared across all projects in this repo — no project-local `.env` is required.

## Running the App

```bash
cd claude-projects/Streamlit_Chatbot
streamlit run app.py
```

This starts a local web server (typically `http://localhost:8501`) and opens the chat interface automatically in your browser.

## How to Use

1. **Pick a model** from the sidebar dropdown — Sonnet 5 (balanced), Opus 5 (most capable), or Haiku 4.5 (fastest).
2. **Optionally attach a file** — a PDF or image — via the sidebar uploader before asking your question about it.
3. **Type your question** in the chat box at the bottom and press Enter.
4. Responses stream in live. If Claude used web search to answer, a **📎 Sources** panel appears below the response with linked citations.
5. Once you've had a conversation, an **⬇️ Export chat as Markdown** button appears in the sidebar to download the full transcript.

## Architecture Notes

- **Streaming**: uses `client.messages.stream()` with `stream.text_stream`, which yields only text deltas — tool-use and search-result blocks are automatically excluded from the stream and handled separately.
- **Session persistence**: Streamlit re-runs the entire script on every user interaction. Conversation history is kept alive across these re-runs using `st.session_state`, not a plain Python variable (which would reset each time).
- **Multimodal input**: uploaded files are base64-encoded and sent as `document` (PDF) or `image` content blocks alongside the user's text, following Claude's multimodal message format.
- **Web search**: enabled via Anthropic's hosted `web_search_20250305` tool. The search itself runs on Anthropic's infrastructure — this app never performs scraping or calls a separate search API directly.
- **Citations**: extracted from the final assembled message (`stream.get_final_message()`) after streaming completes, since citation metadata isn't available on individual streamed text chunks.

## Project Structure

```
Streamlit_Chatbot/
├── app.py          # Main application
└── README.md       # This file
```

## Known Limitations

- Conversation history is held in memory only — refreshing the browser tab clears it (no persistence to disk/database yet).
- Only one conversation thread at a time; no sidebar history of past sessions.
- No authentication — not intended for public deployment as-is.

## Possible Future Enhancements

- Persist conversation history to disk (JSON/SQLite) so sessions survive restarts
- Multiple named conversation threads, switchable from a sidebar
- Token usage / cost tracking per session
- Password-gate or basic auth before deploying publicly (e.g. via Streamlit Community Cloud)
- Response regeneration / message editing

## License

Personal / educational project.
