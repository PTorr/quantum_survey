from read_data import read_data
from constrained_optimization import main as co
from entanglement_check import entanglement_checker as ec
from generate_data import data_generator as dg
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def main():
    # table_path = 'D:\Users\Torr\PycharmProjects\quantum_survey/test_data.csv'
    # table_path = '/home/torr/PycharmProjects/quantum_survey/test_data.csv'
    table_path = 'test_data.csv'
    constraint_analysis(table_path)


def constraint_analysis(table_path):
    '''This is the main function which:
      1) Reads the probabilities from the survey.
      2) Calculate 2 qbits coefficients and check for irrationality.
      3) Checking if they are entangled.
      4) Plots irrationality vs. entanglement.
      5) Tracing out single qbit coefficients.
      Input: table_path - the full path of the csv file from the Qualtrics.'''

    # ------------------------------------------------------------------------------------------------------------
    # Load/create the data
    if os.path.exists(table_path) != True:
        table_path = raw_input("The path is wrong \nEnter the full path of the data file: ")
        if os.path.exists(table_path) != True:
            print ('File not found')
            quit()

    data = read_data(table_path)
    # data = dg(20)

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
    np.savetxt("two_qbits_coefficients_summary.csv", coeff_a, delimiter=",",
               header='qbit1, qbit2, a00, a01, a10, a11, irr, irr_value, entangled, evc')

    # ------------------------------------------------------------------------------------------------------------
    # Plots irrationality vs entanglement
    coeff_a1 = np.matrix(coeff_a)
    irrationality_values = np.matrix(coeff_a1[:, 9])
    entanglement_values = np.matrix(coeff_a1[:, 7])
    irr_ent_plt(irrationality_values, entanglement_values, data)

    # ------------------------------------------------------------------------------------------------------------
    # Tracing out single qubit coefficients
    coeff_a2 = np.array(coeff_a1)
    available_qbits = np.unique(coeff_a2[:, 0:2])
    m = 0
    qa = np.zeros([len(available_qbits), 3])
    for q in available_qbits:
        qa[m, 0:3] = [q, trace_out(q, 0, coeff_a), trace_out(q, 1, coeff_a)]
        m += 1
    # Saving the coefficients of a single qbit to a csv file
    np.savetxt("single_qbit_cofficients.csv", qa, delimiter=",",
               header='qbit, a0, a1')


def coefficients_calculator(data):
    '''computes the coefficients
        input: data - data array: [qbit1, qbit2, p(qb1=1), p(qb2=1),p(qb1=1 & qb2 = 1), fallacy type]
        output: ca - np.ndarray [qbit1, qbit2, a00, a01, a10, a11, is_irrational, irrationality_value]'''
    [nr, nc] = data.shape  # number of rows and columns in the array
    #          columns #            rows #
    ca = [[0 for x in range(nc + 1)] for y in range(nr)]
    for i in range(nr):
        ca[i][0] = data[i, 0]  # qbit_01
        ca[i][1] = data[i, 1]  # qbit_02
        cp = data[i, 2:5]  # coefficients probability from the data (from survey).
        fallacy = data[i, 5]  # here enter irr calculator instead of the last column
        # call the optimization function for the coefficients {a_ij}
        rx, rf = co(cp, fallacy)
        if fallacy == 1:
            pp, rf = co(rx, 4)  # rx = [a,b,c,d], pp[p12_0,p12_1]
            rx = [rx[0] * rx[2], rx[0] * rx[3], rx[1] * rx[2], rx[1] * rx[3]]
            # Check if the probabilities from the question are irrational
            p1 = data[i, 2]
            p2 = data[i, 3]
            p12 = data[i, 4]
            # [irr, irr_value] = irrationality_checker([p1,p2,pp[1],fallacy])
            [irr, irr_value] = irrationality_checker([p1, p2, p12, fallacy])
            # print ([p1,p2,pp[1],fallacy])
            # print rx
        else:
            [irr, irr_value] = irrationality_checker(data[i, 2:6])
        ca[i][2:nc] = rx  # inserting the optimized coefficients into my my array
        ca[i][nc:nc + 2] = [irr, irr_value]
    # ca = np.matrix(ca)
    return ca


