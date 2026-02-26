import streamlit as st
import google.generativeai as genai

# 1. SETUP - Replace with your actual API Key
genai.configure(api_key="AIzaSyDRDdCDv13ydkIWQZHOo2pFAboJTRqK38g")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ChemPilot SaaS", layout="centered")
st.title("🚢 ChemPilot: Engineering Intelligence")
st.subheader("Institutional-Grade Chemical Project Reports")

# Initialize "Memory" for the steps
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- STEP 1: INPUT ---
if st.session_state.step == 1:
    with st.form("input_form"):
        chemical = st.text_input("Chemical Name", placeholder="e.g., Acetic Acid")
        capacity = st.number_input("Annual Capacity (TPA)", min_value=1000, value=100000)
        submitted = st.form_submit_button("Generate Engineering Math")
        
        if submitted:
            with st.spinner("Gemini is researching and calculating..."):
                # Hidden background prompt
                prompt = f"Research {chemical} production. Use Python to calculate Material Balance and Utilities for {capacity} TPA. Output only a summary table."
                response = model.generate_content(prompt)
                st.session_state.math_result = response.text
                st.session_state.step = 2
                st.rerun()

# --- STEP 2: APPROVAL ---
elif st.session_state.step == 2:
    st.write("### 📊 Engineering Evidence Review")
    st.info("Please review the deterministic math below before we generate the full narrative.")
    st.write(st.session_state.math_result)
    
    col1, col2 = st.columns(2)
    if col1.button("✅ Approve & Write Full DPR"):
        st.session_state.step = 3
        st.rerun()
    if col2.button("❌ Modify Inputs"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: FINAL OUTPUT ---
elif st.session_state.step == 3:
    st.success("Math Approved. Generating Institutional-Grade Narrative...")
    st.write("This is where your full report will appear. In the SaaS version, this would be a PDF download.")
    if st.button("Start New Project"):
        st.session_state.step = 1

        st.rerun()
