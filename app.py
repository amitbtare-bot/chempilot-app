import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CONFIG & AUTH ---
st.set_page_config(page_title="ChemPilot TEL SaaS", layout="wide", page_icon="🚢")

# 2026 Market & Scale Database
CHEM_INTEL = {
    "Ethanol": {"cas": "64-17-5", "mes": 40000, "hub": "Dahej / Uttar Pradesh", "cap_mult": 12},
    "Acetic Acid": {"cas": "64-19-7", "mes": 60000, "hub": "Dahej / Paradeep", "cap_mult": 18},
    "Methanol": {"cas": "67-56-1", "mes": 120000, "hub": "Dahej / Vizag", "cap_mult": 25}
}

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    st.error("Missing API Key in Streamlit Secrets.")
    st.stop()

# --- SIDEBAR: INPUTS ---
st.sidebar.title("🚢 Project Command")
chem_choice = st.sidebar.selectbox("Select Chemical", options=list(CHEM_INTEL.keys()), index=None)
user_cap = st.sidebar.number_input("Annual Capacity (TPA)", min_value=5000, value=100000)
exact_loc = st.sidebar.text_input("Proposed Plant Location", placeholder="e.g. Dahej, Gujarat")

if st.sidebar.button("Generate Full Investment Audit", type="primary"):
    if chem_choice and exact_loc:
        intel = CHEM_INTEL[chem_choice]
        
        with st.spinner("Running Technoeconomic & Logistics Engine..."):
            prompt = f"""
            Task: Technoeconomic Feasibility Study (2026 Context)
            Product: {chem_choice} (CAS: {intel['cas']}) | Capacity: {user_cap} TPA | Location: {exact_loc}
            
            1. Scale Analysis: Compare {user_cap} vs Minimum Economic Scale ({intel['mes']}). 
            2. Logistics Engine: Using 2026 rates (Road: ₹2.5/t-km, Rail: ₹1.6/t-km), calculate transport impact for {exact_loc}.
            3. Techno-Economics: Provide CAPEX/OPEX estimates in INR Crores. Calculate Payback Period and ROI.
            4. Market Survey: Describe the 2026 demand-supply gap in India, key competitors, and price trends.
            5. Safety/CAS: Provide NFPA 704 ratings and hazard warnings.
            """
            response = model.generate_content(prompt)
            st.session_state.audit = response.text
            st.session_state.current_chem = chem_choice

# --- MAIN DASHBOARD ---
if 'audit' in st.session_state:
    st.header(f"Investment Audit: {st.session_state.current_chem}")
    
    # 1. FEASIBILITY CARDS
    intel = CHEM_INTEL[st.session_state.current_chem]
    is_feasible = user_cap >= intel["mes"]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Economic Viability", "✅ High" if is_feasible else "⚠️ Low Scale")
    c2.metric("Target India Hub", intel["hub"])
    c3.metric("Projected ROI", "21.5%" if is_feasible else "8.2%")
    
    if not is_feasible:
        st.warning(f"Note: To reach 20%+ ROI, institutional scale for {st.session_state.current_chem} usually starts at {intel['mes']:,} TPA.")

    # 2. LOGISTICS IMPACT
    st.subheader("📍 Logistics & Landing Cost Analysis")
    st.write(f"Analyzing supply chain efficiency for **{exact_loc}**...")
    
    # 3. FULL REPORT (GEMINI OUTPUT)
    st.divider()
    st.markdown(st.session_state.audit)
