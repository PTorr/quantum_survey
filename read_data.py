def main():
    # fpath = 'D:\Users\Torr\PycharmProjects\quantum_survey/test_data.xlsx'
    fpath1 = 'test_data.csv'
    d = read_data(fpath1)
    print d


def read_data(file_path):
    '''Reads the data from csv file and transform it into an array called data.
    input: file_path - the full path of the csv file we want to read in format of
            [qbit1, qbit2, p(qb1=1), p(qb2=1),p(qb1=1 & qb2 = 1), fallacy type]
    output: array in the same format'''
    from xlrd import open_workbook
    import numpy as np
    import os

    filename, file_extension = os.path.splitext(file_path)
    if file_extension == '.xlsx':
        # reading the excel file
        wb = open_workbook(file_path)
        for sheet in wb.sheets():
            # transforming the data in the file into an array
            data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(1,sheet.nrows)]
            data = np.array(data)

    elif file_extension == '.csv':
        # reading csv file
        data = np.genfromtxt(file_path,delimiter=',')
        # data = data[~np.isnan(data)]
        data = data[1:len(data),:]

    return data

if __name__ == '__main__':
    main()
