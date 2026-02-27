import streamlit as st
import google.generativeai as genai
import uuid
import pandas as pd

# --- 1. INITIALIZE GLOBAL STATE (Governance Spine) ---
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        "current_phase": 1,
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "audit_trail": [],
        "report_id": None
    }

# --- 2. THE ENGINE STACK (Functional Logic) ---
def run_technical_engine(phase, inputs):
    """Executes frozen v1 engine logic based on the active phase."""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Context-aware prompting based on v1 engine requirements
    prompts = {
        1: f"Market & Technical Feasibility for {inputs['chem']} at {inputs['cap']} TPA. Verify MES.",
        2: f"Stoichiometric & Energy Balance for {inputs['chem']}. Identify scale-up risks.",
        3: f"Conceptual Equipment Sizing & BOQ for {inputs['chem']} in {inputs['loc']}.",
        4: f"FEED: Detailed Utility sizing (Steam/Power) and Logistics Network Optimization."
    }
    
    try:
        response = model.generate_content(prompts.get(phase, "General Audit"))
        return response.text
    except Exception as e:
        return f"Engine Error: {str(e)}"

# --- 3. UI: THE PROJECT COMMAND CENTER ---
st.set_page_config(page_title="ChemPilot v1 | Technical Governance", layout="wide")

st.title("🚢 ChemPilot Pro")
st.caption("Intelligence • Validation • Governance")

# The Milestone Tracker (Functional)
cols = st.columns(8)
for i in range(1, 9):
    label = "✅" if i < st.session_state.project_data["current_phase"] else "🔵" if i == st.session_state.project_data["current_phase"] else "⚪"
    cols[i-1].markdown(f"**P{i}**\n{label}")

st.divider()

# --- 4. PHASE-GATE INPUTS ---
curr_phase = st.session_state.project_data["current_phase"]

if curr_phase <= 2:
    st.subheader("Phase 1-2: Conception & R&D Intelligence (Free)")
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        chem = c1.text_input("Chemical/CAS", value=st.session_state.project_data["inputs"]["chem"])
        cap = c2.number_input("Scale (TPA)", value=st.session_state.project_data["inputs"]["cap"])
        loc = c3.text_input("Location", value=st.session_state.project_data["inputs"]["loc"])
        bud = c4.number_input("Budget (₹ Cr)", value=st.session_state.project_data["inputs"]["bud"])

    if st.button("🚀 EXECUTE PHASE INTELLIGENCE"):
        # Save Inputs
        st.session_state.project_data["inputs"] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
        
        with st.status("Engaging v1 Engine Stack...", expanded=True) as status:
            report = run_technical_engine(curr_phase, st.session_state.project_data["inputs"])
            st.session_state.project_data["last_report"] = report
            st.session_state.project_data["report_id"] = f"CP-{uuid.uuid4().hex[:6].upper()}"
            status.update(label="Intelligence Validated", state="complete")
        
        st.rerun()

# --- 5. THE GOVERNANCE OUTPUT ---
if "last_report" in st.session_state.project_data:
    st.markdown(f"### 📄 Report {st.session_state.project_data['report_id']}")
    st.markdown(st.session_state.project_data["last_report"])
    
    # Technical Decision: Scale Up/Down?
    if st.button("Accept Technical Findings & Move to Phase 3 (₹25,000)"):
        st.session_state.project_data["current_phase"] = 3
        st.rerun()
