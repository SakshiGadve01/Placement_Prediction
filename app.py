import streamlit as st
import joblib
import numpy as np
import mysql.connector

# Load model
model = joblib.load("Model_AdaBoost.pkl")

# Title
st.title("🎓 Student Placement Prediction App")

# Input fields
CGPA = st.number_input("CGPA (0 - 10)", min_value=0.0, max_value=10.0, step=0.01)
Internships = st.number_input("Number of Internships", min_value=0)
Projects = st.number_input("Number of Projects", min_value=0)
Workshops = st.number_input("Workshops/Certifications Count", min_value=0)
AptitudeTestScore = st.slider("Aptitude Test Score (0 - 100)", 0, 100)
SoftSkillsRating = st.slider("Soft Skills Rating (1 - 10)", 1, 10)
SSC_Marks = st.number_input("SSC Marks (%)", min_value=0.0, max_value=100.0, step=0.1)
HSC_Marks = st.number_input("HSC Marks (%)", min_value=0.0, max_value=100.0, step=0.1)
ExtracurricularActivities = st.selectbox("Extracurricular Activities", ["No", "Yes"])
PlacementTraining = st.selectbox("Attended Placement Training?", ["No", "Yes"])

# Encode categorical
Extra_curr = 1 if ExtracurricularActivities == "Yes" else 0
Training = 1 if PlacementTraining == "Yes" else 0

if st.button("Predict Placement Status"):

    # Input for prediction
    input_data = np.array([[CGPA, Internships, Projects, Workshops, AptitudeTestScore,
                            SoftSkillsRating, SSC_Marks, HSC_Marks, Extra_curr, Training]])
    
    prediction = model.predict(input_data)[0]
    result = "Placed" if prediction == 1 else "Not Placed"

    # Show result
    st.subheader("🎯 Prediction Result:")
    if prediction == 1:
        st.success("✅ Student is likely to be Placed!")
    else:
        st.error("❌ Student is likely NOT to be Placed.")

    # Save to MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="Prediction",
            auth_plugin='mysql_native_password'  # Optional, use only if needed
        )
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO PlacementResults (
                CGPA, Internships, Projects, Workshops, AptitudeTestScore,
                SoftSkillsRating, SSC_Marks, HSC_Marks,
                ExtracurricularActivities, PlacementTraining, Prediction
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            CGPA, Internships, Projects, Workshops, AptitudeTestScore,
            SoftSkillsRating, SSC_Marks, HSC_Marks,
            ExtracurricularActivities, PlacementTraining, result
        )

        cursor.execute(insert_query, values)
        conn.commit()
        st.info("📝 Data saved to database successfully.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        st.error(f"❗ MySQL Error: {err}")
