import streamlit as st
import google.generativeai as genai
import uuid

# --- 1. SETTINGS ---
st.set_page_config(page_title="ChemPilot Pro | Adaptive Engine", layout="wide")
st.markdown("<style>.stApp { background: #0d1117; color: white; }</style>", unsafe_allow_html=True)

# --- 2. ADAPTIVE MODEL DISCOVERY ---
def get_working_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        # List all models to find the one available to your key
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Prioritize Flash for speed and quota
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        # Fallback to the first available model if Flash isn't found
        return genai.list_models()[0].name
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# --- 3. THE RESILIENT ENGINE ---
def run_v1_engine(phase_idx, inputs):
    model_name = get_working_model()
    if not model_name:
        return "ERROR: Could not find a valid model. Check your API key."
    
    try:
        model = genai.GenerativeModel(model_name)
        prompt = f"Technical Audit Phase {phase_idx+1}: {inputs['chem']} at {inputs['cap']} TPA in {inputs['loc']}."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ENGINE_ERROR: {str(e)}"

# --- 4. THE JOURNEY ---
if 'project' not in st.session_state:
    st.session_state.project = {
        "step": 0,
        "inputs": {"chem": "", "cap": 0, "loc": "", "bud": 0},
        "reports": {},
        "id": f"CP-{uuid.uuid4().hex[:6].upper()}"
    }

st.title("🚢 ChemPilot v1 Intelligence")
st.sidebar.markdown(f"**Audit ID:** `{st.session_state.project['id']}`")
st.sidebar.write(f"**Model Active:** `{get_working_model()}`")

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: chem = st.text_input("Chemical", value=st.session_state.project['inputs']['chem'])
    with c2: cap = st.number_input("Scale (TPA)", value=st.session_state.project['inputs']['cap'])
    with c3: loc = st.text_input("Location", value=st.session_state.project['inputs']['loc'])
    with c4: bud = st.number_input("Budget (₹ Cr)", value=st.session_state.project['inputs']['bud'])
    
    if st.button("🚀 EXECUTE PHASE AUDIT", use_container_width=True):
        st.session_state.project['inputs'] = {"chem": chem, "cap": cap, "loc": loc, "bud": bud}
        result = run_v1_engine(st.session_state.project['step'], st.session_state.project['inputs'])
        st.session_state.project['reports'][st.session_state.project['step']] = result

if st.session_state.project['step'] in st.session_state.project['reports']:
    st.divider()
    st.markdown(st.session_state.project['reports'][st.session_state.project['step']])
    
    if st.button(f"Accept & Advance to Phase {st.session_state.project['step']+2}"):
        st.session_state.project['step'] += 1
        st.rerun()
