import streamlit as st
import json

st.set_page_config(page_title="Healthcare Treatment Plan", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Disease database with symptoms and treatments
DISEASE_DATABASE = {
    "Fever": {
        "symptoms": ["high temperature", "chills", "body ache", "fatigue", "fever"],
        "treatment": [
            "Take paracetamol 500mg every 4-6 hours",
            "Stay hydrated - drink plenty of water",
            "Rest for 24-48 hours",
            "Use cool compress on forehead",
            "Consult doctor if fever persists beyond 3 days"
        ],
        "diet": "Light food, soups, and warm liquids"
    },
    "Gastritis": {
        "symptoms": ["stomach pain", "nausea", "bloating", "loss of appetite", "gastric", "acidity"],
        "treatment": [
            "Take antacid (Omeprazole 20mg daily)",
            "Avoid spicy and fatty foods",
            "Eat small frequent meals",
            "Reduce caffeine intake",
            "Consult gastroenterologist if symptoms persist"
        ],
        "diet": "Bland foods, yogurt, milk, banana, rice"
    },
    "Common Cold": {
        "symptoms": ["runny nose", "cough", "sore throat", "sneezing", "cold"],
        "treatment": [
            "Take vitamin C supplements",
            "Use saline nasal drops",
            "Drink warm water with honey",
            "Rest adequately",
            "Gargle with salt water for sore throat"
        ],
        "diet": "Citrus fruits, ginger tea, chicken soup"
    },
    "Headache": {
        "symptoms": ["head pain", "pressure", "tension", "dizziness", "headache", "migraine"],
        "treatment": [
            "Take ibuprofen 200mg or aspirin 500mg",
            "Apply cold compress to temples",
            "Reduce screen time",
            "Practice relaxation techniques",
            "Stay in dark, quiet room"
        ],
        "diet": "Stay hydrated, avoid caffeine"
    },
    "Hypertension": {
        "symptoms": ["high blood pressure", "headache", "chest pain", "fatigue", "hypertension", "bp"],
        "treatment": [
            "Take prescribed BP medication regularly",
            "Monitor blood pressure daily",
            "Reduce salt intake",
            "Exercise 30 minutes daily",
            "Regular follow-up with cardiologist"
        ],
        "diet": "Low-sodium foods, leafy greens, whole grains"
    },
    "Diabetes": {
        "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "diabetes", "sugar"],
        "treatment": [
            "Take insulin or oral antidiabetic drugs",
            "Monitor blood glucose levels",
            "Follow diabetic diet strictly",
            "Exercise regularly (30-45 mins daily)",
            "Monthly check-ups with endocrinologist"
        ],
        "diet": "Whole grains, vegetables, lean proteins, avoid sugar"
    },
    "Anxiety": {
        "symptoms": ["nervousness", "rapid heartbeat", "sweating", "restlessness", "anxiety", "panic"],
        "treatment": [
            "Practice deep breathing exercises",
            "Take prescribed anxiolytics if needed",
            "Regular exercise and meditation",
            "Limit caffeine intake",
            "Counseling or therapy sessions"
        ],
        "diet": "Balanced diet, omega-3 rich foods, herbal teas"
    },
    "Insomnia": {
        "symptoms": ["difficulty sleeping", "waking at night", "fatigue", "irritability", "sleep", "insomnia"],
        "treatment": [
            "Maintain consistent sleep schedule",
            "Avoid screens 1 hour before bed",
            "Take melatonin if needed",
            "Practice relaxation techniques",
            "Consult sleep specialist if persistent"
        ],
        "diet": "Avoid caffeine after 3 PM, warm milk before bed"
    },
    "Allergies": {
        "symptoms": ["itching", "rash", "swelling", "hives", "allergic", "allergy"],
        "treatment": [
            "Take antihistamine (Cetirizine 10mg)",
            "Avoid allergen source",
            "Apply soothing lotion to skin",
            "Use ice packs for swelling",
            "Visit allergist for testing"
        ],
        "diet": "Avoid trigger foods, eat anti-inflammatory foods"
    }
}

def predict_disease(symptoms_text):
    """Simple disease prediction based on symptom matching"""
    symptoms_text = symptoms_text.lower()
    
    scores = {}
    for disease, info in DISEASE_DATABASE.items():
        score = 0
        for symptom in info["symptoms"]:
            if symptom in symptoms_text:
                score += 1
        if score > 0:
            scores[disease] = score
    
    if not scores:
        return None, None
    
    predicted_disease = max(scores, key=scores.get)
    confidence = (scores[predicted_disease] / len(DISEASE_DATABASE[predicted_disease]["symptoms"])) * 100
    return predicted_disease, min(confidence, 100)

def get_treatment_plan(disease, age, gender, medical_history):
    """Generate personalized treatment plan"""
    if disease not in DISEASE_DATABASE:
        return None
    
    disease_info = DISEASE_DATABASE[disease]
    
    plan = {
        "disease": disease,
        "recommendations": disease_info["treatment"],
        "diet": disease_info["diet"],
        "personalized_notes": []
    }
    
    # Age-specific recommendations
    if age < 12:
        plan["personalized_notes"].append("👶 Consult pediatrician before taking any medication")
    elif age > 60:
        plan["personalized_notes"].append("👴 Elderly patient - May require dosage adjustment")
    
    # Gender-specific notes
    if gender == "Female":
        plan["personalized_notes"].append("👩 Pregnancy status should be confirmed before treatment")
    
    # History-based notes
    if "diabetes" in medical_history.lower():
        plan["personalized_notes"].append("⚠️ Diabetic patient - Monitor blood sugar regularly")
    if "hypertension" in medical_history.lower():
        plan["personalized_notes"].append("⚠️ High BP patient - Avoid high-sodium foods")
    if "allergy" in medical_history.lower():
        plan["personalized_notes"].append("⚠️ Allergic patient - Check medication allergies")
    
    return plan

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.emoji("🏥")
with col2:
    st.title("AI-Based Personalized Treatment Plan Generator")
st.write("Get instant disease prediction and personalized treatment recommendations")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Patient Information")
    age = st.slider("Age", 0, 100, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    medical_history = st.text_area("Medical History", placeholder="e.g., diabetes, hypertension, allergies...")

# Main content
st.header("💊 Symptom Analysis & Treatment Plan")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Symptoms")
    symptoms = st.text_area("Enter your symptoms (comma-separated or describe)", 
                           placeholder="e.g., high temperature, chills, body ache",
                           height=150)
    
with col2:
    st.subheader("Quick Symptom Tips")
    st.info("""
    **Common symptoms to enter:**
    - Fever: high temperature, chills, body ache
    - Stomach: stomach pain, nausea, bloating
    - Cold: runny nose, cough, sore throat
    - Headache: head pain, pressure, tension
    - Diabetes: increased thirst, frequent urination
    - Anxiety: nervousness, rapid heartbeat
    """)

# Generate Treatment Plan
if st.button("🔍 Generate Treatment Plan", use_container_width=True, key="generate"):
    if not symptoms.strip():
        st.error("❌ Please enter symptoms first!")
    else:
        # Predict disease
        predicted_disease, confidence = predict_disease(symptoms)
        
        if predicted_disease:
            st.success(f"✅ Predicted Condition: **{predicted_disease}** (Confidence: {confidence:.1f}%)")
            
            # Get treatment plan
            treatment_plan = get_treatment_plan(predicted_disease, age, gender, medical_history)
            
            if treatment_plan:
                st.divider()
                
                # Treatment Recommendations
                st.subheader("💉 Treatment Recommendations")
                for i, rec in enumerate(treatment_plan["recommendations"], 1):
                    st.write(f"**{i}.** {rec}")
                
                # Diet Recommendations
                st.subheader("🥗 Recommended Diet")
                st.info(treatment_plan["diet"])
                
                # Personalized Notes
                if treatment_plan["personalized_notes"]:
                    st.subheader("⚠️ Personalized Health Notes")
                    for note in treatment_plan["personalized_notes"]:
                        st.warning(note)
                
                # Follow-up
                st.divider()
                st.subheader("📞 Next Steps")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("✅ Follow treatment for 3-5 days")
                with col2:
                    st.write("📅 Consult doctor if symptoms persist")
                with col3:
                    st.write("🏥 Emergency: Call 112")
        else:
            st.warning("⚠️ Could not identify specific condition from symptoms. Please describe more clearly or consult a doctor.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px; padding: 20px;'>
<p>⚕️ <b>Disclaimer:</b> This is an AI-based assistant and NOT a substitute for professional medical advice.</p>
<p>Always consult a qualified healthcare provider for accurate diagnosis and treatment.</p>
<p>In case of emergency, call your local emergency number immediately.</p>
</div>
""", unsafe_allow_html=True)
