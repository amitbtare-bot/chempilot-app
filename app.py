import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime
import time

# --- 1. CORE v1 CONFIGURATION (FROZEN) ---
PHASES = [
    "1. Conception & Feasibility",
    "2. Process Development (R&D)",
    "3. Conceptual Design",
    "4. FEED",
    "5. Detailed Engineering",
    "6. Procurement & Construction",
    "7. Commissioning & Startup",
    "8. Operation & Maintenance"
]

# --- 2. THE RESILIENT ENGINE (Functional Logic) ---
@st.cache_data(show_spinner=False)
def run_v1_engine(phase_idx, inputs):
    """Executes frozen v1 engine logic for the specific industry phase."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Using 1.5 Flash for stability and higher free-tier limits
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Phase-specific technical prompts
        context = [
            f"Phase 1: Market & Tech Feasibility for {inputs['chem']} at {inputs['cap']} TPA in {inputs['loc']}. Focus on MES, Logistics Risk, and Budget (₹{inputs['bud']} Cr).",
            f"Phase 2: Stoichiometric & Energy Balance for {inputs['chem']}. List side-reactions, scale-up risks, and utility loads.",
            f"Phase 3: Conceptual Design. Provide Equipment Sizing Table (MOC/Size), Process Flow summary, and Mechanical BOQ breakdown.",
            f"Phase 4: FEED (Front End Engineering Design). Detailed Utility Infrastructure (Steam/Power) and Logistics Network Optimization."
        ]
        
        prompt = context[phase_idx] if phase_idx < 4 else f"Governance & Intelligence for Phase: {PHASES[phase_idx]}"
        
        # Advisory Logic: 20% Portfolio Strategy
        prompt += "\n\nInclude a 'Strategic Pivot' section: How can a 20% budget top-up allow for a second product using similar equipment?"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "QUOTA_LIMIT: Engine busy. Please wait 60 seconds or link a billing account to your API key."
        return f"ENGINE_ERROR: {str(e)}"

# --- 3. SESSION STATE (The Memory Spine) ---
if 'project' not in st.session_state:
    st.session_state.project = {
        "step": 0,
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "reports": {},
        "report_id": f"CP-V1-{uuid.uuid4().hex[:6].upper()}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- 4. THE PROFESSIONAL UI ---
st.set_page_config(page_title="ChemPilot v1 | Production", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0d1117, #000000); color: white; }
    .hero-card { background: rgba(255, 255, 255, 0.03); border: 1px solid #00f2ff33; padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
    .report-area { background: #0d1117; border-left: 4px solid #00f2ff; padding: 25px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Identity & Governance
st.sidebar.title("🛡️ ChemPilot v1")
st.sidebar.markdown(f"**Audit ID:** `{st.session_state.project['report_id']}`")
st.sidebar.markdown(f"**Started:** {st.session_state.project['timestamp']}")
st.sidebar.divider()
st.sidebar.write(f"**Current Milestone:**\n{PHASES[st.session_state.project['step']]}")

# Milestone Progress
st.progress((st.session_state.project['step'] + 1) / 8)

# --- 5. THE COMMAND CENTER ---
st.header(f"🚢 Milestone {st.session_state.project['step'] + 1}: {PHASES[st.session_state.project['step']]}")

with st.container():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: chem = st.text_input("Chemical / CAS", value=st.session_state.project['inputs']['chem'], placeholder="e.g. Methanol")
    with c2: cap = st.number_input("Scale (TPA)", value=st.session_state.project['inputs']['cap'], step=1000)
    with c3: loc = st.text_input("Hub (Location)", value=st.session_state.project['inputs']['loc'], placeholder="e.g. Dahej, Gujarat")
    with c4: bud = st.number_input("Budget (₹ Cr)", value=st.session_state.project['inputs']['bud'], step=10)

    if st.button("🚀 EXECUTE PHASE AUDIT", use_container_width=True):
        if not chem or cap <= 0 or not loc:
            st.warning("Please provide Chemical, Scale, and Location to activate the Logistics & Technical engines.")
        else:
            st.session_state.project['inputs'] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
            with st.spinner("Processing through 2026 Engine Stack..."):
                result = run_v1_engine(st.session_state.project['step'], st.session_state.project['inputs'])
                st.session_state.project['reports'][st.session_state.project['step']] = result
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. THE INTELLIGENCE DASHBOARD ---
if st.session_state.project['step'] in st.session_state.project['reports']:
    st.markdown('<div class="report-area">', unsafe_allow_html=True)
    report_content = st.session_state.project['reports'][st.session_state.project['step']]
    
    if "QUOTA_LIMIT" in report_content:
        st.error(report_content)
    else:
        st.markdown(report_content)
        
        # Stage-Gate Move
        st.divider()
        if st.button(f"✅ Accept Audit & Move to {PHASES[st.session_state.project['step'] + 1]}"):
            if st.session_state.project['step'] < 7:
                st.session_state.project['step'] += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
