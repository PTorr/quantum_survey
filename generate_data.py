import numpy as np

def main():
    n = 5
    data_generator(n)

def data_generator(n):
    '''Generating artificial data.
       n - Number of probabilities/ questions.
       a - Vector of probabilities.
       Return: data - An array with all the probabilities for selected qbits.'''

    data = np.empty([np.power(n,3), 6])

    # the probabilities values for the array
    a = np.linspace(0,1,n)

    # qbits
    data[:,0:2] = [1,2]

    # Question type
    data[:,5] = 1

    # Filling the data array
    row = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                data[row, 2] = a[i]
                data[row, 3] = a[j]
                data[row, 4] = a[k]
                row += 1

    # data2 = np.around(data,3)
    # print np.matrix(data2)
    # print data
    return data

if __name__ == '__main__':
    main()
