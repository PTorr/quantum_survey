from read_data import read_data
from constrained_optimization import main as co
from entanglement_check import entanglement_checker as ec
import numpy as np
import os

def main():
    table_path = 'D:/Clouds/OneDrive/University/Lab/quantom_cognition/phyton/test_data.xlsx'
    if os.path.exists(table_path)!=True:
        table_path = raw_input("The path is wrong \nEnter the full path of the data file: ")
        if os.path.exists(table_path) != True:
            print ('File not found')
            quit()

    data = read_data(table_path)
    # Compute the coefficients
    coeff_a = coefficients_calculator(data)
    # Checking if the qbits are entangled
    for i in range(len(coeff_a)):
        [ev, c, entangled] = ec(coeff_a[i][2:6])
        coeff_a[i][6] = entangled

    print np.matrix(coeff_a)



def coefficients_calculator(data):
    # compute the coefficients
    [nr, nc] = data.shape  # number of rows and columns in the array
    #          columns #            rows #
    ca = [[0 for x in range(nc+1)] for y in range(nr)]
    for i in range(nr):
        ca[i][0] = data[i,0] # qbit_01
        ca[i][1] = data[i,1] # qbit_02
        cp = data[i, 2:5] # coefficients probability from the data (from survey).
        irr = data[i,5]

        rx, rf = co(cp, irr)  # call the optimization function for the coefficients {a_ij}
        ca[i][2:6] = rx # inserting the optimized coefficients into my my array
    # ca = np.matrix(ca)
    return ca

if __name__ == '__main__':
    main()