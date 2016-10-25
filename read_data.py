def read_data(file_path):
    # Reads the data from csv file and transform it into an array called data.
    from xlrd import open_workbook
    import numpy as np

    # reading the excel file
    wb = open_workbook('D:/Clouds/OneDrive/University/Lab/quantom_cognition/phyton/test_data.xlsx')
    # wb = open_workbook(file_path)

    for sheet in wb.sheets():
        # number_of_rows = sheet.nrows
        # number_of_columns = sheet.ncols

        # transforming the data in the file into an array
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(1,sheet.nrows)]
        data = np.array(data)
    return data
