import streamlit as st
from src.components.header import header_dashBoard,teacher_header_dashBoard
from src.components.footer import footer
from src.components.subject_card import subject_card
from src.database.db import create_teacher,check_teacher_exist,teacher_login,get_teacher_subject
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photo_dialog
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from src.database.db import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.dialog_attendance_result import attendance_result_dialog
from src.database.db import get_attendance_for_teacher
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

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_scree_login()
    elif st.session_state.teacher_login_type == 'register':
         teacher_screen_register()


def teacher_dashboard():
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
    data = st.session_state.teacher_data
    teacher_header_dashBoard()
    st.markdown("""
            <div style="
                width: 100%;
                height: 2px;
                margin: 0.75rem 0 1rem 0;
                background-color: #a6a2a4;
            "></div>
    """, unsafe_allow_html=True)

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    active_tab_key = {
        'take_attendance': 'take_attendance_tab',
        'manage_subject': 'manage_subject_tab',
        'attendance_record': 'attendance_record_tab',
    }[st.session_state.current_teacher_tab]

    st.markdown("""
        <style>
            .st-key-take_attendance_tab button,
            .st-key-manage_subject_tab button,
            .st-key-attendance_record_tab button {
                display: block !important;
                visibility: visible !important;
                width: 100% !important;
                min-height: 48px !important;
                border: none !important;
                border-radius: 0.8rem !important;
                padding: 0.55rem 0.75rem !important;
                color: #ffffff !important;
                background-color: #000000 !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                transition: background-color 0.2s ease, transform 0.2s ease !important;
            }

            .st-key-take_attendance_tab button:hover,
            .st-key-manage_subject_tab button:hover,
            .st-key-attendance_record_tab button:hover {
                background-color: #1f1f1f !important;
                transform: translateY(-2px) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <style>
            .st-key-{active_tab_key} button,
            .st-key-{active_tab_key} button:hover {{
                color: white !important;
                background-color: #ec4899 !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3 = st.columns(3)

    with tab1:
        if st.button("Take attendance", width="stretch", key="take_attendance_tab"):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        if st.button("Manage subject", width="stretch", key="manage_subject_tab"):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()
    with tab3:
        if st.button("Attendance Record", width="stretch", key="attendance_record_tab"):
            st.session_state.current_teacher_tab = 'attendance_record'
            st.rerun()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subject':
        teacher_tab_manage_subject()
    if st.session_state.current_teacher_tab == 'attendance_record':
        teacher_tab_attendance_record()

    footer()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    st.header("take AI attendance")
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)
    if not subjects:
        st.warning("You have not create a subject yes ...")

    subject_options = {f"{s['name']}-{s['subject_code']}" : s['subject_id'] for s in subjects}
    col1,col2 = st.columns(2)
    with col1:
        selected_subject_label = st.selectbox("Select subject", options=list(subject_options.keys()))

    with col2:
        st.space()
        if st.button("Add photos",type='primary',width='stretch'):
            add_photo_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    st.divider()
    if st.session_state.attendance_images:
        st.header("Added photos")
        galory_cols = st.columns(4)

        for i,img in enumerate(st.session_state.attendance_images):
            with galory_cols[i % 4]:
                st.image(img,width='stretch',caption=f'Photo {i + 1}')
    c1,c2,c3 = st.columns(3)
    has_photo = bool(st.session_state.attendance_images)
    with c1:
        if st.button("Clear all images",width='stretch',type='primary',disabled=not has_photo):
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        if st.button("Run the face Analysis",type='primary',width='stretch',disabled=not has_photo):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_ids = {}
                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected,_,_ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id,[]).append(f'Photo {idx+1}')

                enrolled_res = supabase.table("subject_students").select("*, students(*)").eq('subject_id',selected_subject_id).execute()
                enrolled_students = enrolled_res.data
                if not enrolled_students:
                    st.warning("No students are enrolled now")
                else:
                    result,attendance_to_log = [],[]
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']),[])
                        is_present = len(sources) > 0

                        result.append({
                            "Name" : student['name'],
                            'ID': student['student_id'],
                            "source" : ','.join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })
                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                        
                attendance_result_dialog(pd.DataFrame(result),attendance_to_log)
    with c3:
        if st.button("Use voice attendance",width='stretch',type='primary'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data["teacher_id"]
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
    col1,col2 = st.columns(2)
    with col1:
        st.header("Manage subject",width='stretch')
    with col2:
        if st.button("Create new subject", width="stretch", key="create_subject"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for subject in subjects:
            stats = [
                ("👥", "Students", subject["total_students"]),
                ("⏰", "Classes", subject["total_classes"]),
            ]

            def share_btn(subject_code=subject["subject_code"]):
                st.markdown("""
                    <style>
                        [class*="subject_share_button_"] button {
                            background-color: #ec4899 !important;
                            color: white !important;
                            border: none !important;
                            border-radius: 0.8rem !important;
                            padding: 0.55rem 1rem !important;
                            font-weight: 600 !important;
                        }

                        [class*="subject_share_button_"] button:hover {
                            background-color: #db2777 !important;
                        }
                    </style>
                """, unsafe_allow_html=True)
                with st.container(key=f"subject_share_button_{subject_code}"):
                    if st.button("Share code", key=f"share_{subject_code}"):
                        share_subject_dialog(subject['name'],subject['subject_code'])

            subject_card(
                name=subject["name"],
                code=subject["subject_code"],
                section=subject["section"],
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.info("no subject found, create one above")

def teacher_tab_attendance_record():
    st.header("attendance record")
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else 'N/A',
            "Subject" : r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present',False))
        })
    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group','Time',"Subject","Subject Code"]).agg(
            present_Count = ('is_present','sum'),
            Total_Count = ('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅" + summary['present_Count'].astype(str) + ' /'+ summary['Total_Count'].astype(str)+ " Students"
    )
    display_df = ( summary.sort_values('ts_group',ascending=False)
                [['Time','Subject',"Subject Code", "Attendance Stats"]])
    st.dataframe(display_df,width='stretch',hide_index=True)


def login_teacher(teacher_username,teacher_pass):
    if not teacher_username or not teacher_pass:
        return False
    teacher = teacher_login(teacher_username,teacher_pass)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_confirm_pass):
    if not teacher_username or not teacher_pass or not teacher_name or not teacher_confirm_pass:
        return False, "All fields are required"
    if check_teacher_exist(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_confirm_pass:
        return False, "password does not match"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True, "successfully create ! login now"
    except Exception:
        return False, "Unexpected error"


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
        if st.button("Login", width="stretch", key="teacher_login"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Login successfully 💐")
                import time 
                time.sleep(1)
                st.rerun()
            else:
                st.error("invalid userName")

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
        if st.button("Register", width="stretch", key="teacher_register_submit"):
            success,message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
                
    footer()
