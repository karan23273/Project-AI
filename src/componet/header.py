import streamlit as st
import pathlib
import base64

def header():
    logo_bytes = pathlib.Path('src/assets/attendance.png').read_bytes()
    logo_b64 = base64.b64encode(logo_bytes).decode()

    st.markdown(
        f"""
        <div style = 'display:flex; flex-direction: column; align-items:center; justify-content:center'>
            <img src="data:image/png;base64,{logo_b64}" style = 'height: 150px;'margin:0px;'/>
            <h1 style = 'text-align:center; color:#DDDDDD '>Ease IN</h1>
        </div>
    """, unsafe_allow_html=True)