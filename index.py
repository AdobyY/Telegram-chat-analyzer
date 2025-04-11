import streamlit as st
from streamlit_option_menu import option_menu

from pages.main import *


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Main"],
        icons=["house"]
    )
    

if selected == "Main":
    show_main_page()
      
