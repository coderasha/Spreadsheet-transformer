import streamlit as st
import pandas as pd

from natsort import index_natsorted

from components.grid import render_grid


def render_transform_page():

    st.title("Transform Workbook")

    # =========================================================
    # CHECK UPLOAD
    # =========================================================

    if not st.session_state.uploaded:
        st.warning("Please upload a workbook first")
        return

    # =========================================================
    # SELECT WORKSHEET
    # =========================================================

    selected_sheet = st.selectbox(
        "Select Worksheet",
        st.session_state.sheet_names,
        index=st.session_state.sheet_names.index(
            st.session_state.current_sheet
        )
    )

    st.session_state.current_sheet = selected_sheet

    df = st.session_state.workbook[selected_sheet]

    # Remove AG Grid internal columns
    df = df.loc[
        :,
        ~df.columns.astype(str).str.startswith("::")
    ]

    st.session_state.workbook[selected_sheet] = df

    valid_columns = list(df.columns)

    # =========================================================
    # APPLY SCOPE
    # =========================================================

    st.subheader("Apply Changes To")

    apply_scope = st.radio(
        "Transformation Scope",
        [
            "Current Worksheet",
            "Selected Worksheets",
            "All Worksheets"
        ]
    )

    selected_sheets = []

    if apply_scope == "Selected Worksheets":

        selected_sheets = st.multiselect(
            "Choose Worksheets",
            st.session_state.sheet_names,
            default=[selected_sheet]
        )

    # =========================================================
    # EDITABLE GRID
    # =========================================================

    st.subheader(
        f"Editing Worksheet: {selected_sheet}"
    )

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

        if apply_scope == "Current Worksheet":
            target_sheets = [selected_sheet]

        elif apply_scope == "Selected Worksheets":
            target_sheets = selected_sheets

        else:
            target_sheets = st.session_state.sheet_names

        for sheet in target_sheets:

            sheet_df = st.session_state.workbook[sheet]

            if column not in sheet_df.columns:
                continue

            if operation == "UPPERCASE":

                sheet_df[column] = (
                    sheet_df[column]
                    .astype(str)
                    .str.upper()
                )

            elif operation == "lowercase":

                sheet_df[column] = (
                    sheet_df[column]
                    .astype(str)
                    .str.lower()
                )

            elif operation == "Title Case":

                sheet_df[column] = (
                    sheet_df[column]
                    .astype(str)
                    .str.title()
                )

            elif operation == "Trim Spaces":

                sheet_df[column] = (
                    sheet_df[column]
                    .astype(str)
                    .str.strip()
                )

            st.session_state.workbook[sheet] = sheet_df

        st.success(
            "Transformation Applied Successfully"
        )

        st.rerun()

    st.divider()

    # =========================================================
    # REARRANGE COLUMNS & RENAME HEADERS
    # =========================================================

    st.subheader(
        "Rearrange Columns & Rename Headers"
    )

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

        column_config = sorted(
            column_config,
            key=lambda x: x["serial"]
        )

        ordered_columns = [
            item["old_name"]
            for item in column_config
        ]

        rename_mapping = {
            item["old_name"]: item["new_name"]
            for item in column_config
        }

        if apply_scope == "Current Worksheet":
            target_sheets = [selected_sheet]

        elif apply_scope == "Selected Worksheets":
            target_sheets = selected_sheets

        else:
            target_sheets = st.session_state.sheet_names

        for sheet in target_sheets:

            sheet_df = st.session_state.workbook[sheet]

            valid_sheet_columns = [
                col for col in ordered_columns
                if col in sheet_df.columns
            ]

            updated_df = (
                sheet_df[valid_sheet_columns]
            )

            applicable_rename_mapping = {
                k: v
                for k, v in rename_mapping.items()
                if k in updated_df.columns
            }

            updated_df = updated_df.rename(
                columns=applicable_rename_mapping
            )

            st.session_state.workbook[sheet] = (
                updated_df
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
            df[sort_column].astype(str)
        )

        if not ascending:
            sorted_index = list(reversed(sorted_index))

        updated_df = (
            df.iloc[sorted_index]
            .reset_index(drop=True)
        )

        st.session_state.workbook[
            selected_sheet
        ] = updated_df

        st.success("Rows Sorted Successfully")

        st.rerun()

    st.divider()

    # =========================================================
    # MERGE WORKSHEETS
    # =========================================================

    st.subheader("Merge Worksheets")

    merge_scope = st.radio(
        "Merge Scope",
        [
            "Selected Worksheets",
            "All Worksheets"
        ],
        key="merge_scope"
    )

    merge_sheets = []

    if merge_scope == "Selected Worksheets":

        merge_sheets = st.multiselect(
            "Select Worksheets To Merge",
            st.session_state.sheet_names,
            default=st.session_state.sheet_names
        )

    else:

        merge_sheets = st.session_state.sheet_names

    merged_sheet_name = st.text_input(
        "New Merged Worksheet Name",
        value="Final_Merged_Sheet"
    )

    if st.button("Merge Worksheets"):

        valid_dfs = []

        for sheet in merge_sheets:

            sheet_df = st.session_state.workbook[sheet]

            # Remove AG Grid internal columns
            sheet_df = sheet_df.loc[
                :,
                ~sheet_df.columns.astype(str)
                .str.startswith("::")
            ]

            valid_dfs.append(sheet_df)

        if len(valid_dfs) == 0:

            st.error("No worksheets selected")

        else:

            merged_df = pd.concat(
                valid_dfs,
                ignore_index=True
            )

            st.session_state.workbook[
                merged_sheet_name
            ] = merged_df

            if merged_sheet_name not in (
                st.session_state.sheet_names
            ):

                st.session_state.sheet_names.append(
                    merged_sheet_name
                )

            st.session_state.current_sheet = (
                merged_sheet_name
            )

            st.success(
                f"Worksheets merged into "
                f"'{merged_sheet_name}' successfully"
            )

            st.rerun()

    st.divider()

    # =========================================================
    # CURRENT WORKSHEET PREVIEW
    # =========================================================

    st.subheader("Current Worksheet Preview")

    st.dataframe(
        st.session_state.workbook[selected_sheet],
        use_container_width=True
    )