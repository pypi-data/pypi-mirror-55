from os.path import join, dirname, realpath
import xlrd, openpyxl


def new_excel(file_name: str, file_path: str = None, sheet_name: str = None) -> None:
    if (not file_name.endswith('.xls')) and (not file_name.endswith('.xlsx')):
        raise ValueError('file_name should end with .xls or .xlsx')

    book = openpyxl.Workbook()
    book.create_sheet(title=sheet_name, index=0)

    path = file_path if file_path else dirname(realpath(__file__))
    excel_path = join(path, file_name)
    book.save(excel_path)


def iter_excel_by_row(file_name: str, file_path: str = None, sheet_index: int = 0) -> list:
    path = file_path if file_path else dirname(realpath(__file__))
    excel_path = join(path, file_name)
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(sheet_index)

    for i in range(sheet.nrows):
        yield sheet.row_values(i)
