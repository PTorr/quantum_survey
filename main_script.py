from read_data import read_data
from constrained_optimization import main as co
from entanglement_check import entanglement_checker as ec
from generate_data import data_generator as dg
import numpy as np
import os
import matplotlib.pyplot as plt
import itertools


def main():
    # Calculating 2 qbits coefficients
    # [qbit1, qbit2, a00, a01, a10, a11, irr, irr_value, entangled, evc]       - evc = from the concurrence.
    table_path = 'D:/Clouds/OneDrive/University/Lab/quantom_cognition/phyton/test_data.xlsx'
    if os.path.exists(table_path) != True:
        table_path = raw_input("The path is wrong \nEnter the full path of the data file: ")
        if os.path.exists(table_path) != True:
            print ('File not found')
            quit()

    # data = read_data(table_path)
    data = dg(10)
    # Compute the coefficients
    coeff_a = coefficients_calculator(data)
    # print np.isnan(coeff_a).any()

    # Checking if the qbits are entangled
    ca_nc = len(coeff_a[0])
    for i in range(len(coeff_a)):
        [evc, c, entangled] = ec(coeff_a[i][2:6])
        coeff_a[i][ca_nc:ca_nc + 2] = [entangled, evc]

    # print np.matrix(coeff_a)
    # Saving the coefficients array to a csv file
    np.savetxt("2qbits_coefficients_summary.csv", coeff_a, delimiter=",")

    # This section plots the irrationality (irr_value) as function of the entanglement (evc)
    coeff_a1 = np.matrix(coeff_a)
    x = np.matrix(coeff_a1[:, 9])
    y = np.matrix(coeff_a1[:, 7])
    xx = np.real(x)
    yy = np.real(y)
    yy1 = yy[yy > 0]
    xx1 = xx[yy > 0]
    y1 = yy1[xx1 <= 0]
    x1 = xx1[xx1 <= 0]
    y2 = yy1[xx1 > 0]
    x2 = xx1[xx1 > 0]
    yy2 = yy[yy <= 0]
    xx2 = xx[yy <= 0]
    y3 = yy2[xx2 <= 0]
    x3 = xx2[xx2 <= 0]
    y4 = yy2[xx2 > 0]
    x4 = xx2[xx2 > 0]
    # plt.subplot(2,1,1)
    plt.plot(xx,yy,'bo',x1,y1,'ro',x2,y2,'go',x3,y3,'mo',x4,y4,'yo')
    plt.xlabel('Entanglement')
    plt.ylabel('Irrationality')
    # plt.subplot(2, 1, 2)
    # plt.scatter(x1,y1)
    # plt.xlabel('Entanglement')
    # plt.ylabel('Irrationality')
    plt.show()


    # fig, ax = plt.subplots()
    # ys = np.real(y)
    # threshold = 0
    # ax.plot(np.real(x),ys, linestyle='none', color='b', marker='o',)

    # greater_than_threshold = [i for i, val in enumerate(ys) if val > threshold]
    # ax.plot(greater_than_threshold, ys[greater_than_threshold],
    #         linestyle='none', color='r', marker='o')

    # plt.show()


def coefficients_calculator(data):
    # compute the coefficients
    [nr, nc] = data.shape  # number of rows and columns in the array
    #          columns #            rows #
    ca = [[0 for x in range(nc + 1)] for y in range(nr)]
    for i in range(nr):
        ca[i][0] = data[i, 0]  # qbit_01
        ca[i][1] = data[i, 1]  # qbit_02
        cp = data[i, 2:5]  # coefficients probability from the data (from survey).
        fallacy = data[i, 5]  # here enter irr calculator instead of the last column
        # Check if the probabilities from the question are irrational
        [irr, irr_value] = irrationality_checker(data[i, 2:6])
        # call the optimization function for the coefficients {a_ij}
        rx, rf = co(cp, fallacy)
        ca[i][2:nc] = rx  # inserting the optimized coefficients into my my array
        ca[i][nc:nc + 2] = [irr, irr_value]
    # ca = np.matrix(ca)
    return ca


def irrationality_checker(pb):  # pb - probabilities from the survey [p(qbit1),p(qbit2),p(qbit1&qbit2),type of fallacy]
    if pb[3] == 1:  # conjunction
        if (pb[2] > pb[0]) and pb[2] > pb[1]:
            irr = 1
            irr_value = (pb[2] - pb[0] + pb[2] - pb[1]) / 2
        elif pb[2] > pb[0]:
            irr = 1
            irr_value = pb[2] - pb[0]
        elif pb[2] > pb[1]:
            irr = 1
            irr_value = pb[2] - pb[1]
        else:
            irr = 0
            irr_value = (pb[2] - pb[0] + pb[2] - pb[1]) / 2
    elif pb[3] == 2:  # disjunction
        if (pb[2] < pb[0]) and (pb[2] < pb[1]):
            irr = 1
            irr_value = (pb[2] - pb[0] + pb[2] - pb[1]) / 2
        elif pb[2] < pb[0]:
            irr = 1
            irr_value = pb[2] - pb[0]
        elif pb[2] < pb[1]:
            irr = 1
            irr_value = pb[2] - pb[1]
        else:
            irr = 0
            irr_value = (pb[2] - pb[0] + pb[2] - pb[1]) / 2
    return irr, irr_value


if __name__ == '__main__':
    main()
