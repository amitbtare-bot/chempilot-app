import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETTINGS & GLASSMORPHISM UI ---
st.set_page_config(page_title="ChemPilot Pro", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
        url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        background-size: cover; color: #f0f2f6;
    }
    /* Glassmorphism Effect for Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px; padding: 15px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; font-weight: bold;
        background: linear-gradient(45deg, #00f2ff, #0066ff);
        color: white; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00f2ff; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA & SESSION STATE ---
if 'project' not in st.session_state:
    st.session_state.project = {"chem": None, "cap": 100000, "loc": "", "report": None}

SUGGESTIONS = ["Ethanol (64-17-5)", "Acetic Acid (64-19-7)", "Methanol (67-56-1)", "Ammonia (7664-41-7)"]

# --- 3. QUOTA-SAFE ENGINE ---
@st.cache_data(show_spinner=False)
def run_investment_audit(chemical, capacity, location):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Act as a 2026 Chemical Investment Advisor for India.
        Analyze: {chemical} | {capacity} TPA | {location}.
        1. FEASIBILITY: Is this scale viable vs Indian MES?
        2. LOGISTICS: Calculate landing cost impact for {location} vs ports (Mundra/JNPT).
        3. FINANCIALS: Est CAPEX/OPEX (INR Cr), ROI, and Payback.
        4. MARKET: 2026 India demand-supply gap and competitors.
        5. SAFETY: NFPA 704 & GHS data.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e): return "QUOTA_ERROR"
        return f"Error: {str(e)}"

# --- 4. MAIN INTERFACE ---
st.title("🚢 ChemPilot: Universal TEL Engine")

with st.sidebar:
    st.header("Project Setup")
    
    # PREDICTIVE SEARCHBOX (Native 2026 Streamlit)
    selected_chem = st.selectbox(
        "Search or Type Chemical/CAS",
        options=SUGGESTIONS,
        index=None,
        placeholder="Start typing (e.g. Eth...)",
        accept_new_options=True  # Allows manual typing with predictive text
    )
    
    user_cap = st.number_input("Annual Capacity (TPA)", min_value=1000, value=100000)
    exact_loc = st.text_input("Plant Location", placeholder="e.g. Dahej, Gujarat")
    
    run_btn = st.button("Generate TEL Audit")

# --- 5. EXECUTION & RESULTS ---
if run_btn:
    if not selected_chem or not exact_loc:
        st.warning("Please provide both Chemical and Location.")
    else:
        with st.status("🏗️ Distilling Data...", expanded=True) as status:
            result = run_investment_audit(selected_chem, user_cap, exact_loc)
            
            if result == "QUOTA_ERROR":
                status.update(label="❌ Quota Hit", state="error")
                st.error("Engine busy. Please wait 60 seconds and retry.")
            else:
                st.session_state.project.update({
                    "chem": selected_chem, "cap": user_cap, "loc": exact_loc, "report": result
                })
                status.update(label="✅ Audit Complete", state="complete")

if st.session_state.project["report"]:
    st.header(f"Executive Audit: {st.session_state.project['chem']}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Target Capacity", f"{st.session_state.project['cap']:,} TPA")
    c2.metric("Logistics Hub", st.session_state.project['loc'])
    c3.metric("Feasibility", "Analysis Ready")
    
    st.divider()
    st.markdown(st.session_state.project["report"])
