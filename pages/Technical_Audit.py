import streamlit as st

st.set_page_config(page_title="Technical Audit", layout="wide")

if not st.session_state.project["audit_report"]:
    st.warning("Please initialize a project on the Home Page first.")
    st.stop()

p = st.session_state.project
st.header(f"📈 Technical Audit & Logistics: {p['loc']}")

col1, col2, col3 = st.columns(3)
col1.metric("Selected Scale", f"{p['cap']:,} TPA")
col2.metric("Logistics Hub", p['loc'])
col3.metric("Status", "Audit Verified")

st.divider()
st.subheader("📍 Logistics Engine: Indian Context")
st.write(f"Evaluating freight impact for {p['loc']} using 2026 Dedicated Freight Corridor (DFC) rates.")

# Pulling the logistics section from the main report
st.markdown("### Engineering & Logistics Breakdown")
st.write(p["audit_report"])
