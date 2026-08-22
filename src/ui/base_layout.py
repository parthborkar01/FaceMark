import streamlit as st
def base_backGround_dashBoard():
    st.markdown("""
        <style>
            .stApp {
                position: relative !important;
                isolation: isolate !important;
                overflow: hidden !important;
                background-color: #0b1220 !important;
                background-image:
                    linear-gradient(rgba(125, 211, 252, 0.08) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(125, 211, 252, 0.08) 1px, transparent 1px),
                    linear-gradient(135deg, #0b1220 0%, #182a49 48%, #164e63 100%) !important;
                background-size: 32px 32px, 32px 32px, 200% 200% !important;
                background-position: 0 0, 0 0, 0% 50% !important;
                background-attachment: fixed !important;
                animation: background-drift 20s ease-in-out infinite alternate !important;
            }

            .stApp::before,
            .stApp::after {
                content: '' !important;
                position: fixed !important;
                inset: -18% !important;
                z-index: 0 !important;
                pointer-events: none !important;
                background-repeat: no-repeat !important;
                opacity: 0.28 !important;
                transition: opacity 0.5s ease, filter 0.5s ease !important;
            }

            .stApp > div {
                position: relative !important;
                z-index: 1 !important;
            }

            .stApp::before {
                background-image:
                    radial-gradient(circle at 18% 24%, rgba(56, 189, 248, 0.5) 0 5%, transparent 5.5%),
                    radial-gradient(circle at 78% 18%, rgba(251, 191, 36, 0.42) 0 7%, transparent 7.5%),
                    radial-gradient(circle at 62% 80%, rgba(45, 212, 191, 0.38) 0 4%, transparent 4.5%);
                animation: bubble-drift 18s ease-in-out infinite alternate !important;
            }

            .stApp::after {
                background-image:
                    radial-gradient(circle at 88% 62%, rgba(14, 165, 233, 0.38) 0 8%, transparent 8.5%),
                    radial-gradient(circle at 34% 84%, rgba(245, 158, 11, 0.3) 0 5%, transparent 5.5%),
                    radial-gradient(circle at 46% 10%, rgba(96, 165, 250, 0.3) 0 3%, transparent 3.5%);
                animation: bubble-drift-reverse 24s ease-in-out infinite alternate !important;
            }

            .stApp:hover::before,
            .stApp:hover::after {
                opacity: 0.62 !important;
                filter: brightness(0.62) saturate(1.35) !important;
            }

            @keyframes background-drift {
                from {
                    background-position: 0 0, 0 0, 0% 50%;
                }
                to {
                    background-position: 32px 32px, 32px 32px, 100% 50%;
                }
            }

            @keyframes bubble-drift {
                from { transform: translate3d(-2%, -1%, 0) scale(0.96); }
                to { transform: translate3d(2%, 2%, 0) scale(1.04); }
            }

            @keyframes bubble-drift-reverse {
                from { transform: translate3d(2%, 1%, 0) scale(1.03); }
                to { transform: translate3d(-2%, -2%, 0) scale(0.97); }
            }

            @media (prefers-reduced-motion: reduce) {
                .stApp {
                    animation: none !important;
                }

                .stApp::before,
                .stApp::after {
                    animation: none !important;
                }
            }

            .block-container {
                padding-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>

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
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                color: black !important;
                text-align: center !important;
            }

            /* H3 heading */
            h3 {
                font-family: 'Libre Baskerville', serif !important;
                font-size: 1.25rem !important;
                line-height: 1.2 !important;
                color: black !important;
                text-align: center !important;
            }
        </style>
    """, unsafe_allow_html=True)


# Style for Home Button
def home_button():
    st.markdown("""
        <style>

            /* Streamlit button */
            div.stButton > button {
                border-radius: 1.5rem !important;
                width: 100% !important;
                background-color: #5865F2 !important;
                color: white !important;

                border: none !important;

                font-size: 2.75rem !important;
                font-weight: 500 !important;

                padding: 0.5rem 1.25rem !important;

                transition: transform 0.25s ease-in-out,
                            background-color 0.25s ease-in-out !important;
            }

            /* Hover */
            div.stButton > button:hover {
                transform: scale(1.05) !important;
                background-color: #4752C4 !important;
            }

            /* Click */
            div.stButton > button:active {
                transform: scale(0.98) !important;
            }

        </style>
    """, unsafe_allow_html=True)


def card_style():
    st.markdown("""
    <style>

        .st-key-student_card,
        .st-key-teacher_card {
            position: relative !important;
            z-index: 2 !important;
            background: rgba(255, 255, 255, 0.94) !important;
            padding: 1.75rem 1.5rem !important;
            border: 1px solid rgba(255, 255, 255, 0.95) !important;
            border-radius: 1.75rem !important;
            min-height: 390px !important;
            box-sizing: border-box !important;
            box-shadow: 0 16px 30px rgba(30, 64, 175, 0.14) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        .st-key-student_card:hover,
        .st-key-teacher_card:hover {
            transform: translateY(-6px) !important;
            box-shadow: 0 22px 38px rgba(30, 64, 175, 0.22) !important;
        }

        .st-key-student_card div.stButton > button,
        .st-key-teacher_card div.stButton > button {
            border-radius: 0.9rem !important;
            font-size: 1.05rem !important;
            padding: 0.5rem 1rem !important;
        }

    </style>
    """, unsafe_allow_html=True)