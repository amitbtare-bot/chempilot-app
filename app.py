import streamlit as st
st.set_page_config(page_title="ChemPilot SaaS", layout="wide")
# Initialize global data storage
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        "chemical": "",
        "capacity": 0,
        "math_result": "",
        "approved": False
    }

st.title("🚢 ChemPilot Landing")
st.write("Welcome to the Command Center. Use the sidebar to navigate.")import google.generativeai as genai

# --- CONFIGURATION & SECRETS ---
# This looks for your key in the Streamlit Cloud "Secrets" vault
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("❌ API Key not found! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- UI SETUP ---
st.set_page_config(page_title="ChemPilot SaaS", page_icon="🚢", layout="centered")
st.title("🚢 ChemPilot: Engineering Intelligence")
st.markdown("---")

# Initialize Session State (Memory)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'math_result' not in st.session_state:
    st.session_state.math_result = ""

# --- STEP 1: PROJECT INPUT ---
if st.session_state.step == 1:
    st.subheader("Start New Project")
    with st.form("input_form"):
        chemical = st.text_input("Target Chemical", placeholder="e.g., Acetic Acid")
        capacity = st.number_input("Annual Capacity (TPA)", min_value=1000, value=100000, step=1000)
        submit = st.form_submit_button("Generate Engineering Math")

        if submit and chemical:
            with st.spinner(f"🔍 Researching {chemical} process and calculating math..."):
                try:
                    # System instruction hidden from the user
                    prompt = f"""
                    Act as a Chemical Engineering Engine. 
                    Calculate the Material Balance and Utilities for a {chemical} plant at {capacity} TPA. 
                    1. Use Python (Code Execution) for stoichiometry and MW calculations.
                    2. Output a clean table with kg/hr for reactants and kW/Steam for utilities.
                    """
                    response = model.generate_content(prompt)
                    st.session_state.math_result = response.text
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Computation Error: {str(e)}")

# --- STEP 2: EVIDENCE REVIEW ---
elif st.session_state.step == 2:
    st.subheader("📊 Phase 1: Engineering Evidence Review")
    st.info("Verify the deterministic math below before generating the full DPR.")
    
    st.markdown(st.session_state.math_result)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Write Narrative"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("❌ Modify Inputs"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 3: NARRATIVE & VENDOR MATCHING ---
elif st.session_state.step == 3:
    st.subheader("📄 Phase 2: Report Finalization")
    st.success("Math Approved! Narrative and Vendor suggestions are being compiled...")
    
    st.write("---")
    st.write("### Recommended Suppliers (Marketplace)")
    st.write("* **Vendor A:** Reactor Specialist (Registered)")
    st.write("* **Vendor B:** Industrial Boiler Systems (Verified)")
    
    if st.button("🔄 Start New Calculation"):
        st.session_state.step = 1
        st.rerun()

# --- VENDOR SIDEBAR ---
st.sidebar.markdown("### Vendor Marketplace")
if st.sidebar.button("Register as a Supplier"):
    st.sidebar.info("Vendor registration portal coming soon!")


