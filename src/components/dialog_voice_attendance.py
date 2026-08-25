import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_aviod
from src.database.db import supabase
from src.components.dialog_attendance_result import show_attendance_result
from datetime import datetime
import pandas as pd
@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of student saying I am present.., the AI will recognize")
    audio_data = False
    audio_data  = st.audio_input("recorde calssroom audion")
    if 'voice_attendance_result' not in st.session_state:
        st.session_state.voice_attendance_result = None
    if st.button("Analyze audio", width='stretch',type='primary'):
        with st.spinner("Processing audio data"):
            enrolled_res = supabase.table("subject_students").select("*, students(*)").eq('subject_id',selected_subject_id).execute()
            enrolled_students = enrolled_res.data
            if not enrolled_students:
                st.warning("No students are enrolled now")
                return
            
            cadidates_dict = {
                s['students']['student_id']: s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not cadidates_dict:
                st.error("No enrolled student have voice profile is registed")
                return 

            if audio_data is None:
                st.warning("Please record class voice first.")
                return
            
            audio_bytes = audio_data.read()
            detected_scores = process_bulk_aviod(audio_bytes,cadidates_dict)

            result,attendance_to_log = [],[]
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'],0.0)
                is_present = bool(score > 0)
            
                result.append({
                    "Name" : student['name'],
                    'ID': student['student_id'],
                    "source" : score if is_present else 0 ,
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })
                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })
            st.session_state.voice_attendance_result = (pd.DataFrame(result),attendance_to_log)
    if st.session_state.voice_attendance_result:
        st.divider()
        df_results,logs = st.session_state.voice_attendance_result
        show_attendance_result(df_results,logs)