import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="ChemPilot Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: white; }
    .report-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE STABLE ENGINE ---
def run_stable_engine(phase_idx, inputs):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # We'll use 'gemini-1.5-flash-latest' for maximum compatibility
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Act as a Chemical Project Auditor. Phase {phase_idx+1} for {inputs['chem']} at {inputs['cap']} TPA.
        Location: {inputs['loc']}. Budget: ₹{inputs['bud']} Cr.
        Provide a technical audit including Equipment Sizing, BOQ, and Utility Load.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ENGINE_ERROR: {str(e)}"

# --- 3. SESSION STATE ---
if 'project' not in st.session_state:
    st.session_state.project = {
        "step": 0,
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "reports": {},
        "id": f"CP-{uuid.uuid4().hex[:6].upper()}"
    }

# --- 4. DASHBOARD ---
st.title("🚢 ChemPilot v1 Intelligence")
st.sidebar.markdown(f"**Audit ID:** `{st.session_state.project['id']}`")
st.progress((st.session_state.project['step'] + 1) / 8)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: chem = st.text_input("Chemical", value=st.session_state.project['inputs']['chem'])
    with c2: cap = st.number_input("Scale (TPA)", value=st.session_state.project['inputs']['cap'])
    with c3: loc = st.text_input("Location", value=st.session_state.project['inputs']['loc'])
    with c4: bud = st.number_input("Budget (₹ Cr)", value=st.session_state.project['inputs']['bud'])
    
    if st.button("🚀 EXECUTE PHASE AUDIT", use_container_width=True):
        st.session_state.project['inputs'] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
        with st.spinner("Connecting to 2026 Engine Stack..."):
            result = run_stable_engine(st.session_state.project['step'], st.session_state.project['inputs'])
            st.session_state.project['reports'][st.session_state.project['step']] = result

# --- 5. OUTPUT ---
if st.session_state.project['step'] in st.session_state.project['reports']:
    st.divider()
    st.markdown(st.session_state.project['reports'][st.session_state.project['step']])
    
    if st.button(f"Accept & Advance to Phase {st.session_state.project['step']+2}"):
        st.session_state.project['step'] += 1
        st.rerun()
