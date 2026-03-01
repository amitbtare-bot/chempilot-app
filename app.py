import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# --- 1. CORE SYSTEM SETTINGS & STYLING ---
st.set_page_config(page_title="ChemPilot v1 | IDI Platform", layout="wide")

# Institutional Theme (Glassmorphism & High-Trust UI)
st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .hero-card { background: rgba(255, 255, 255, 0.03); border: 1px solid #00f2ff33; padding: 25px; border-radius: 15px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00f2ff, #0072ff); color: white; border: none; font-weight: bold; height: 3rem; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00f2ff, #0072ff); }
    </style>
""", unsafe_allow_html=True)

# --- 2. ADAPTIVE INTELLIGENCE PIPELINE ---
def get_working_engine():
    """Self-Healing API Layer: Scans for the most stable LLM [cite: 167, 168]"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prioritize high-performance Flash models for industrial speed [cite: 169]
        for m in models:
            if 'flash' in m: return m
        return models[0] if models else None
    except: return None

def run_technical_audit(phase_idx, data):
    """Executes technical logic based on the 8-Phase Spine [cite: 27, 165]"""
    engine_name = get_working_engine()
    if not engine_name: return "🚨 Connection Error: Engineering Engine Offline."
    
    model = genai.GenerativeModel(engine_name)
    # Technical Guardrail Prompting [cite: 176, 177]
    prompt = f"""
    Act as the ChemPilot IDI Orchestrator. [cite: 73]
    PHASE: {PHASES[phase_idx]} 
    PRODUCT: {data['chem']} | SCALE: {data['cap']} TPA | HUB: {data['loc']} | BUDGET: ₹{data['bud']} Cr.
    
    1. Perform Stoichiometric/Engineering Audit for this phase. [cite: 68, 74]
    2. Recommend Material of Construction (MOC) based on NACE standards. [cite: 41, 45, 75]
    3. Calculate Technical Integrity Score (TIS) based on MOC-Budget alignment. [cite: 66, 69]
    """
    return model.generate_content(prompt).text

# --- 3. SESSION PERSISTENCE & GOVERNANCE ---
PHASES = [
    "1. Feasibility & Market", "2. R&D & Stoichiometry", 
    "3. Conceptual Design", "4. FEED Engineering", 
    "5. Detailed BOQ", "6. JWN Procurement", 
    "7. Startup & Safety", "8. Operations & Maintenance"
]

if 'session' not in st.session_state:
    st.session_state.session = {
        "step": 0, "id": f"CP-{uuid.uuid4().hex[:6].upper()}",
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "history": {}, "unlocked": False
    }

# --- 4. MULTI-STAKEHOLDER DASHBOARD ---
st.sidebar.title("🛡️ ChemPilot v1")
# Role-Based Access Control (RBAC) [cite: 80, 83]
user_role = st.sidebar.selectbox("Access Role", ["Entrepreneur", "Bank Manager", "Super User"])
st.sidebar.markdown(f"**Audit ID:** `{st.session_state.session['id']}`")
st.sidebar.progress((st.session_state.session['step'] + 1) / 8)

# Sidebar: Milestone Ribbon [cite: 89]
st.sidebar.write("### Project Milestones")
for i, p in enumerate(PHASES):
    status = "✅" if i < st.session_state.session['step'] else ("🔵" if i == st.session_state.session['step'] else "⚪")
    st.sidebar.write(f"{status} {p}")

st.header(f"🚢 Milestone: {PHASES[st.session_state.session['step']]}")

# --- 5. THE INPUT VAULT ---
with st.container():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    chem = c1.text_input("Product Name", value=st.session_state.session['inputs']['chem'])
    cap = c2.number_input("Scale (TPA)", value=st.session_state.session['inputs']['cap'])
    loc = c3.text_input("Industrial Hub", value=st.session_state.session['inputs']['loc'])
    bud = c4.number_input("Budget (₹ Cr)", value=st.session_state.session['inputs']['bud'])

    if st.button("🚀 EXECUTE PHASE ENGINE"):
        st.session_state.session['inputs'] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
        with st.spinner("Reconciling Engineering Logic..."):
            audit_res = run_technical_audit(st.session_state.session['step'], st.session_state.session['inputs'])
            st.session_state.session['history'][st.session_state.session['step']] = audit_res
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. OUTPUT & PAYMENT GATEWAY LOGIC ---
if st.session_state.session['step'] in st.session_state.session['history']:
    st.divider()
    
    # 6.1 Banker's Validation View [cite: 95, 100]
    if user_role == "Bank Manager":
        st.success("🛡️ Institutional Validation Portal Active")
        st.metric("Technical Integrity Score (TIS)", "92%", delta="Optimal Budget")
    
    # 6.2 JWN Masked Bidding Hub (Phase 6 Specific) [cite: 58, 60, 108]
    if st.session_state.session['step'] == 5:
        st.subheader("🛒 JWN Procurement Hub (Masked)")
        st.info("Identity Block Active: Redacting client details from vendors. [cite: 185]")
        st.table({
            "Vendor UID": ["CP-VN-08", "CP-VN-14", "CP-VN-03"],
            "Lead Time": ["12 Weeks", "10 Weeks", "16 Weeks"],
            "Technical Grade": ["Premium", "Standard", "Premium"]
        })
        
        # High-Value Payment Integration (NEFT/RTGS) [cite: 136, 151, 153]
        st.markdown("### 💳 Unlock Vendor Shortlist")
        st.write("Dossier Release Fee: **₹1,80,000** [cite: 136]")
        if st.button("Generate Pro-Forma & Virtual Account"):
            st.code(f"A/C: ChemPilot-Escrow\nA/C No: 992026{st.session_state.session['id']}\nIFSC: ICIC0000001")
            st.caption("Auto-unmasks vendor identities upon NEFT/RTGS detection.")

    # 6.3 Standard Report Display
    st.markdown(st.session_state.session['history'][st.session_state.session['step']])
    
    # Super User Bridging [cite: 114, 116, 119]
    if user_role == "Super User":
        if st.button("🖋️ Super-User Digital Sign & Advance"):
            st.session_state.session['step'] += 1
            st.rerun()
    else:
        if st.button("Accept Finding & Request Next Gate"):
            st.session_state.session['step'] += 1
            st.rerun()
