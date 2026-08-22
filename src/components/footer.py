import streamlit as st

def footer():
    st.markdown("""
    <style>
        .custom-footer {
            width: 100% !important;
            box-sizing: border-box !important;
            margin-top: 4rem !important;
            padding: 1.5rem 2rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 1.5rem !important;
            background: #172554 !important;
            color: #ffffff !important;
            border-top: 4px solid #fbbf24 !important;
            border-radius: 1.5rem 1.5rem 0 0 !important;
            font-family: 'Libre Baskerville', serif !important;
            box-shadow: 0 -12px 28px rgba(23, 37, 84, 0.16) !important;
        }

        .custom-footer .footer-title {
            font-family: 'Elsie', serif !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            color: #ffffff !important;
            letter-spacing: 0 !important;
        }

        .custom-footer .footer-text {
            font-family: 'Libre Baskerville', serif !important;
            font-size: 0.78rem !important;
            line-height: 1.5 !important;
            margin: 0 !important;
            color: #dbeafe !important;
        }

        .custom-footer .footer-status {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.45rem !important;
            color: #fde68a !important;
            font-size: 0.75rem !important;
            white-space: nowrap !important;
        }

        .custom-footer .footer-status::before {
            content: '' !important;
            width: 0.5rem !important;
            height: 0.5rem !important;
            display: inline-block !important;
            background: #4ade80 !important;
            border-radius: 50% !important;
            box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.16) !important;
        }

        .custom-footer .footer-copy {
            text-align: right !important;
        }

        @media (max-width: 640px) {
            .custom-footer {
                flex-direction: column !important;
                align-items: center !important;
                text-align: center !important;
                padding: 1.35rem 1rem !important;
            }

            .custom-footer .footer-copy {
                text-align: center !important;
            }
        }
    </style>

    <div class="custom-footer">
        <div>
            <div class="footer-title">FaceMark</div>
            <div class="footer-text">Smart attendance, made simple.</div>
        </div>
        <div class="footer-status">System ready</div>
        <div class="footer-copy">
            <div class="footer-text">Smart &bull; Fast &bull; Secure</div>
            <div class="footer-text">&copy; 2026 FaceMark</div>
        </div>
    </div>
    """, unsafe_allow_html=True)