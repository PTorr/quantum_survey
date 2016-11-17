import numpy as np
# This is for changing the coefficients value to the input.
cp = [] # coefficients probabilities
fallacy = [] # conjunction/disjunction/...

def inp_value(cpv,fallacyv):
    global cp,fallacy
    cp = cpv
    fallacy = fallacyv

def func1(x):
    inp_value(cpv,fallacyv)
    return func1_1()


def func1_1(x,cp):
    [p1, p2, p12] = prob_value_update(cp)
    return np.power(np.sum(np.multiply(np.abs(x), np.abs(x))) - 1, 2) \
           + np.power(np.abs(x[0] * b[0] + x[1] * b[0]) * np.abs(x[0] * b[0] + x[1] * b[0]) + np.abs(
        x[2] * b[1] + x[3] * b[1]) * np.abs(x[2] * b[1] + x[3] * b[1]) - 1, 2) \
           + np.power(np.abs(x[0] * c[0] + x[2] * c[0]) * np.abs(x[0] * c[0] + x[2] * c[0]) + np.abs(
        x[1] * c[1] + x[3] * c[1]) * np.abs(x[1] * c[1] + x[3] * c[1]) - 1, 2) \
           + np.power(
        np.abs((x[0] + x[1] + x[2]) * d[0]) * np.abs((x[0] + x[1] + x[2]) * d[0]) + np.abs(x[3] * d[1]) * np.abs(
            x[3] * d[1]) - 1, 2)

def prob_value_update(cp):
    # cp is coefficients probability array
    b = [np.sqrt(1 - cp[0]), np.sqrt(cp[0])]
    c = [np.sqrt(1 - cp[1]), np.sqrt(cp[1])]
    d = [np.sqrt(1 - cp[2]), np.sqrt(cp[2])]
    return b, c, d
