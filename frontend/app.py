import streamlit as st
from frontend.pages.upload import render_upload_page
from frontend.pages.transform import render_transform_page
from frontend.pages.formatting import render_formatting_page
from frontend.pages.export import render_export_page

st.set_page_config(
    page_title="Spreadsheet Transformer",
    layout="wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Upload",
        "Transform",
        "Formatting",
        "Export"
    ]
)

if page == "Upload":
    render_upload_page()

elif page == "Transform":
    render_transform_page()

elif page == "Formatting":
    render_formatting_page()

elif page == "Export":
    render_export_page()