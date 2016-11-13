import numpy as np
from constraint_analysis import irrationality_checker as irr_check


def main():
    # help(state_prob)
    d = np.sqrt(0.8)
    d1 = np.sqrt(0.2)
    ca = np.ndarray((6), float)
    qa = np.ndarray((2, 3), float)
    # ca,qa = state_prob(d,d1)
    # print np.matrix(ca)
    # ca,qa = state_prob(d1,d)
    # print np.matrix(ca)
    n = 10
    d = np.linspace(0, 1, n)
    d1 = np.linspace(0, 1, n)
    # Filling the data array
    irr_coeff = []
    for i in range(n):
        for j in range(n):
            [ca, qa] = state_prob(d[i], d1[j])
            [irr, irr_value] = irr_check([qa[0, 2],qa[1, 2],ca[5],1])
            if (irr==1):
                irr_coeff.append([qa[0, 2], qa[1, 2], ca[5]])
    if len(irr_coeff) != 0:
        np.savetxt("irrationality_coefficients.csv", irr_coeff, delimiter=",",
                   header='q1a1, q2a1, a11')
    else:
        print 'No irrationalities where found'


def state_prob(d,d1):
    '''This is the function which run the functions that calculate:
        1) coefficients of 2 qbits state
        2) probabilities of each qubit.
        constrains:
        c * c + d * d = 1
        c1 * c1 + d1 * d1 = 1'''
    c = np.sqrt(1 - d * d)
    c1 = np.sqrt(1 - d1 * d1)
    [a, b] = ab(c, c1, d, d1)
    ca = np.ndarray((6), float)
    ca[0:2] = [1, 2]
    ca[2:6] = coeff_a(a, b, c, d)
    # print('|s> = %s[%s|00>+%s|11>]+%s[%s|01>-%s|10>]' % ('a', 'c', 'd', 'b', 'c', 'd'))
    # print('|s> = %+.2f[%+.2f|00>%+.2f|11>]%+.2f[%+.2f|01>-(%+.2f)|10>]'% (a,c,d,b,c,d))
    # print('|s> = %+.2f|00>%+.2f|11>%+.2f|01>%+.2f|10>' % (ca[2],ca[5],ca[3],ca[4]))

    from constraint_analysis import trace_out as trace_out
    qa = np.ndarray((2,3), float)
    # qa[0, :] = ['qbit', 'a0', 'a1']
    qa[0, :] = [1, trace_out(1, 0, ca), trace_out(1, 1, ca)]
    qa[1, :] = [2, trace_out(2, 0, ca), trace_out(2, 1, ca)]
    return ca, qa


def coeffs_cd(a,b,c1,d1):
    # c =
    # d =
    # return c,d
    pass

def coeffs_c1d1(a,b,c,d):
    '''calculate c' & d' from c,d,a,b'''
    c1 = a*c+b*d
    d1 = a*d-b*c
    return c1, d1

def ab(c,c1,d,d1):
    '''calculate a & b from c,c1,d,d1'''
    a = c*c1+d*d1
    b = d*c1-d1*c
    return a,b

def ang(a):
    '''calculate the angle between the bits from a.'''
    import math
    theta = math.degrees(math.acos(a))
    return theta

def coeff_a(a,b,c,d):
    '''calculate the coefficients of the 2 qbits state'''
    ca = np.ndarray((4), float)
    ca[0] = a * c
    ca[1] = b * c
    ca[2] = b * d
    ca[3] = a * d
    return ca

if __name__ == '__main__':
    main()