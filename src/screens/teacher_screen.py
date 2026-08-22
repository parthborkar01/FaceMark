import streamlit as st
from src.components.header import header_dashBoard
from src.components.footer import footer
def teacher_screen():
    st.markdown("""
        <style>
            .stApp {
                background: #f0d5e4 !important;
                background-image: none !important;
            }

            .stApp::before,
            .stApp::after {
                display: none !important;
            }

        </style>
    """, unsafe_allow_html=True)

    if "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_scree_login()
    elif st.session_state.teacher_login_type == 'register':
         teacher_screen_register()

def teacher_scree_login():
    header_dashBoard()
    st.markdown("""
        <div style="
            width: 100%;
            height: 2px;
            margin: 0.75rem 0 1rem 0;
            background-color: #a6a2a4;
        "></div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <style>
            .teacher-markdown-title {
                margin: 0 !important;
                padding: 0 !important;
                color: #3f3a3d !important;
                font-family: 'Libre Baskerville', serif !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                line-height: 1.2 !important;
                text-align: center !important;
                margin-top:0.5rem !important;
            }
        </style>
        <h3 class="teacher-markdown-title">Login using password</h3>
    """,unsafe_allow_html=True)
    st.markdown("""
        <style>
            [data-testid="stTextInput"] label {
                color: #000000 !important;
            }

            [data-testid="stTextInput"] input {
                background-color: transparent !important;
                color: #000000 !important;
                border: none !important;
            }

            [data-testid="stTextInput"] input::placeholder {
                color: #000000 !important;
                opacity: 0.55 !important;
            }

            .st-key-teacher_login button,
            .st-key-teacher_register button {
                width: 100% !important;
                border: none !important;
                border-radius: 0.8rem !important;
                padding: 0.55rem 1rem !important;
                color: #000000 !important;
                font-size: 2.4rem !important;
                line-height: 1.25 !important;
                font-weight: 600 !important;
                transition: background-color 0.2s ease, transform 0.2s ease !important;
            }

            .st-key-teacher_login button {
                background-color: #ec4899 !important;
            }

            .st-key-teacher_register button {
                background-color: #3b82f6 !important;
            }

            .st-key-teacher_login button:hover {
                background-color: #db2777 !important;
                transform: translateY(-2px) !important;
            }

            .st-key-teacher_register button:hover {
                background-color: #2563eb !important;
                transform: translateY(-2px) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.space()
    teacher_username = st.text_input("Enter userName",placeholder="parthborkar10")
    teacher_pass = st.text_input("Enter password",placeholder="123***",type="password")
    st.markdown("""
            <div style="
                width: 100%;
                height: 2px;
                margin: 0.75rem 0 1rem 0;
                background-color: #000000;
            "></div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2,gap=2)
    with col1:
        st.button("Login", width="stretch", key="teacher_login")
    with col2:
        if st.button("Register Page", width="stretch", key="teacher_register"):
            st.session_state.teacher_login_type = "register"
            st.rerun()
        
            
    footer()
def teacher_screen_register():
    header_dashBoard()
    st.markdown("""
            <div style="
                width: 100%;
                height: 2px;
                margin: 0.75rem 0 1rem 0;
                background-color: #a6a2a4;
            "></div>
        """, unsafe_allow_html=True)
    st.markdown("""
            <style>
                .teacher-markdown-title {
                    margin: 0 !important;
                    padding: 0 !important;
                    color: #3f3a3d !important;
                    font-family: 'Libre Baskerville', serif !important;
                    font-size: 1.5rem !important;
                    font-weight: 700 !important;
                    line-height: 1.2 !important;
                    text-align: center !important;
                    margin-top:0.5rem !important;
                }
            </style>
            <h3 class="teacher-markdown-title">Register as a Teacher</h3>
        """,unsafe_allow_html=True)
    st.markdown("""
            <style>
                [data-testid="stTextInput"] label {
                    color: #000000 !important;
                }
    
                [data-testid="stTextInput"] input {
                    background-color: transparent !important;
                    color: #000000 !important;
                    border: none !important;
                }
    
                [data-testid="stTextInput"] input::placeholder {
                    color: #000000 !important;
                    opacity: 0.55 !important;
                }
    
                .st-key-teacher_register_login button,
                .st-key-teacher_register_submit button {
                    width: 100% !important;
                    border: none !important;
                    border-radius: 0.8rem !important;
                    padding: 0.55rem 1rem !important;
                    color: #000000 !important;
                    font-size: 2.4rem !important;
                    line-height: 1.25 !important;
                    font-weight: 600 !important;
                    transition: background-color 0.2s ease, transform 0.2s ease !important;
                }
    
                .st-key-teacher_register_login button {
                    background-color: #ec4899 !important;
                }
    
                .st-key-teacher_register_submit button {
                    background-color: #3b82f6 !important;
                }
    
                .st-key-teacher_register_login button:hover {
                    background-color: #db2777 !important;
                    transform: translateY(-2px) !important;
                }
    
                .st-key-teacher_register_submit button:hover {
                    background-color: #2563eb !important;
                    transform: translateY(-2px) !important;
                }
            </style>
        """, unsafe_allow_html=True)
    st.space()
    teacher_username = st.text_input("Enter userName",placeholder="parthborkar10")
    teacher_name = st.text_input("Enter Name", placeholder="Parth Borkar")
    teacher_pass = st.text_input("Enter password",placeholder="123***",type="password")
    teacher_pass_confirm = st.text_input("confirm Password",placeholder="123***",type="password")
    st.markdown("""
                <div style="
                    width: 100%;
                    height: 2px;
                    margin: 0.75rem 0 1rem 0;
                    background-color: #000000;
                "></div>
        """, unsafe_allow_html=True)
    col1, col2 = st.columns(2,gap=2)
    with col1:
        if st.button("Login Page", width="stretch", key="teacher_register_login"):
            st.session_state.teacher_login_type = "login"
            st.rerun()
    with col2:
        st.button("Register", width="stretch", key="teacher_register_submit")
            
                
    footer()
