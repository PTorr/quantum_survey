import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
from mpldatacursor import datacursor


def main():
    N = 3
    pp1 = np.linspace(0.1, 1, N)
    pp2 = np.linspace(0.1, 1, N)
    pp1[0] = np.sqrt(0.3)
    pp2[0] = np.sqrt(0.7)
    L = 1
    fig = plt.figure('state function')
    fig.suptitle('Plots for the state in the [b,d] space under different probabilities [p1,p2] \n'\
        r'$|s\rangle=(|acp_1^0-bdp_1^1|^2 + |bcp_1^0+adp_1^1|^2 - 1)^2 +(|acp_2^0+bcp_2^1|^2 + |adp_2^1-bdp_2^0|^2 - 1)^2 $')
    for n in range(0,N):
        for m in range(0,N):
            p1 = [pp1[n],1-pp1[n]]
            p2 = [pp2[m],1-pp2[m]]
            # f, ax = plt.subplots(2, 2)
            ax = fig.add_subplot(3, 3, L,projection='3d')
            st = 'p1=',str(p1[0]),'p2',str(p2[0])
            ax.title.set_text(st)
            # ax = fig.gca(projection='3d')
            M = 10
            b = np.linspace(0, 1, M)
            d = np.linspace(0, 1, M)
            z = np.empty([np.power(M,2), 3])
            l = 0
            for i in range(len(b)):
                for j in range(len(d)):
                    z[l, 0] = b[i]
                    z[l, 1] = d[j]
                    z[l,2] = func2(b[i], d[j], p1, p2)
                    l += 1
            X1 = z[:, 0].tolist()
            # X = np.tile(X1, (len(X1), 1))
            Y1 = z[:, 1].tolist()
            # Y = np.tile(Y1, (len(Y1), 1))
            X, Y = np.meshgrid(X1, Y1)
            Z1 = z[:, 2]/np.max(z[:, 2])
            Z = np.tile(Z1, (len(Z1), 1))
            Z = func2(X,Y,p1,p2)
            ax.plot_trisurf(X1, Y1, Z1, cmap=cm.jet, linewidth=0.1,alpha=1)
            # cset = ax.contour(X, Y, Z, zdir='y', offset=1, cmap = cm.jet)
            # ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap=cm.jet, linewidth=0.1)
            ax.set_xlabel('b')
            ax.set_ylabel('d')
            ax.set_zlim([0,1])
            print L
            L += 1

    plt.show()

def func1(x,cp):
    [a,b,c,d]= cp
    return np.power((np.power(np.abs(x[1] * a * d), 2) + np.power(np.abs(x[0] * (a * c + b * c - b * d)), 2)) - 1, 2)

def func2(b,d,p1,p2):
    # x[0] = a, x[1] = b, x[2] = c, x[3] = d
    a = np.sqrt(1 - b**2)
    c = np.sqrt(1 - d**2)
    return np.power(np.power(np.abs(a * c * p1[0] - b * d * p1[1]), 2) + np.power(np.abs(b * c * p1[0] + a * d * p1[1]), 2) - 1.0, 2)\
    + np.power(np.power(np.abs(a * c * p2[0] + b * c * p2[1]), 2) + np.power(np.abs(a * d * p2[1] - b * d * p2[0]), 2) - 1.0, 2)

def prob_value_update(cp):
    # cp is coefficients probability array
    b = [np.sqrt(1 - cp[0]), np.sqrt(cp[0])]
    c = [np.sqrt(1 - cp[1]), np.sqrt(cp[1])]
    d = [np.sqrt(1 - cp[2]), np.sqrt(cp[2])]
    return b,c,d

if __name__ == '__main__':
    main()