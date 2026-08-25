import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time
@st.dialog("enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll")
    join_code = st.text_input("Subject code", placeholder="E.g DSA101")

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

    if st.button("Enroll now",width='stretch'):
        if join_code:
            res = supabase.table('subjects').select("subject_id, name, subject_code").eq('subject_code',join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table("subject_students").select("*").eq("subject_id",subject['subject_id']).eq('student_id',student_id).execute()
                if check.data:
                    st.warning("You are already enrolled in this program")
                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success("Successfully enrolled")
                    time.sleep(1)
                    st.rerun()

        else:
            st.warning("Please enter a subject")
