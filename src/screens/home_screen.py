import streamlit as st
from src.components.header import header
from src.components.footer import footer
from src.ui.base_layout import style_base_layout,base_backGround_dashBoard,home_button,card_style
def home_screen():
    base_backGround_dashBoard()
    style_base_layout()
    card_style()
    home_button()
    header()
    left,center,right = st.columns([1,6,1])
    with center:
        col1, col2 = st.columns(2,gap="large")


        with col1:
            with st.container(key="student_card"):
                st.markdown("""
                    <h3 style="font-size:28px; color:black; margin-bottom:0rem;">I'm Student</h3>
                """,unsafe_allow_html=True)
                st.markdown("""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin-top:0rem;
                        margin-bottom:5px;
                    ">
                        <img 
                            src="https://i.ibb.co/844D9Lrt/mascot-student.png"
                            style="
                                width: 180px;
                                height: 190px;
                                display: block;
                                object-fit: contain;
                            "
                        >
                    </div>
                """, unsafe_allow_html=True)
                student = st.button("Student  ↑",type='primary')
                if student:
                    st.session_state["login_type"] = "student"
                    st.rerun()


        with col2:
            with st.container(key="teacher_card"):
                st.markdown("""
                     <h3 style="font-size:28px; color:black; margin-bottom:0rem;">I'm Teacher</h3>
                """,unsafe_allow_html=True)
                st.markdown("""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            margin-top:0rem;
                            margin-bottom:5px;
                        ">
                        <img 
                            src="https://i.ibb.co/CsmQQV6X/mascot-prof.png"
                            style="
                            width: 180px;
                            height: 190px;
                            display: block;
                            object-fit: contain;
                            "
                        >
                    </div>
                """, unsafe_allow_html=True)       
                teacher = st.button("Teacher  ↑", type="primary")
                if teacher:
                    st.session_state["login_type"] = "teacher"
                    st.session_state["teacher_login_type"] = "login"
                    st.rerun()

    footer()