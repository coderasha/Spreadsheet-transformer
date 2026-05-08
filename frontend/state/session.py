import streamlit as st
import pandas as pd


def init_session():

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    if "selected_sheet" not in st.session_state:
        st.session_state.selected_sheet = None