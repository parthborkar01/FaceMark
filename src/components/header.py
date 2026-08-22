import streamlit as st

def header():
    st.markdown("""
        <style>
            .facemark-header {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 1rem 0 2rem 0;
            }

            .facemark-header img {
                width: 80px;
                height: 80px;
                object-fit: contain;
                filter: drop-shadow(0 8px 14px rgba(0, 0, 0, 0.28));
            }

            .facemark-title {
                margin: 0.35rem 0 0 0 !important;
                color: #ffffff !important;
                font-family: 'Elsie', serif !important;
                font-size: 3.5rem !important;
                line-height: 1 !important;
                text-align: center !important;
                text-shadow: 0 4px 18px rgba(0, 0, 0, 0.32) !important;
            }

            .facemark-accent {
                width: 4rem;
                height: 0.25rem;
                margin-top: 0.8rem;
                border-radius: 1rem;
                background: #fbbf24;
                box-shadow: 0 0 18px rgba(251, 191, 36, 0.7);
            }
        </style>

        <div class="facemark-header">
            <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="FaceMark logo"/>
            <h2 class="facemark-title">FaceMark</h2>
            <div class="facemark-accent"></div>
        </div>
    """,unsafe_allow_html=True)


def header_dashBoard():
    st.markdown("""
        <style>
            .inner_div{
                display:flex;
                flex-direction:row;
                align-items:center;
                justify-content:center;
                gap:1rem;
                margin-top:1.5rem !important;
            }
            /* Google Fonts */
                        @import url('https://fonts.googleapis.com/css2?family=Elsie:wght@400;900&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400;1,700&display=swap');
            
                        /* Hide Streamlit default UI */
                        #MainMenu {
                            visibility: hidden !important;
                        }
            
                        header {
                            visibility: hidden !important;
                        }
            
                        footer {
                            visibility: hidden !important;
                        }
            
                        /* Main container */
                        .block-container {
                            padding-top: 0.5rem !important;
                        }
            
                        /* H2 heading */
                        h2 {
                            font-family: 'Elsie', serif !important;
                            font-size: 2rem !important;
                            line-height: 1.1 !important;
                            color:#595658 !important;
                            text-align: center !important;
                        }
                        .st-key-dashboard_home button {
                            width: auto !important;
                            min-width: 120px !important;
                            background-color: #ec4899 !important;
                            color: white !important;
                            border: none !important;
                            border-radius: 0.8rem !important;
                            padding: 0.35rem 0.8rem !important;
                            font-family: 'Libre Baskerville', serif !important;
                            font-size: 0.82rem !important;
                        }

                        .st-key-dashboard_home {
                            display: flex !important;
                            justify-content: flex-end !important;
                        }

                        .st-key-dashboard_home button:hover {
                            background-color: #db2777 !important;
                        }
        </style>

    """,unsafe_allow_html=True)

    header_column, button_column = st.columns(2, vertical_alignment="center")
    with header_column:
        st.markdown("""
            <div class="inner_div">
                <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="FaceMark logo" width=75/>
                <h2>FaceMark</h2>
            </div>
        """, unsafe_allow_html=True)
    with button_column:
        go_home = st.button("Go Home", key="dashboard_home")

    if go_home:
        st.session_state["login_type"] = None
        st.rerun()