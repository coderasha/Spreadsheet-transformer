import streamlit as st
import pandas as pd

from io import BytesIO


def render_export_page():

    st.title("Export Spreadsheet")

    if not st.session_state.uploaded:
        st.warning("Upload a file first")
        return

    df = st.session_state.df

    # Remove AG Grid internal columns
    df = df.loc[
        :,
        ~df.columns.astype(str).str.startswith("::")
    ]

    st.subheader("Select Export Format")

    export_format = st.radio(
        "Export Type",
        ["Excel (.xlsx)", "CSV (.csv)"]
    )

    # =========================================================
    # EXCEL EXPORT
    # =========================================================

    if export_format == "Excel (.xlsx)":

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name="transformed.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            )
        )

    # =========================================================
    # CSV EXPORT
    # =========================================================

    elif export_format == "CSV (.csv)":

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download CSV File",
            data=csv_data,
            file_name="transformed.csv",
            mime="text/csv"
        )