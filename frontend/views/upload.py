import streamlit as st
import pandas as pd


def render_upload_page():

    st.title("Upload Spreadsheet Workbook")

    uploaded_file = st.file_uploader(
        "Upload XLSX/XLS/CSV",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file:

        # CSV FILE
        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            st.session_state.workbook = {
                "Sheet1": df
            }

            st.session_state.sheet_names = ["Sheet1"]

            st.session_state.current_sheet = "Sheet1"

            st.session_state.uploaded = True

            st.success("CSV Uploaded Successfully")

            st.dataframe(df)

            return

        # EXCEL WORKBOOK
        workbook = pd.read_excel(
            uploaded_file,
            sheet_name=None
        )

        st.session_state.workbook = workbook

        st.session_state.sheet_names = list(
            workbook.keys()
        )

        st.session_state.current_sheet = (
            st.session_state.sheet_names[0]
        )

        st.session_state.uploaded = True

        st.success("Workbook Uploaded Successfully")

        st.subheader("Available Worksheets")

        st.write(st.session_state.sheet_names)