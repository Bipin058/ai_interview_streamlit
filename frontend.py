# frontend.py
import streamlit as st
import requests
import pdfplumber

API_URL = "https://ai-interview-backend-38wc.onrender.com/add_user"
# API_URL = os.getenv("API_URL")
# API_URL = "http://localhost:8000/add_user"
st.title("User Registration Form")

name = st.text_input("Full Name")
email = st.text_input("Email")

uploaded_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])

resume_extracted = ""

if uploaded_pdf is not None:
    st.info("Extracting text from PDF...")

    try:
        with pdfplumber.open(uploaded_pdf) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        resume_extracted = text.strip()

        st.success("PDF extracted successfully!")
        # st.subheader("Extracted Resume Text:")
        # st.text_area("Resume Extracted Text", resume_extracted, height=200)

    except Exception as e:
        st.error(f"Error extracting PDF: {e}")

if st.button("Submit"):
    if not name or not email or not resume_extracted:
        st.error("Please fill all fields including PDF.")
    else:
        payload = {
            "name": name,
            "email": email,
            "resume_extracted": resume_extracted
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code == 400:
           st.error("A user with this email already exists.")
        if response.status_code == 200:
            st.success("User saved successfully! Email sent.")
        else:
            st.error("Error saving user")
            st.write(response.text)
