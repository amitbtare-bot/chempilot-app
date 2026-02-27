import streamlit as st
import google.generativeai as genai
from streamlit_searchbox import st_searchbox
import time

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="ChemPilot Pro", layout="wide", page_icon="🧪")

# UI: Glassmorphism & Background
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

# --- 2. PREDICTIVE SEARCH LOGIC ---
def chemical_suggestions(searchterm: str):
    # This list can be expanded or linked to a database
    base_data = ["Ethanol (64-17-5)", "Acetic Acid (64-19-7)", "Methanol (67-56-1)", "Ammonia (7664-41-7)", "Benzene (71-43-2)"]
    if not searchterm:
        return base_data
    return [c for c in base_data if searchterm.lower() in c.lower()]

# --- 3. SESSION STATE ---
if 'project' not in st.session_state:
    st.session_state.project = {"chem": "", "cap": 100000, "loc": "", "report": None}

# --- 4. MAIN INTERFACE ---
st.title("🚢 ChemPilot: Universal TEL Engine")

with st.sidebar:
    st.header("Project Parameters")
    
    # Predictive Searchbox (Plain text style)
    selected_chem = st_searchbox(
        chemical_suggestions,
        placeholder="Type chemical or CAS...",
        label="Chemical Search",
        key="chem_search"
    )
    
    user_cap = st.number_input("Annual Capacity (TPA)", min_value=1000, value=100000)
    exact_loc = st.text_input("Plant Location", placeholder="e.g. Dahej, Gujarat")
    
    run_btn = st.button("Generate Investment Audit", type="primary")

# --- 5. ENGINE EXECUTION ---
if run_btn:
    if not selected_chem or not exact_loc:
        st.warning("Please provide both Chemical and Location.")
    else:
        with st.status("🏗️ Distilling Data...", expanded=True) as status:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                prompt = f"""
                Investment Audit 2026: {selected_chem} | {user_cap} TPA | {exact_loc}.
                Include: 1. Scale feasibility vs MES. 2. Logistics landing cost impact for {exact_loc}. 
                3. Financials (CAPEX/OPEX INR Cr, ROI, Payback). 4. India Market Survey.
                5. Safety (NFPA 704).
                """
                
                response = model.generate_content(prompt)
                st.session_state.project.update({
                    "chem": selected_chem, "cap": user_cap, "loc": exact_loc, "report": response.text
                })
                status.update(label="Audit Complete!", state="complete")
            except Exception as e:
                st.error(f"Quota/Engine Error: {str(e)}")

# --- 6. DISPLAY RESULTS ---
if st.session_state.project["report"]:
    st.header(f"Executive Summary: {st.session_state.project['chem']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Selected Capacity", f"{st.session_state.project['cap']:,} TPA")
    col2.metric("Target Hub", st.session_state.project['loc'])
    col3.metric("Feasibility", "Analysis Ready")
    
    st.divider()
    st.markdown(st.session_state.project["report"])
