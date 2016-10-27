from read_data import read_data
from constrained_optimization import main as co
from entanglement_check import entanglement_checker as ec
from generate_data import data_generator as dg
import numpy as np
import os
import matplotlib.pyplot as plt

def main():
    # This is the main function which:
    #   1) Reads the probabilities from the survey.
    #   2) Calculate 2 qbits coefficients and check for irrationality.
    #   3) Checking if they are entangled.
    #   4) Plots irrationality vs. entanglement.
    #   5) Tracing out single qbit coefficients.

    # ------------------------------------------------------------------------------------------------------------
    # Load/create the data
    table_path = 'D:\Users\Torr\PycharmProjects\quantum_survey/test_data.csv'
    if os.path.exists(table_path) != True:
        table_path = raw_input("The path is wrong \nEnter the full path of the data file: ")
        if os.path.exists(table_path) != True:
            print ('File not found')
            quit()

    # data = read_data(table_path)
    data = dg(100)

    # ------------------------------------------------------------------------------------------------------------
    # Compute the coefficients
    coeff_a = coefficients_calculator(data)
    # print np.isnan(coeff_a).any()

    # ------------------------------------------------------------------------------------------------------------
    # Checking if the qbits are entangled
    ca_nc = len(coeff_a[0])
    for i in range(len(coeff_a)):
        [evc, c, entangled] = ec(coeff_a[i][2:6])
        coeff_a[i][ca_nc:ca_nc + 2] = [entangled, evc]
    # Saving the coefficients of 2qbits array to a csv file
    # [qbit1, qbit2, a00, a01, a10, a11, irr, irr_value, entangled, evc]       - evc = from the concurrence.
    np.savetxt("two_qbits_coefficients_summary.csv", coeff_a, delimiter=",")

    # ------------------------------------------------------------------------------------------------------------
    # Plots irrationality vs entanglement
    coeff_a1 = np.matrix(coeff_a)
    irrationality_values = np.matrix(coeff_a1[:, 9])
    entanglement_values = np.matrix(coeff_a1[:, 7])
    # irr_ent_plt(irrationality_values,entanglement_values)

    # ------------------------------------------------------------------------------------------------------------
    # Tracing out single qubit coefficients
    coeff_a2 = np.array(coeff_a1)
    available_qbits = np.unique(coeff_a2[:,0:2])
    m = 0
    qa = np.zeros([len(available_qbits),3])
    for q in available_qbits:
        qa[m,0:3] = [q,trace_out(q, 0, coeff_a),trace_out(q, 1, coeff_a)]
        m += 1
    # Saving the coefficients of a single qbit to a csv file
    # qa = [qbit, a0, a1]
    np.savetxt("single_qbit_cofficients.csv", qa, delimiter=",")


def coefficients_calculator(data):
    # computes the coefficients
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

def trace_out(qbit,state,coeff_a):
    #  calculates coefficient of single qbit according to:
    #   qbit - wanted qubit
    #   state - 0/1
    ca = np.matrix(coeff_a)
    qbit_idx = [ca[:,0] == qbit] # if the bit is the 1st bit
    qbit_idx1 = [ca[:, 1] == qbit] # if the bit is the 2nd bit

    a00 = ca[:, 2]
    a01 = ca[:, 3]
    a10 = ca[:, 4]
    a11 = ca[:, 5]

    ca1 = a00[qbit_idx].T
    ca2 = a01[qbit_idx].T
    ca3 = a10[qbit_idx].T
    ca4 = a11[qbit_idx].T

    ca11 = a00[qbit_idx1].T
    ca22 = a01[qbit_idx1].T
    ca33 = a10[qbit_idx1].T
    ca44 = a11[qbit_idx1].T

    if state == 0:
        qbit_state = sum(np.power(ca1, 2)) + sum(np.power(ca2, 2))
        qbit_state += sum(np.power(ca11, 2)) + sum(np.power(ca33, 2))
    if state == 1:
        qbit_state = sum(np.power(ca3,2)) + sum(np.power(ca4,2))
        qbit_state += sum(np.power(ca22, 2)) + sum(np.power(ca44, 2))
    qbit_state = np.sqrt(qbit_state)
    qbit_state = qbit_state[0,0]
    return qbit_state

def irrationality_checker(pb):  # pb - probabilities from the survey [p(qbit1),p(qbit2),p(qbit1&qbit2),type of fallacy]
    # Checks if the probabilities are irrational.
    # Then calculate how much is the value is irrational by subtracting probabilities
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

def irr_ent_plt(x,y):
    # Plots the irrationality (irr_value) as function of the entanglement (evc)
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

    plt.plot(np.asarray(x1.T), np.asarray(y1.T), 'b.', label = 'rational & not entangled')
    plt.plot(np.asarray(x2.T), np.asarray(y2.T), 'g*', label = 'rational & entangled')
    plt.plot(np.asarray(x3.T), np.asarray(y3.T), 'mx', label = 'irrational & not entangled')
    plt.plot(np.asarray(x4.T), np.asarray(y4.T), 'r+', label = 'irrational & entangled')

    # p1, =
    # p2, =
    # p3, =
    # p4, =
    # plt.legend([p1,p2,p3,p4],['rational & not entangled','rational & entangled','irrational & not entangled','irrational & entangled'])
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()
    plt.xlabel('Entanglement')
    plt.ylabel('Irrationality')
    plt.savefig('irr_ent.png')
    plt.show()

if __name__ == '__main__':
    main()
