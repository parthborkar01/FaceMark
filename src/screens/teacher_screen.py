import streamlit as st

def teacher_screen():
    st.header("Teacher screen")
    back = st.button("Back",type="secondary")
    if back:
        st.session_state["login_type"] = None
        st.rerun()