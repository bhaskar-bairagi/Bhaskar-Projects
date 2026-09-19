import streamlit as st

from planner import Application, assess

st.set_page_config(page_title="Azure to GCP migration lab", page_icon="🧭")
st.title("Azure → GCP migration decision lab")
st.caption("Educational decision exercise; no cloud credentials or resources required")
name = st.text_input("Application name", "Synthetic order service")
os_name = st.selectbox("Guest OS", ["Linux", "Windows"])
stateful = st.checkbox("Stores state on its VM", value=False)
container = st.checkbox("Has a repeatable container build", value=True)
dependencies = st.number_input("Connected systems", min_value=0, value=2)
data_gb = st.number_input("Approximate data volume (GB)", min_value=0, value=10)
regulated = st.checkbox("Regulated data", value=False)
if st.button("Assess migration"):
    try:
        result = assess(Application(name, "Azure VM", os_name, stateful, container,
                                    dependencies, data_gb, regulated))
        st.subheader(f"{result['wave']}: {result['route']}")
        for reason in result["reasons"]:
            st.write(f"• {reason}")
        st.subheader("Validation and rollback checklist")
        for i, step in enumerate(result["checklist"], 1):
            st.write(f"{i}. {step}")
        st.download_button("Download assessment JSON", __import__("json").dumps(result, indent=2),
                           "migration-assessment.json", "application/json")
    except ValueError as error:
        st.error(str(error))
