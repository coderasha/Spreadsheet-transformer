import streamlit as st


def render_sidebar(columns):
    st.sidebar.title("Transformations")

    selected_column = st.sidebar.selectbox(
        "Select Column",
        columns
    )

    operation = st.sidebar.selectbox(
        "Operation",
        [
            "Uppercase",
            "Lowercase",
            "Title Case",
            "Trim Spaces"
        ]
    )

    return selected_column, operation