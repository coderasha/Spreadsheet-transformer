import streamlit as st
from natsort import index_natsorted

from components.grid import render_grid


def render_transform_page():

    st.title("Transform Data")

    if not st.session_state.uploaded:
        st.warning("Please upload a file first")
        return

    # =========================================================
    # CLEAN DATAFRAME
    # =========================================================

    df = st.session_state.df

    # Remove AG Grid internal columns
    df = df.loc[
        :,
        ~df.columns.astype(str).str.startswith("::")
    ]

    st.session_state.df = df

    valid_columns = list(df.columns)

    # =========================================================
    # EDITABLE GRID
    # =========================================================

    st.subheader("Editable Spreadsheet")

    render_grid()

    st.divider()

    # =========================================================
    # COLUMN TRANSFORMATIONS
    # =========================================================

    st.subheader("Column Transformations")

    column = st.selectbox(
        "Select Column",
        valid_columns
    )

    operation = st.selectbox(
        "Operation",
        [
            "UPPERCASE",
            "lowercase",
            "Title Case",
            "Trim Spaces"
        ]
    )

    if st.button("Apply Transformation"):

        if operation == "UPPERCASE":

            st.session_state.df[column] = (
                st.session_state.df[column]
                .astype(str)
                .str.upper()
            )

        elif operation == "lowercase":

            st.session_state.df[column] = (
                st.session_state.df[column]
                .astype(str)
                .str.lower()
            )

        elif operation == "Title Case":

            st.session_state.df[column] = (
                st.session_state.df[column]
                .astype(str)
                .str.title()
            )

        elif operation == "Trim Spaces":

            st.session_state.df[column] = (
                st.session_state.df[column]
                .astype(str)
                .str.strip()
            )

        st.success("Transformation Applied Successfully")

        st.rerun()

    st.divider()

    # =========================================================
    # REARRANGE COLUMNS & RENAME HEADERS
    # =========================================================

    st.subheader("Rearrange Columns & Rename Headers")

    column_config = []

    for idx, col in enumerate(valid_columns):

        col1, col2, col3 = st.columns([4, 2, 4])

        with col1:
            st.text_input(
                "Previous Column",
                value=col,
                disabled=True,
                key=f"old_{col}"
            )

        with col2:
            serial = st.number_input(
                "Serial No",
                min_value=1,
                value=idx + 1,
                step=1,
                key=f"serial_{col}"
            )

        with col3:
            new_name = st.text_input(
                "New Header Name",
                value=col,
                key=f"new_{col}"
            )

        column_config.append({
            "old_name": col,
            "serial": serial,
            "new_name": new_name
        })

    if st.button("Apply Column Changes"):

        # Sort by serial number
        column_config = sorted(
            column_config,
            key=lambda x: x["serial"]
        )

        # Ordered columns
        ordered_columns = [
            item["old_name"]
            for item in column_config
        ]

        # Keep only valid columns
        ordered_columns = [
            col for col in ordered_columns
            if col in st.session_state.df.columns
        ]

        # Rearrange dataframe
        st.session_state.df = (
            st.session_state.df[ordered_columns]
        )

        # Rename mapping
        rename_mapping = {
            item["old_name"]: item["new_name"]
            for item in column_config
        }

        # Rename headers
        st.session_state.df = (
            st.session_state.df.rename(
                columns=rename_mapping
            )
        )

        st.success(
            "Columns Rearranged & Renamed Successfully"
        )

        st.rerun()

    st.divider()

    # =========================================================
    # ROW SORTING
    # =========================================================

    st.subheader("Sort Rows")

    sort_column = st.selectbox(
        "Sort By",
        valid_columns,
        key="sort_column"
    )

    sort_order = st.radio(
        "Order",
        ["Ascending", "Descending"]
    )

    if st.button("Sort Data"):

        ascending = sort_order == "Ascending"

        sorted_index = index_natsorted(
            st.session_state.df[sort_column]
            .astype(str)
        )

        if not ascending:
            sorted_index = list(reversed(sorted_index))

        st.session_state.df = (
            st.session_state.df.iloc[sorted_index]
            .reset_index(drop=True)
        )

        st.success("Rows Sorted Successfully")

        st.rerun()

    st.divider()

    # =========================================================
    # DATA PREVIEW
    # =========================================================

    st.subheader("Current Data Preview")

    st.dataframe(
        st.session_state.df,
        use_container_width=True
    )