import streamlit as st


def init_session():
    if "df" not in st.session_state:
        st.session_state.df = None