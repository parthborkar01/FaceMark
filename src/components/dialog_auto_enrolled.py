import streamlit as st
from src.database.db import supabase
import time
from src.database.db import enroll_student_to_subject
@st.dialog("Quick enrollement")
def auto_enrolled_dialog(join_code):
    student_id = st.session_state.student_data['student_id']
    res = supabase.table('subjects').select('subject_id,name').eq('subject_code',join_code).execute()
    if not res.data:
        st.error(f'subject vode is not exist {join_code}')
        if st.button('close'):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]
    check = supabase.table("subject_students").select("*").eq("subject_id",subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.warning("You are already enrolled in this program")
        if st.button('close'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in {subject['name']} ?")
    col1,col2 = st.columns(2)
    with col1:
        if st.button('No thanks',type='primary',width='stretch'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("yes enroll now",type='primary',width='stretch'):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.success("enroll successfully")
            st.query_params.clear()
            time.sleep(1)
            st.rerun()