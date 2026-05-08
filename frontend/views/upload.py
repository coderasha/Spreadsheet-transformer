import streamlit as st
import pandas as pd


def render_upload_page():

    st.title("Upload Spreadsheet Workbook")

    uploaded_file = st.file_uploader(
        "Upload XLSX/XLS/CSV",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file:

        # CSV Handling
        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            st.session_state.df = df
            st.session_state.uploaded = True

            st.success("CSV Uploaded Successfully")

            st.dataframe(df)

            return

        # Excel Workbook Handling
        excel_file = pd.ExcelFile(uploaded_file)

        sheet_names = excel_file.sheet_names

        st.subheader("Select Worksheet")

        selected_sheet = st.selectbox(
            "Available Sheets",
            sheet_names
        )

        if st.button("Load Selected Sheet"):

            df = pd.read_excel(
                uploaded_file,
                sheet_name=selected_sheet
            )

            st.session_state.df = df
            st.session_state.uploaded = True
            st.session_state.selected_sheet = selected_sheet

            st.success(
                f"Sheet '{selected_sheet}' Loaded Successfully"
            )

            st.dataframe(df)