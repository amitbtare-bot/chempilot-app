import streamlit as st

st.set_page_config(page_title="Vendor Marketplace", layout="wide")

st.header("🏗️ Registered Vendor Marketplace")
st.write("Matching equipment suppliers for your project location and scale.")

# Example Marketplace Logic
vendors = [
    {"Company": "Praj Industries", "Specialty": "Bio-Chemicals / Ethanol", "Region": "Pune / Pan-India"},
    {"Company": "Thermax", "Specialty": "Boilers & Utilities", "Region": "Gujarat / Maharashtra"},
    {"Company": "L&T Heavy Engineering", "Specialty": "Reactors & Columns", "Region": "Hazira"}
]

st.table(vendors)
st.button("Request Quotes from All Verified Vendors")
