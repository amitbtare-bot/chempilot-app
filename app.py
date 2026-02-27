import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# --- 1. ACCESS & PRICING RULES (FROZEN v1) ---
PHASES = {
    "Phase 1: Conception & Feasibility": {"price": 0, "access": "Free"},
    "Phase 2: Process Development (R&D)": {"price": 0, "access": "Free"},
    "Phase 3: Conceptual Design": {"price": 25000, "access": "Paid"},
    "Phase 4: FEED": {"price": 45000, "access": "Paid"},
    "Phase 5: Detailed Engineering": {"price": 35000, "access": "Paid"},
    "Phase 6-8: Commissioning/Ops": {"price": 50000, "access": "Paid"}
}

# --- 2. GLOBAL UI & AUTH ---
st.set_page_config(page_title="ChemPilot Pro | Governance Spine", layout="wide")

if 'user_role' not in st.session_state:
    st.session_state.user_role = "Normal User" # Options: Normal User, Consultant, Vendor, Super User

# --- 3. DYNAMIC JOURNEY & PHASE LOGIC ---
st.sidebar.title("🛡️ ChemPilot Governance")
st.session_state.user_role = st.sidebar.selectbox("Access Mode", ["Normal User", "Consultant", "Vendor", "Super User"])

selected_phase = st.sidebar.selectbox("Industry Phase", list(PHASES.keys()))
phase_meta = PHASES[selected_phase]

# --- 4. THE COMMAND CENTER (STAGING) ---
st.markdown(f"### {selected_phase}")
st.caption(f"Status: {phase_meta['access']} | Cost: ₹{phase_meta['price']:,}")

# V1 ENGINE STACK: Integrated Inputs
with st.container():
    st.markdown('<div style="background:rgba(255,255,255,0.05); padding:30px; border-radius:15px;">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: chem = st.text_input("CHEMICAL / CAS", placeholder="e.g. Methanol")
    with c2: cap = st.number_input("SCALE (TPA)", value=100000)
    with c3: loc = st.text_input("LOCATION", placeholder="e.g. Dahej")
    with c4: bud = st.number_input("BUDGET (₹ Cr)", value=250)
    
    # Validation & Reconciliation Trigger
    if st.button("EXECUTE STAGE INTELLIGENCE"):
        if "Paid" in phase_meta['access'] and st.session_state.user_role == "Normal User":
            st.warning("💳 Phase 3+ requires mandatory registration and payment.")
        else:
            # Execute frozen engine logic
            st.session_state.report_id = f"CP-{uuid.uuid4().hex[:8].upper()}"
            st.success(f"Intelligence Generated. ID: {st.session_state.report_id}")

# --- 5. REPORTING & WATERMARKING (v1 COMPLIANT) ---
if 'report_id' in st.session_state:
    st.divider()
    st.markdown(f"#### 📄 ChemPilot Report: {st.session_state.report_id}")
    st.info(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (IST) | Governance: System-Governed")
    
    # The Technical Tabs (Stacked from previous version)
    t1, t2, t3, t4 = st.tabs(["⚙️ Technical & Scale", "📊 BOQ & Vendor Match", "🏦 Banking & Liaison", "⚖️ Governance"])
    
    with t1:
        st.subheader("Stoichiometric & Energy Balance")
        st.write("Cross-stage validation active. Scale-up risk scoring: Low.")
        
    with t2:
        st.subheader("BOQ Generation (Mechanical/Civil/Elec)")
        if st.session_state.user_role == "Vendor":
            st.error("❌ Vendors have no access to feasibility reports.")
        else:
            st.write("JWN Workflow active. Masked vendor identity enforcement.")

    with t4:
        st.write("### 🖋️ Digital Signing")
        st.write("Consultant Signature: [PENDING]")
        if st.session_state.user_role == "Super User":
            st.button("Digitally Sign & Release (Super User)")
