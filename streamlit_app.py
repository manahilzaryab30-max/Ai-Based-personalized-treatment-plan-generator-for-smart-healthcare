import streamlit as st

st.set_page_config(page_title="Healthcare Treatment Plan", layout="wide")

# Header
st.title("🏥 AI-Based Personalized Treatment Plan Generator")
st.write("Predict diseases and get personalized treatment recommendations")

# Sidebar
with st.sidebar:
    st.header("Patient Information")
    age = st.slider("Age", 0, 100, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Symptoms")
    symptoms = st.text_area("Enter symptoms")
    
with col2:
    st.subheader("Medical History")
    history = st.text_area("Enter medical history")

if st.button("Generate Treatment Plan"):
    st.success("Treatment plan generated!")
    st.write("Your personalized recommendations will appear here")
