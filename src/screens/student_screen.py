import streamlit as st

def student_screen():
    st.header("Student Screen")
    back = st.button("Back",type="secondary")
    if back:
        st.session_state["login_type"] = None
        st.rerun()