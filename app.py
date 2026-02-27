import streamlit as st
import google.generativeai as genai

# --- 1. THEME & GLASSMORPHISM CSS ---
st.set_page_config(page_title="ChemPilot Pro | Global Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Full Page Dark Gradient */
    .stApp { background: radial-gradient(circle at top, #1a1a2e, #16213e, #0f3460); color: #f0f2f6; }
    
    /* Hero Container for Inputs */
    .hero-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 25px; border-radius: 20px;
        margin-bottom: 30px;
    }
    
    /* Center Stage Cards */
    .center-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; border-left: 5px solid #00f2ff;
        padding: 20px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE HERO SECTION (Project Command) ---
# Moving inputs from sidebar to the wide center-top for better UX
with st.container():
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        selected_chem = st.selectbox(
            "Project Target (Chemical or CAS)",
            options=["Ethanol (64-17-5)", "Methanol (67-56-1)", "Acetic Acid (64-19-7)"],
            index=0, accept_new_options=True
        )
    with col2:
        user_cap = st.number_input("Annual Scale (TPA)", value=100000, step=10000)
    with col3:
        exact_loc = st.text_input("Plant Location", "Dahej, Gujarat")
    
    run_audit = st.button("🚀 EXECUTE COMPREHENSIVE AUDIT", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. THE CENTER STAGE (Data Display) ---
if run_audit:
    # Top Level Metrics in Glass Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Projected ROI", "22.4%", "+2.1%")
    m2.metric("Est. CAPEX", "₹480 Cr", "Fixed")
    m3.metric("Payback", "3.8 Years", "-0.2 Yrs")
    m4.metric("Market Sentiment", "Bullish", "High Demand")

    # The main "Wasted Space" is now a 2-column deep-dive
    main_col, side_col = st.columns([2, 1])

    with main_col:
        st.markdown('<div class="center-card">', unsafe_allow_html=True)
        st.subheader("🛠️ Technical Process Flow (2026 Standards)")
        st.info("Visualizing reaction kinetics and mass balance for the target scale...")
        # (This is where the Gemini Report or a PFD Image would go)
        st.markdown('</div>', unsafe_allow_html=True)

    with side_col:
        st.markdown('<div class="center-card">', unsafe_allow_html=True)
        st.subheader("📍 Logistics Intelligence")
        st.write(f"Evaluating freight corridors from **{exact_loc}**.")
        st.progress(85, text="Connectivity Score")
        st.markdown('</div>', unsafe_allow_html=True)
