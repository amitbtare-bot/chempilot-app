import streamlit as st
import google.generativeai as genai
import uuid

# --- 1. STYLING ---
st.set_page_config(page_title="ChemPilot Pro | Adaptive Engine", layout="wide")
st.markdown("<style>.stApp { background: #0d1117; color: white; }</style>", unsafe_allow_html=True)

# --- 2. THE STABLE MODEL FINDER ---
def get_working_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        # Convert generator to a list to make it subscriptable
        model_list = list(genai.list_models())
        
        # 1. Look for the most stable 1.5 Flash model
        for m in model_list:
            if 'gemini-1.5-flash' in m.name and 'generateContent' in m.supported_generation_methods:
                return m.name
        
        # 2. Fallback: Find ANY model that supports generation
        for m in model_list:
            if 'generateContent' in m.supported_generation_methods:
                return m.name
                
        return None
    except Exception as e:
        st.error(f"API Connection Error: {str(e)}")
        return None

# --- 3. THE RESILIENT ENGINE ---
def run_v1_engine(phase_idx, inputs):
    model_name = get_working_model()
    if not model_name:
        return "ERROR: No compatible Gemini models found for this API key."
    
    try:
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        Execute ChemPilot v1 Engineering Audit:
        Phase: {phase_idx+1} | Product: {inputs['chem']} | Scale: {inputs['cap']} TPA.
        Provide: 1. Equipment Sizing 2. Side-reaction Analysis 3. Utility Load.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ENGINE_ERROR: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'project' not in st.session_state:
    st.session_state.project = {
        "step": 0,
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "reports": {},
        "id": f"CP-{uuid.uuid4().hex[:6].upper()}"
    }

# --- 5. THE DASHBOARD ---
st.title("🚢 ChemPilot v1 Intelligence")
st.sidebar.markdown(f"**Audit ID:** `{st.session_state.project['id']}`")

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: chem = st.text_input("Chemical", value=st.session_state.project['inputs']['chem'])
    with c2: cap = st.number_input("Scale (TPA)", value=st.session_state.project['inputs']['cap'])
    with c3: loc = st.text_input("Location", value=st.session_state.project['inputs']['loc'])
    with c4: bud = st.number_input("Budget (₹ Cr)", value=st.session_state.project['inputs']['bud'])
    
    if st.button("🚀 EXECUTE PHASE AUDIT", use_container_width=True):
        st.session_state.project['inputs'] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
        with st.spinner(f"Engaging {get_working_model()}..."):
            result = run_v1_engine(st.session_state.project['step'], st.session_state.project['inputs'])
            st.session_state.project['reports'][st.session_state.project['step']] = result

if st.session_state.project['step'] in st.session_state.project['reports']:
    st.divider()
    st.markdown(st.session_state.project['reports'][st.session_state.project['step']])
    
    if st.button(f"Accept & Advance to Phase {st.session_state.project['step']+2}"):
        st.session_state.project['step'] += 1
        st.rerun()
