import streamlit as st


def init_session():

    if "workbook" not in st.session_state:
        st.session_state.workbook = {}

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    if "current_sheet" not in st.session_state:
        st.session_state.current_sheet = None

    if "sheet_names" not in st.session_state:
        st.session_state.sheet_names = []