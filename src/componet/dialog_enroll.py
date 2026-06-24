import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Enroll in Subject")
def enroll_dialog(student):
    st.write("Enter the subject code provided by your teacher to enroll")
    join_code = st.text_input("Subject Code", placeholder='Eg. CES101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            # Get the subject from code
            response = supabase.table('subject').select('subject_id, subject_name, subject_code').eq('subject_code', join_code).execute()

            if response.data:
                subject = response.data[0]
                student_id = student['student_id']

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

                if check.data:
                    st.warning("You are already in this course")
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success("Subject Enrolled Successfully")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("This course is not being offered or Invalid code!")
        else:
            st.warning("Please enter subject code")