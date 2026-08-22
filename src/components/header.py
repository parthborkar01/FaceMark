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