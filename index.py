import streamlit as st
from streamlit_option_menu import option_menu

from pages.main import *

st.set_page_config(
    page_title="Telegram Chat Analyzer",
    page_icon="📈",
    layout="wide",
)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Main"],
        icons=["house"]
    )
    

if selected == "Main":
    show_main_page()
      
