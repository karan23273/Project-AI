import streamlit as st
import pathlib
import base64

def style_base_layout():
    st.markdown("""
        <style>
            .stApp{
            background: #CB2957 !important
        }
            .stApp div[data-testid="stColumn"]{
                background-color: #DDDDDD !important;
                padding: 1.5rem !important;
                border-radius: 1.5rem !important;
            }
        </style>

    """, unsafe_allow_html=True)

def style_font():
    font_path = "src/assets/Game of Thrones.ttf"
    font_bytes = pathlib.Path(font_path).read_bytes()
    font_base64 = base64.b64encode(font_bytes).decode()
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&display=swap'); /* Black Ops One */
        @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Chelsea+Market&display=swap'); /* Chelsea Market */


        @font-face{
            font-family:'My font';
            src: url(data:font/ttf;base64,"""+ font_base64+""") format('truetype');
            font-weight: normal;
            font-style: normal;
        }
        h1{
            font-family: 'Black Ops One', sans-serif !important;
            font-size: 4.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }
        h2{
            font-family: 'My font', sans-serif !important;
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }
        h3,h4,p{
            font-family: 'Chelsea Market', sans-serif !important;
        }
        
        button[kind='primary']{
            border-radius: 12px !important;
            background: #E05454 !important;
            color: Black !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.2rem !important;
            transition: all 0.2s ease !important;
            border: 0px !important;
        }
        button[kind='secondary']{
            border-radius: 12px !important;
            background: transparent !important;
            color: Black !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.2rem !important;
            transition: all 0.2s ease !important;
            border: 0px !important;
        }
        button[kind='tertiary']{
            border-radius: 12px !important;
            background: #FFE3E3 !important;
            color: Black !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.2rem !important;
            transition: all 0.2s ease !important;
            border: 0px !important;
        }
        button:hover {
            background: #FFAE6E !important;
            transform: scale(1.03) !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18) !important;
            transition: all 0.2s ease !important;
        }
        button:active {
            transform: scale(0.98) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.1s ease !important;
        }

        
    </style>
    """, unsafe_allow_html=True)

def style_hide():
    st.markdown("""
        <style>
            #MainMenu, footer,header{
                visibility:hidden    
            }
            .block-container{
                padding-top: 1.5rem !important    
            }
        </style>

    """, unsafe_allow_html=True)