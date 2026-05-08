from st_aggrid import AgGrid


def render_grid(df):
    AgGrid(
        df,
        editable=True,
        fit_columns_on_grid_load=True,
        height=500
    )