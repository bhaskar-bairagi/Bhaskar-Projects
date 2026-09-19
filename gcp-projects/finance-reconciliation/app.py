from pathlib import Path

import streamlit as st

from engine import reconcile, to_csv

SAMPLES = Path(__file__).parent / "samples"
st.set_page_config(page_title="Finance reconciliation lab", page_icon="💳")
st.title("Finance reconciliation lab")
st.caption("Synthetic data · local execution · GCP mapping in README")
ledger_file = st.file_uploader("Ledger CSV", type="csv")
settlement_file = st.file_uploader("Settlement CSV", type="csv")
if st.button("Run reconciliation"):
    try:
        ledger = ledger_file.getvalue().decode("utf-8-sig") if ledger_file else (SAMPLES / "ledger.csv").read_text()
        settlement = settlement_file.getvalue().decode("utf-8-sig") if settlement_file else (SAMPLES / "settlement.csv").read_text()
        rows = reconcile(ledger, settlement)
        st.metric("Matched", sum(row["status"] == "matched" for row in rows))
        st.metric("Exceptions", sum(row["status"] != "matched" for row in rows))
        st.dataframe(rows, hide_index=True)
        st.download_button("Download results CSV", to_csv(rows), "reconciliation.csv", "text/csv")
    except (ValueError, UnicodeError) as exc:
        st.error(str(exc))
