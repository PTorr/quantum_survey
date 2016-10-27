def read_data(file_path):
    # Reads the data from csv file and transform it into an array called data.
    from xlrd import open_workbook
    import numpy as np

    # reading the excel file
    wb = open_workbook(file_path)

    for sheet in wb.sheets():
        # transforming the data in the file into an array
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(1,sheet.nrows)]
        data = np.array(data)
    return data
