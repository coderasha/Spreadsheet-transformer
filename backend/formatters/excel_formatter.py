from openpyxl.styles import Font


def make_column_bold(ws, column_letter):
    for cell in ws[column_letter]:
        cell.font = Font(bold=True)