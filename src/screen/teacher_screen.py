import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_font,style_hide
from src.componet.header import header_dashboard
from src.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subject
import time
from src.componet.dialog_create_subject import create_subject_dialog
from src.componet.subject_card import subject_card
from src.componet.dialog_share_subject import share_subject_dialog

def teacher_screen():
    style_background_dashboard()
    style_font() 
    style_hide() 
    
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()



######################################################## LOGIN #########################################################################
def login_teacher(teacher_user_name, teacher_user_pass):
    if not teacher_user_name or not teacher_user_pass:
        return False
        
    teacher = teacher_login(teacher_user_name, teacher_user_pass)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.isLogin = True
        return True
    return False

def teacher_screen_login():
    c1,c4 = st.columns([3,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    with c4:
        if st.button('Back', type='tertiary', key='back-login', width='stretch'):
            st.session_state['login-type'] = None
            st.rerun()
    with c1:
        header_dashboard()


    st.markdown(f"""<h3 style="font-size:25px; text-align:center; margin:0;">Login using password</h3>""", unsafe_allow_html=True)

    # input
    teacher_user_name = st.text_input('Enter your user name', placeholder='JohnDoe@iiitd')
    teacher_user_pass = st.text_input('Enter your password', type='password', placeholder='Password')
    st.divider()

    button1, button2 = st.columns([3,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    
    login_success = -1
    with button2:
        if(st.button('Login', type='primary', key='login', width='stretch')):
            if login_teacher(teacher_user_name, teacher_user_pass):
                login_success = 1
            else:
                login_success = 0

    if login_success == 1:
        st.toast("Welcome, Sir", icon='🔥')
        time.sleep(0.5)
        st.rerun()
    elif login_success == 0:
        st.error("Username or Password is incorrect!")



    with button1:
        if(st.button('Register Instead', type='primary', key='register-instead', width='content')):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()

####################################################### REGISTER ###########################################################################

def register_teacher(teacher_user_name, teacher_name, teacher_user_pass, teacher_pass_confirm):
    if not teacher_name or not teacher_user_name or not teacher_user_pass or not teacher_pass_confirm:
        return False, "All fields are Mandatory"
    
    if check_teacher_exist(teacher_user_name):
        return False, "User already exist change username or try Login"

    if teacher_pass_confirm != teacher_user_pass:
        return False, "Password does not match"
    
    try:
        create_teacher(teacher_user_name, teacher_name, teacher_user_pass)
        return True, "Successfully Registered"
    except Exception as e:
        return False, "Unexpected Error"

def teacher_screen_register():
    c1,c4 = st.columns([3,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    with c4:
        if st.button('Back', type='tertiary', key='back-register', width='stretch'):
            st.session_state['login-type'] = None
            st.rerun()
    with c1:
        header_dashboard()
    
    
    st.markdown(f""" 
        <h3 style= "font-size:25px; text-align:center">Register your teacher profile</h3>   """, unsafe_allow_html=True)
    
    teacher_user_name = st.text_input('Enter username', placeholder='JohnDoe@iiitd')
    teacher_name = st.text_input('Enter name', placeholder='John Doe')
    teacher_user_pass = st.text_input('Enter your password', type='password', placeholder='Password')
    teacher_pass_confirm = st.text_input('Confirm password', type='password', placeholder='Password')
    st.divider()

    button1, button2 = st.columns([3,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    

    success = -1
    message = ""
    with button2:
        if(st.button('Register now', type='primary', key='register', width='stretch')):
            success, message = register_teacher(teacher_user_name, teacher_name, teacher_user_pass, teacher_pass_confirm)
    
    if success == 1:
        st.success(message)
        st.session_state.teacher_login_type = 'login'
        time.sleep(1.5)
        st.rerun()
    elif success == 0:
        st.error(message)


    with button1:
        if(st.button('Login Instead', type='primary', key='login-instead', width='content')):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()


################################################## TEACHER DASHBOARD ######################################################

def teacher_dashboard():
    teacher = st.session_state.teacher_data
    
    c1, c2, c3 = st.columns([1, 2, 1], gap='xxlarge', vertical_alignment='center', width='stretch')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
        f"""
            <h1 style="font-size:25px; text-align:center; white-space:nowrap; margin:0;">
            Welcome, {teacher['teacher_name']}
            </h1>
        """, unsafe_allow_html=True)
        
    with c3:
        if st.button('Logout', type='secondary', key='log_out', width='stretch'):
            st.session_state['isLogin'] = False
            del st.session_state.teacher_data
            st.rerun()
        

    st.space()
    st.space()
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3, gap='xxlarge')
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take attendance', type=type1, width='stretch'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subject' else "tertiary"
        if st.button('Manage subjects', type=type2, width='stretch'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_record' else "tertiary"
        if st.button('Attendance report', type=type3, width='stretch'):
            st.session_state.current_teacher_tab = 'attendance_record'
            st.rerun()

    st.divider()
    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == 'manage_subject':
        teacher_tab_manage_subject()
    else:
        teacher_tab_attendance_record()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1,col2 = st.columns([2,1], vertical_alignment='center', gap='xxlarge', width='stretch')
    with col1:
        st.markdown(f"""<h3 style= "font-size:30px; text-align:center, width:content;">Manage Subjects</h3>""", unsafe_allow_html=True)
    with col2:
        if st.button('Create new subject', width='stretch'):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👩🏻‍💻", "Students", sub['total_students']),
                ("👨🏻‍🏫", "Classes", sub['total_classes'])
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['subject_name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['subject_name'], sub['subject_code'])
                st.write("")

            subject_card(
                name = sub['subject_name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback = share_btn
            )
    else:
        st.info("NO SUBJECT FOUND!, CREATE ONE FIRST")
    
def teacher_tab_manage_subject():
    st.header("Manage subject")

def teacher_tab_attendance_record():
    st.header("Attendance report")
