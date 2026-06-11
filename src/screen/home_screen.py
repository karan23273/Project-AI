import streamlit as st

def home_screen():
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.markdown(
            """
            <h3>I'm a Student</h2>
            <img src = 'https://i.ibb.co/844D9Lrt/mascot-student.png', style="width:130px; padding:0px 0px 0px 0px"/>
            
        """, unsafe_allow_html=True)
        if st.button('Login-as-Student', type="primary", key='1', width='stretch'):
            st.session_state['login-type'] = 'student'
            st.rerun()
    with col2:
        st.markdown(
            """
            <h3>I'm a Teacher</h2>
            <img src = 'https://i.ibb.co/CsmQQV6X/mascot-prof.png', style="width:160px; padding:0px 0px 1px 0px;"/>
            
        """, unsafe_allow_html=True)
        
        if st.button('Login-as-Teacher', type="primary", key='2', width='stretch'):
            st.session_state['login-type'] = 'teacher'
            st.rerun()

