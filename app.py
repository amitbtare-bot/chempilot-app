import streamlit as st
import google.generativeai as genai
import time

# --- CACHED ENGINE FUNCTION ---
@st.cache_data(show_spinner=False)
def call_gemini_with_retry(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    max_retries = 3
    for i in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                time.sleep(10) # Wait 10 seconds and try again automatically
                continue
            else:
                raise e
    return "The system is currently busy due to high demand. Please wait 60 seconds."

# --- MAIN EXECUTION ---
if run_btn and chemical_query and exact_loc:
    # ... (Your loader code here)
    
    # Updated Prompt to be more "Token-Efficient"
    optimized_prompt = f"Direct technical audit for {chemical_query}, {user_cap} TPA at {exact_loc}. Data points: 2026 MES, logistics cost per tonne, CAPEX/OPEX (INR Cr), ROI%, Payback, Market Gap India, NFPA safety."
    
    try:
        report_text = call_gemini_with_retry(optimized_prompt)
        st.markdown(report_text)
    except Exception as e:
        st.error(f"Quota issue. Let's wait a minute and try again.")

# --- 1. SETUP & THEMES ---
st.set_page_config(page_title="ChemPilot TEL SaaS", layout="wide", page_icon="🧪")

# 2026 Knowledge Base for "Smart Suggestions" (Optional, doesn't limit search)
SUGGESTIONS = ["Ethanol (64-17-5)", "Acetic Acid (64-19-7)", "Methanol (67-56-1)", "Ammonia (7664-41-7)"]

# --- 2. CUSTOM UI: DYNAMIC BACKGROUND & SPINNER ---
def inject_ui_styles():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                 url("https://www.shutterstock.com/shutterstock/videos/1069542037/thumb/1.jpg");
                 background-size: cover; color: white; }
        @keyframes distill { 0% { height: 10%; } 50% { height: 90%; } 100% { height: 10%; } }
        .beaker-loader { width: 40px; height: 50px; border: 2px solid #00f2ff; border-radius: 0 0 15px 15px; position: relative; margin: auto; }
        .liquid { width: 100%; background: #00f2ff; position: absolute; bottom: 0; animation: distill 2s infinite; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. THE ENGINE ---
inject_ui_styles()
st.title("🚢 ChemPilot: Universal TEL Engine")

with st.sidebar:
    st.header("Project Parameters")
    # OPEN SEARCH: User can type anything here.
    chemical_query = st.selectbox("Search or Type Chemical/CAS", options=SUGGESTIONS + ["Other (Type Below)"], index=None)
    if chemical_query == "Other (Type Below)":
        chemical_query = st.text_input("Enter Manual Name or CAS")
    
    user_cap = st.number_input("Annual Capacity (TPA)", min_value=1000, value=100000)
    exact_loc = st.text_input("Exact Plant Location", placeholder="e.g. Dahej, Gujarat")
    
    run_btn = st.button("Generate Comprehensive Audit", type="primary")

# --- 4. EXECUTION ---
if run_btn and chemical_query and exact_loc:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="beaker-loader"><div class="liquid"></div></div>', unsafe_allow_html=True)
        st.write("Distilling Market Data, Logistics, and Financials...")
        
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Act as a 2026 Industrial Investment Advisor. Analyze {chemical_query} at {user_cap} TPA in {exact_loc}.
        INCLUDE ALL FEATURES:
        1. VALIDATE CAS: Find the correct CAS and confirm if {user_cap} TPA meets the Indian Minimum Economic Scale (MES).
        2. LOGISTICS: Calculate Landing Cost impact using distance to nearest Indian port/rail-head. 
        3. FINANCIALS: Est CAPEX/OPEX (INR Cr), Payback, and ROI.
        4. MARKET: 2026 Demand-Supply gap in India and key competitors.
        5. SAFETY: NFPA 704 & GHS data.
        """
        response = model.generate_content(prompt)
        placeholder.empty()
        
        # Displaying Results in a Professional Dashboard
        st.header(f"Investment Audit Report: {chemical_query}")
        st.markdown(response.text)
        
    except Exception as e:
        placeholder.empty()
        st.error(f"Engine Error: {str(e)}")

