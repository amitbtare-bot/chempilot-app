import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Utilities", layout="wide")

if not st.session_state.project["audit_report"]:
    st.warning("Please initialize a project on the Home Page first.")
    st.stop()

st.header("⚙️ Utility & Resource Sizing")

if st.button("Calculate Utility Load"):
    with st.spinner("Calculating Steam, Power, and Water requirements..."):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"Calculate the hourly Utility Consumption (Steam in TPH, Power in MW, Water in m3/hr) for a {st.session_state.project['cap']} TPA {st.session_state.project['chem']} plant."
        response = model.generate_content(prompt)
        st.markdown(response.text)
