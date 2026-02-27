import streamlit as st
import google.generativeai as genai
import time
import streamlit as st
from streamlit_searchbox import st_searchbox

# --- 1. SEARCH LOGIC (Predictive Typing) ---
def chemical_lookup(searchterm: str):
    # This function filters your database as the user types
    # In 2026, you can even connect this to a live chemical API
    base_options = ["Ethanol (64-17-5)", "Acetic Acid (64-19-7)", "Methanol (67-56-1)"]
    if not searchterm:
        return base_options
    
    # Simple fuzzy match: return options that contain the typed letters
    return [opt for opt in base_options if searchterm.lower() in opt.lower()]

# --- 2. THE UI ---
st.title("🚢 ChemPilot Universal Search")

# Plain text box with predictive suggestions
selected_value = st_searchbox(
    chemical_lookup,
    key="chemical_search",
    placeholder="Start typing chemical or CAS...",
    label="Chemical / CAS Number"
)

# Handle the output
if selected_value:
    st.success(f"Targeting: {selected_value}")
else:
    # UX fallback: if nothing is selected from suggestions, use manual input
    manual_input = st.text_input("Manual Override (if not in suggestions)")

@st.cache_data(show_spinner=False)
def run_audit_safe(chem, cap, loc):
    model = genai.GenerativeModel('gemini-2.0-flash')
    # Exponential Backoff Logic
    for delay in [1, 5, 20, 60]: # Wait 1s, then 5s, then 20s...
        try:
            response = model.generate_content(f"Technical audit for {chem}...")
            return response.text
        except Exception as e:
            if "429" in str(e):
                st.warning(f"Engine is busy. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return f"Unexpected Error: {e}"
    return "The engine is currently overloaded. Please try again in a few minutes."

# --- GLOBAL CONFIG & UI ---
st.set_page_config(page_title="ChemPilot Pro", layout="wide", page_icon="🧪")

# UX/UI: Glassmorphism & Background
st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
             url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
             background-size: cover; color: #f0f2f6; }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px); border-radius: 15px; padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE DATA ---
if 'project' not in st.session_state:
    st.session_state.project = {"chem": [], "cap": 100000, "loc": "", "audit_report": None}

# --- SEARCH ENGINE ---
st.title("🚢 ChemPilot: Techno-Economic & Logistics Engine")

with st.sidebar:
    st.header("Project Initiation")
    chems = st.multiselect("Search Chemicals (Suggestive)", 
                          options=["Ethanol (64-17-5)", "Methanol (67-56-1)", "Acetic Acid (64-19-7)", "Ammonia (7664-41-7)"],
                          accept_new_options=True)
    cap = st.number_input("Annual Capacity (TPA)", value=100000)
    loc = st.text_input("Exact Location", placeholder="e.g. Dahej, Gujarat")
    
    if st.button("Generate Full Audit", type="primary"):
        if chems and loc:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # THE CONSOLIDATED PROMPT (Logistics, Scale, Financials, Market)
                prompt = f"""
                Analyze {', '.join(chems)} at {cap} TPA in {loc}, India (2026 Context).
                Include: 1. Scale feasibility (MES). 2. Logistics landing cost impact. 
                3. Financials (CAPEX/OPEX INR Cr, ROI, Payback). 4. 2026 India Market Survey.
                5. Safety (NFPA 704 & CAS). Provide data in Markdown tables.
                """
                response = model.generate_content(prompt)
                st.session_state.project.update({"chem": chems, "cap": cap, "loc": loc, "audit_report": response.text})
                st.success("Project Data Distilled!")
            except Exception as e:
                st.error(f"Engine Error: {str(e)}")
        else:
            st.warning("Please provide Chemical and Location.")

# --- LANDING DISPLAY ---
if st.session_state.project["audit_report"]:
    st.header(f"Executive Summary: {', '.join(st.session_state.project['chem'])}")
    st.markdown(st.session_state.project["audit_report"])
else:
    st.info("👈 Enter project parameters in the sidebar to generate the Investment Audit.")


