import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Share Class Link")
def auto_enroll_dialog(join_code):
    student_id = st.session_state.student_data['student_id']

    res = supabase.table('subject').select('subject_id, subject_name').eq('subject_code', join_code).execute()

    if not res.data:
        st.error('Subject code not found')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return
    
    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

    if check.data:
        st.info("You're already enrolled in this course")

        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"""<h3 style= "font-size:30px; text-align:center, width:content;">Would you like to enroll in {subject['subject_name']} ?</h3>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button('Enroll Now!', type='tertiary', width='stretch'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success("Joined successfully")
            st.query_params.clear()
            time.sleep(1)
            st.rerun()


    