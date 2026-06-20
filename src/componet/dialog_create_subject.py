import streamlit as st
from src.database.db import create_subject

@st.dialog("Add new Course")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of your course")
    course_id = st.text_input("Course Code", placeholder="CSE343")
    course_name = st.text_input("Course Name", placeholder="Machine Learning")
    course_section = st.text_input("Course Section", placeholder="A")

    if st.button("Create subject", type='primary', width='stretch'):
        if course_id and course_name and course_name:
            try:
                create_subject(teacher_id, course_id, course_name, course_section)
                st.toast("Subject Created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

        else:
            st.warning("Please fill all the details!")

    