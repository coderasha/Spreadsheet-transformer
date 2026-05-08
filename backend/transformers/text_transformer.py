
def uppercase_column(df, column_name):
    df[column_name] = df[column_name].astype(str).str.upper()
    return df


def lowercase_column(df, column_name):
    df[column_name] = df[column_name].astype(str).str.lower()
    return df


def titlecase_column(df, column_name):
    df[column_name] = df[column_name].astype(str).str.title()
    return df


def trim_spaces(df, column_name):
    df[column_name] = df[column_name].astype(str).str.strip()
    return df