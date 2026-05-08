import streamlit as st

from views.upload import render_upload_page
from views.transform import render_transform_page
from views.export import render_export_page

from state.session import init_session


st.set_page_config(
    page_title="Spreadsheet Transformer",
    layout="wide"
)

init_session()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Upload",
        "Transform",
        "Export"
    ]
)

if page == "Upload":
    render_upload_page()

elif page == "Transform":
    render_transform_page()

elif page == "Export":
    render_export_page()