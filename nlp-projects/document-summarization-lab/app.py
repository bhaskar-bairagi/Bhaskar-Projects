from pathlib import Path

import streamlit as st

from summarizer import evaluate, summarize

st.set_page_config(page_title="Document summarization lab", page_icon="📝")
st.title("Document summarization lab")
st.caption("Local extractive baselines; sample text is synthetic")
sample = (Path(__file__).parent / "sample_data" / "incident.txt").read_text(encoding="utf-8")
source = st.text_area("Source document", sample, height=190)
terms = st.text_input("Key terms to check (comma separated)", "five, duplicated, paused")
count = st.slider("Sentences in summary", 1, 5, 2)
if st.button("Compare summaries"):
    try:
        for method, title in [("lead", "Lead sentences"), ("frequency", "Word frequency")]:
            result = summarize(source, method, count)
            st.subheader(title)
            st.write(result)
            st.json(evaluate(source, result, terms.split(",")))
    except ValueError as error:
        st.error(str(error))
st.caption("Coverage depends on the manually entered terms. Source support only confirms copied sentences, not whether the summary is complete.")
