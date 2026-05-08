import streamlit as st
from frontend.utils.api import upload_file


def render_upload_page():
    st.title("Upload Spreadsheet")

    uploaded_file = st.file_uploader(
        "Upload XLSX/XLS/CSV",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file:
        response = upload_file(uploaded_file)

        st.write(response)