def trace_out(qbit, state, coeff_a):
    '''calculates coefficient of single qbit according to:
       qbit - wanted qubit
       state - 0/1
       input: qbit - which qbit to trace out.
              state - state of the qbit.
              coeff_a - array of all the coefficients of the two qbits state.
       output: qbit_state - the coefficient of the selected qbit and its state.'''
    ca = np.matrix(coeff_a)
    qbit_idx = [ca[:, 0] == qbit]  # if the bit is the 1st bit
    qbit_idx1 = [ca[:, 1] == qbit]  # if the bit is the 2nd bit

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
        qbit_state = sum(np.power(ca3, 2)) + sum(np.power(ca4, 2))
        qbit_state += sum(np.power(ca22, 2)) + sum(np.power(ca44, 2))
    qbit_state = np.sqrt(qbit_state)
    qbit_state = qbit_state[0, 0]
    return qbit_state


def irrationality_checker(pb):
    '''Checks if the probabilities are irrational.
       Then calculate how much is the value is irrational by subtracting probabilities
       input: pb - probabilities from the survey [p(qbit1),p(qbit2),p(qbit1&qbit2),type of fallacy]
       p(qbit1&qbit2) - we predict?
       output: irr - 0/1 is irrational
               irr_value - the value of the irrationality'''
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


def irr_ent_plt(x, y, data):
    '''Plots the irrationality (irr_value) as function of the entanglement (evc)
        input: x - entanglement values
               y - irrationality values'''
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

    dxx = data[:, 2]
    dyy = data[:, 3]
    dzz = data[:, 4]
    dxx = np.matrix(dxx)
    dyy = np.matrix(dyy)
    dzz = np.matrix(dzz)
    dxx = dxx.T
    dyy = dyy.T
    dzz = dzz.T
    dxx1 = dxx[yy > 0]
    dyy1 = dyy[yy > 0]
    dzz1 = dzz[yy > 0]
    dy1 = dyy1[xx1 <= 0]
    dx1 = dxx1[xx1 <= 0]
    dz1 = dzz1[xx1 <= 0]
    dy2 = dyy1[xx1 > 0]
    dx2 = dxx1[xx1 > 0]
    dz2 = dzz1[xx1 > 0]
    dyy2 = dyy[yy <= 0]
    dxx2 = dxx[yy <= 0]
    dzz2 = dzz[yy <= 0]
    dy3 = dyy2[xx2 <= 0]
    dx3 = dxx2[xx2 <= 0]
    dz3 = dzz2[xx2 <= 0]
    dy4 = dyy2[xx2 > 0]
    dx4 = dxx2[xx2 > 0]
    dz4 = dzz2[xx2 > 0]

    plt.figure(1)
    plt.plot(np.asarray(x1.T), np.asarray(y1.T), 'bo', label='irrational & not entangled')
    plt.plot(np.asarray(x2.T), np.asarray(y2.T), 'g*', label='irrational & entangled')
    plt.plot(np.asarray(x3.T), np.asarray(y3.T), 'md', label='rational & not entangled')
    plt.plot(np.asarray(x4.T), np.asarray(y4.T), 'rs', label='rational & entangled')

    plt.legend()
    plt.xlabel('entangled')
    plt.ylabel('irrationality')
    plt.title('Irrationality - Entanglement')
    plt.savefig('irr_ent.png')

    fig2 = plt.figure(2)
    ax2 = fig2.gca(projection='3d')
    ax2.scatter(np.asarray(dx1.T), np.asarray(dy1.T), np.asarray(dz1.T), color='blue', marker='o', s=30,
                label='irrational & not entangled')
    ax2.scatter(np.asarray(dx2.T), np.asarray(dy2.T), np.asarray(dz2.T), color='green', marker='*', s=30,
                label='irrational & entangled')
    ax2.scatter(np.asarray(dx3.T), np.asarray(dy3.T), np.asarray(dz3.T), color='magenta', marker='d', s=30,
                label='rational & not entangled')
    ax2.scatter(np.asarray(dx4.T), np.asarray(dy4.T), np.asarray(dz4.T), color='red', marker='s', s=30,
                label='rational & entangled')
    ax2.legend()
    ax2.set_xlabel('p1')
    ax2.set_ylabel('p2')
    ax2.set_zlabel('p12')
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])
    ax2.set_zlim([0, 1])
    ax2.set_title('Probabilities')

    # fig3  = plt.figure(3)
    # ax3 = fig3.gca(projection='3d')
    # x = data[:, 2]
    # # x = x.tolist()
    # y = data[:, 3]
    # # y = y.tolist()
    # z = data[:, 4]
    # # z = z.tolist()
    # X, Y = np.meshgrid(x, y)
    # Z = np.tile(z,[len(z),1])
    # # ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    # ax3.plot_trisurf(x, y, z, cmap=cm.jet)
    # ax3.set_xlabel('p1')
    # ax3.set_ylabel('p2')
    # ax3.set_zlabel('p12')

    plt.show()


if __name__ == '__main__':
    main()
