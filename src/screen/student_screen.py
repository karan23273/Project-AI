import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_font,style_hide
from src.componet.header import header_dashboard

from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import get_all_students, create_student, get_student_attendance, get_student_subjects, unenroll_student_from_subject
import time
from src.componet.dialog_enroll import enroll_dialog
from src.componet.subject_card import subject_card

def student_screen():
    style_background_dashboard()
    style_font() 
    style_hide() 
    
    if 'student_data' in st.session_state:
        student_dashboard()
        return
    show_registration = False

    c1,c4 = st.columns([3,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    with c4:
        if st.button('Back', type='tertiary', key='back-login', width='stretch'):
            st.session_state['login-type'] = None
            st.rerun()
    with c1:
        header_dashboard()
    
    
    st.markdown(f"""
        <h3 style= "font-size:25px; text-align:center">Login using face ID</h3>
    """, unsafe_allow_html=True)
    photo_source = st.camera_input("Keep your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        # more like loading circle
        with st.spinner('AI is scanning...'):
            # Right now we are logging in
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not Found!')
            elif num_faces > 1:
                st.warning('Multiple Faces Found!')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    
                    student = None
                    for s in all_students:
                        if s['student_id'] == student_id:
                            student = s
                            break
                        
                    if student:
                        st.session_state.isLogin = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['student_name']}")
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info('Face not recognised! You migh be a new student!')
                    show_registration = True

        if show_registration:
            with st.container(border = True):
                st.markdown(f"""
                    <h3 style= "font-size:25px; text-align:center">Register new Profile</h3>
                """, unsafe_allow_html=True)
                user_name = st.text_input('Enter user name', placeholder='John@Doe')
                new_name = st.text_input('Enter your name', placeholder='John Doe')
                st.subheader('Optional: Voice Enrollment')
                st.info("Enroll for voice only attendance")

                audio_data = None
                try:
                    audio_data = st.audio_input('Record your audio: Hello Sir, I am present')
                except Exception:
                    st.error('Audio Data Failed!')

                if st.button('Create Account', type='primary'):
                    if new_name and user_name:
                        with st.spinner('Creating profile...'):
                            img = np.array(Image.open(photo_source))
                            encodings = get_face_embeddings(img)

                            if encodings:
                                face_emb = encodings[0].tolist()

                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embeddings(audio_data.read())

                                response_data = create_student(new_name, user_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                # New data found need to retrain
                                if response_data:
                                    train_classifier()
                                    st.session_state.isLogin = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0] 
                                    st.toast(f"Profile created!, {new_name}")
                                    time.sleep(1)
                                    st.rerun()

                            else:
                                st.error("Could'nt capture your facial features, Please retry!")


                    else:
                        st.warning('Name and user name field are mandatory!')


#########################################################STUDENT DASHBOARD##############################
            
                     
def student_dashboard():
    student = st.session_state.student_data

    c1, c2, c3 = st.columns([1, 2, 1], gap='xxlarge', vertical_alignment='center', width='stretch')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
        f"""
            <h1 style="font-size:25px; text-align:center; white-space:nowrap; margin:0;">
            Welcome, {student['student_name']}
            </h1>
        """, unsafe_allow_html=True)
        
    with c3:
        if st.button('Logout', type='secondary', key='log_out', width='stretch'):
            st.session_state['isLogin'] = False
            del st.session_state.student_data
            st.rerun()
    st.space()
    st.space()
    st.space()
    col1,col2 = st.columns([2,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    with col1:
        st.markdown(f"""<h3 style= "font-size:30px; text-align:center, width:content;">Your Enrolled Subjects</h3>""", unsafe_allow_html=True)
    with col2:
        if st.button('Enroll in subject', key='enroll', width='stretch'):
            enroll_dialog(student)

    with st.spinner("Fetching your courses"):
        subjects = get_student_subjects(student)
        logs = get_student_attendance(student)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        # This comes first tym
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        # Increase number of classes
        stats_map[sid]['total']+=1
        #  Increase attendance
        if log.get('is_present'):
            stats_map[sid]['attended']+=1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subject']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total":0, "attended":0}) #get with a fallback
        def unenroll_btn():
            if st.button("Unenroll from the course", key=f"unenroll_{sid}", type='tertiary', width='stretch'):
                unenroll_student_from_subject(student['student_id'], sid)
                st.toast("Unenroll successfully")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name= sub['subject_name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended'])
                ],
                footer_callback=unenroll_btn
            )
