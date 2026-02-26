import streamlit as st
import google.generativeai as genai

# SECURE SETUP
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 2026 UPDATE: Using Gemini 3.1 Flash for faster response
    model = genai.GenerativeModel('gemini-3.1-flash-preview')
except Exception:
    st.error("Check your API Key in Streamlit Secrets!")
    st.stop()

# SEARCH LOGIC
st.subheader("🚀 Project Initiation")
selected_option = st.selectbox(
    "Select Chemical",
    options=search_options,
    index=None,
    placeholder="Type 'Eth' or '64-17' to test..."
)

if selected_option:
    # This splits "Ethanol (64-17-5)" back into "Ethanol"
    chem_name = selected_option.split(" (")[0]
    cas_no = CHEM_DB[chem_name]
    st.success(f"Selected: {chem_name} | CAS: {cas_no}")
