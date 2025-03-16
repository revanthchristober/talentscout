# app/streamlit_app.py
import sys
import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.talentscout.crew import Talentscout

load_dotenv()

def collect_candidate_info():
    with st.form("candidate_info"):
        st.header("Candidate Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50)
        position = st.text_input("Desired Position")
        location = st.text_input("Current Location")
        tech_stack = st.text_input("Tech Stack (comma-separated)")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            return {
                "candidate": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "experience": experience,
                    "position": position,
                    "location": location,
                    "tech_stack": [t.strip() for t in tech_stack.split(",")]
                }
            }
    return None

def main():
    st.set_page_config(page_title="TalentScout", page_icon="🤖")
    st.title("TalentScout Hiring Assistant")
    
    inputs = collect_candidate_info()
    
    if inputs:
        with st.spinner("Processing application..."):
            try:
                result = Talentscout().crew().kickoff(inputs=inputs)
                
                if result:
                    st.success("Analysis complete!")
                    # st.subheader("Candidate Report")
                    st.subheader("Results:")
                    st.markdown(result)
                    # st.subheader("Technical Questions")
                    # st.markdown(result.get("questions", "No questions generated"))
                    
            except Exception as e:
                st.error(f"Processing failed: {str(e)}")

if __name__ == "__main__":
    main()