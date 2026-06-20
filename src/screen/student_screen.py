import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_font,style_hide
from src.componet.header import header_dashboard

from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import get_all_students, create_student
import time

def student_dashboard():
    st.header("Student dashboard")

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
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['student_user_name']}")
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
                new_name = st.text_input('Enter username', placeholder='JohnDoe@iiitd')
                st.subheader('Optional: Voice Enrollment')
                st.info("Enroll for voice only attendance")

                audio_data = None
                try:
                    audio_data = st.audio_input('Record your audio: Hello Sir, I am present')
                except Exception as e:
                    print(e.with_traceback())
                    st.error('Audio Data Failed!')

                if st.button('Create Account', type='primary'):
                    if new_name:
                        with st.spinner('Creating profile...'):
                            img = np.array(Image.open(photo_source))
                            encodings = get_face_embeddings(img)

                            if encodings:
                                face_emb = encodings[0].tolist()

                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embeddings(audio_data.read())

                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                # New data found need to retrain
                                if response_data:
                                    student = response_data[0]
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = student
                                    st.toast(f"Profile created!, {student['student_user_name']}")
                                    time.sleep(1)
                                    st.rerun()

                            else:
                                st.error("Could'nt capture your facial features, Please retry!")


                    else:
                        st.warning('Please enter your name!')


                

                     