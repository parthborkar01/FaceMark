import streamlit as st
from src.database.db import create_subject

@st.dialog("create new Subject")
def create_subject_dialog(teacher_id):
    st.markdown("""
            <style>
                .st-key-create_subject button {
                    background-color: #ec4899 !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 0.8rem !important;
                    padding: 0.55rem 1rem !important;
                    font-size: 1rem !important;
                    font-weight: 600 !important;
                    transition: background-color 0.2s ease, transform 0.2s ease !important;
                }
    
                .st-key-create_subject button:hover {
                    background-color: #db2777 !important;
                    transform: translateY(-2px) !important;
                }
            </style>
    """, unsafe_allow_html=True)
    st.write("Enter the details of the subject")
    sub_id = st.text_input("Subject_id",placeholder='DSA101')
    sub_name = st.text_input("Subjext name",placeholder="Introduction to Data Structure")
    sub_session = st.text_input("Section",placeholder='A')

    if st.button("Create subject Now",width='stretch'):
        if sub_session and sub_name and sub_id: 
            try:
                create_subject(sub_id,sub_name,sub_session,teacher_id)
                st.rerun()
                st.toast("subject created successfully")
            except Exception as e:
                st.error(f"error {e}")
        else:
            st.warning("All fields are required")