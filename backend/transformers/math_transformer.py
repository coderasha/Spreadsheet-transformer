
def add_columns(df, col1, col2, output_col):
    df[output_col] = df[col1] + df[col2]
    return df


def subtract_columns(df, col1, col2, output_col):
    df[output_col] = df[col1] - df[col2]
    return df


def multiply_columns(df, col1, col2, output_col):
    df[output_col] = df[col1] * df[col2]
    return df