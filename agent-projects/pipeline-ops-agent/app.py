import streamlit as st

from runner import load_plugins, run_tool

st.set_page_config(page_title="Pipeline operations workbench", page_icon="🛠️")
st.title("Pipeline operations workbench")
st.caption("Synthetic pipeline runs · explicit tools · read-only")
plugins = load_plugins()
name = st.selectbox("Tool", list(plugins), format_func=lambda key: plugins[key][0]["description"])
run_id = st.selectbox("Sample run", ["R-001", "R-002", "R-003"])
if st.button("Run tool"):
    try:
        trace = run_tool(name, {"run_id": run_id})
        st.json(trace)
    except ValueError as error:
        st.error(str(error))
st.markdown("Choose **R-002** and run both tools to compare a failed run with its quality checks. This workbench never modifies a pipeline.")
