def export_excel(df, output_path):
    df.to_excel(output_path, index=False)