import streamlit as st

def student_screen():
    st.header('I am a Student')
    
    if st.button('Back', type='tertiary', key='3'):
        st.session_state['login-type'] = None
        st.rerun()