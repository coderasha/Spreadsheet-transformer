from backend.exporters.excel_exporter import export_excel


def export_dataframe(df, output_path):
    export_excel(df, output_path)