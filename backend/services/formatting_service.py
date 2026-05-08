from openpyxl import load_workbook
from backend.formatters.excel_formatter import make_column_bold


def apply_bold_format(file_path, column_letter):
    wb = load_workbook(file_path)
    ws = wb.active

    make_column_bold(ws, column_letter)

    wb.save(file_path)