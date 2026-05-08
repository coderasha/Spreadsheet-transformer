from backend.transformers.text_transformer import uppercase_column


def apply_uppercase(df, column_name):
    return uppercase_column(df, column_name)