from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode
)

import streamlit as st


def render_grid():

    current_sheet = st.session_state.current_sheet

    df = st.session_state.workbook[
        current_sheet
    ].copy()

    # Remove AG Grid internal columns
    df = df.loc[
        :,
        ~df.columns.astype(str).str.startswith("::")
    ]

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        editable=True,
        resizable=True,
        sortable=True,
        filter=True
    )

    gb.configure_grid_options(
        rowDragManaged=True,
        animateRows=True
    )

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        height=500
    )

    updated_df = grid_response["data"]

    updated_df = updated_df.loc[
        :,
        ~updated_df.columns.astype(str).str.startswith("::")
    ]

    st.session_state.workbook[
        current_sheet
    ] = updated_df