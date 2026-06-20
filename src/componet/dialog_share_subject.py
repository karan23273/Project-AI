import streamlit as st
import segno # for QR
import io # for binary data 

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501/"
    join_url = f"{app_domain}/?join-code={subject_code}"
    
    QR = segno.make(join_url)
    out = io.BytesIO()
    QR.save(out, kind='png', scale=10, border=1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language='text')
        st.code(subject_code, language='text')
        st.info("Copy this link to share with your classmate")

    with col2:
        st.markdown("### Scan to join")
        st.image(out.getvalue(), caption='QRCODE for class link')

    