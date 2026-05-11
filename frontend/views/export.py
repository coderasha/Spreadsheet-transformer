import streamlit as st
import pandas as pd

from io import BytesIO


def render_export_page():

    st.title("Export Workbook")

    if not st.session_state.uploaded:
        st.warning("Upload a workbook first")
        return

    export_scope = st.radio(
        "Export Scope",
        [
            "Current Worksheet",
            "Selected Worksheets",
            "Entire Workbook"
        ]
    )

    current_sheet = st.session_state.current_sheet

    selected_sheets = []

    if export_scope == "Selected Worksheets":

        selected_sheets = st.multiselect(
            "Choose Worksheets",
            st.session_state.sheet_names,
            default=[current_sheet]
        )

    export_format = st.radio(
        "Export Format",
        [
            "Excel (.xlsx)",
            "CSV (.csv)"
        ]
    )

    # CURRENT WORKSHEET
    if export_scope == "Current Worksheet":

        df = st.session_state.workbook[current_sheet]

        if export_format == "CSV (.csv)":

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{current_sheet}.csv",
                mime="text/csv"
            )

        else:

            output = BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    sheet_name=current_sheet,
                    index=False
                )

            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name=f"{current_sheet}.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument"
                    ".spreadsheetml.sheet"
                )
            )

    # MULTIPLE / ALL WORKSHEETS
    else:

        if export_scope == "Selected Worksheets":
            sheets_to_export = selected_sheets
        else:
            sheets_to_export = st.session_state.sheet_names

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            for sheet in sheets_to_export:

                df = st.session_state.workbook[sheet]

                df.to_excel(
                    writer,
                    sheet_name=sheet,
                    index=False
                )

        st.download_button(
            label="Download Workbook",
            data=output.getvalue(),
            file_name="transformed_workbook.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            )
        )