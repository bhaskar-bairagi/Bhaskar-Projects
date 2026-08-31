from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from invoice_helper import extract_invoice, invoice_to_row


PROJECT_DIR = Path(__file__).parent

st.set_page_config(page_title="Easy AI Invoice Organizer", page_icon="🧾", layout="wide")
st.title("🧾 Easy AI Invoice Organizer")
st.write("Read invoice PDFs, see the important fields, and download a simple CSV report.")

with st.sidebar:
    st.header("Optional AI settings")
    api_key = st.text_input(
        "OpenAI API key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Not required for the free demo.",
    )
    model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-5.6"))
    st.caption("For low-cost testing, upload one invoice at a time.")

demo_tab, ai_tab = st.tabs(["Free demo", "Try your invoices"])

with demo_tab:
    st.subheader("No API key required")
    st.write("These results come from the four sample invoices included with the project.")
    if st.button("Load free demo results", type="primary"):
        st.session_state["results"] = pd.read_csv(PROJECT_DIR / "demo_results.csv")

with ai_tab:
    uploaded_files = st.file_uploader(
        "Upload PDF invoices", type=["pdf"], accept_multiple_files=True
    )
    if st.button("Extract invoice details"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        elif not api_key:
            st.warning("Enter an API key in the sidebar, or use the free demo tab.")
        else:
            rows = []
            progress = st.progress(0)
            for number, uploaded in enumerate(uploaded_files, start=1):
                try:
                    invoice = extract_invoice(uploaded.getvalue(), uploaded.name, api_key, model)
                    rows.append(invoice_to_row(invoice, uploaded.name))
                except Exception as error:
                    st.error(f"Could not process {uploaded.name}: {error}")
                progress.progress(number / len(uploaded_files))
            if rows:
                st.session_state["results"] = pd.DataFrame(rows)

results = st.session_state.get("results")
if results is not None:
    st.divider()
    st.subheader("Invoice results")
    st.dataframe(results, use_container_width=True, hide_index=True)
    st.download_button(
        "Download CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="organized_invoices.csv",
        mime="text/csv",
    )
    st.info("Your original PDF files are not renamed, moved, or deleted.")

