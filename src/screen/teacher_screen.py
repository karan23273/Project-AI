import streamlit as st

def teacher_screen():
    st.header('I am a Teacher')
    if st.button('Back', type='tertiary', key='3'):
        st.session_state['login-type'] = None
        st.rerun()