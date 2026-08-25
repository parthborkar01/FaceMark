import streamlit as st
from src.components.header import header_dashBoard
from src.components.footer import footer
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embedding,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject
import time
from src.components.header import student_header_dashBoard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
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
    student_header_dashBoard()
    st.markdown("""
            <div style="
                width: 100%;
                height: 2px;
                margin: 0.75rem 0 1rem 0;
                background-color: #a6a2a4;
            "></div>
    """, unsafe_allow_html=True)

    # st.markdown("""
    #         <style>
    #             .st-key-create_subject button {
    #                 background-color: #ec4899 !important;
    #                 color: white !important;
    #                 border: none !important;
    #                 border-radius: 0.8rem !important;
    #                 padding: 0.55rem 1rem !important;
    #                 font-size: 1rem !important;
    #                 font-weight: 600 !important;
    #                 transition: background-color 0.2s ease, transform 0.2s ease !important;
    #             }
    
    #             .st-key-create_subject button:hover {
    #                 background-color: #db2777 !important;
    #                 transform: translateY(-2px) !important;
    #             }
    #         </style>
    # """, unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.header("Your enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject",width='stretch'):
            enroll_dialog()

    st.markdown("""
                <div style="
                    width: 100%;
                    height: 2px;
                    margin: 0.75rem 0 1rem 0;
                    background-color: #a6a2a4;
                "></div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading your enrolled subjects"):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sub_id = log['subject_id']
        if sub_id not in stats_map:
            stats_map[sub_id] = {"total":0,"attended":0}
        stats_map[sub_id]['total'] += 1
        if log.get('is_present'):
            stats_map[sub_id]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub_node['subject_id']
        stats = stats_map.get(sid,{"total":0,"attended":0})

        def unenroll_button():
            # button style 
            if st.button("Unenroll from this course",width='stretch'):
                unenroll_student_to_subject(student_id,sid)
                st.toast(f'Unenrolled from {sid} successfully')
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('🗓️','Total',stats['total']),
                    ('✅','Attended',stats['attended'])
                ],
                footer_callback = unenroll_button
            )
    footer()

def student_screen():
    if 'student_data' in st.session_state:
        student_dashboard()
        return
    show_registration = False
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
            [data-testid="stCameraInput"] button {
                background-color: #3b82f6 !important;
                color: white !important;
                border: none !important;
                border-radius: 0.8rem !important;
                padding: 0.65rem 1.25rem !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                transition: background-color 0.2s ease, transform 0.2s ease !important;
            }

            [data-testid="stCameraInput"] button:hover {
                background-color: #2563eb !important;
                transform: translateY(-2px) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.header("login using faceId", text_alignment='center')
    st.space()
    photo_source = st.camera_input("Position your face to center")
    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning ..."):
            detected_student,all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("face not found")
            elif num_faces > 1:
                st.warning("Multiple faces found")
            else:
                if detected_student:
                    studet_id = list(detected_student.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == studet_id),None)

                    if student:
                        st.session_state.is_loged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else: 
                    st.info("Face not recognized! you might be a new student")
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name = st.text_input("Enter your name ",placeholder="E.g Jiya Borekar")

            st.subheader("Optional : Voice enrolment")
            st.info("Enroll your voice")
            audio_data = None
            try:
                audio_data = st.audio_input("Rcord a short phrase like I am present,My name is Jiya")
            except Exception:
                st.error("Audio data failed")

            if st.button("create button"):
                if new_name:
                    with st.spinner("adding student info.."):
                        img = np.array(Image.open(photo_source))
                        embedding = get_face_embedding(img)
                        if embedding:
                            face_emb = embedding[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_loged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created Hi {new_name}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("can not recognised your face ")                    



                else:
                    st.warning("please enter your name")
    footer()