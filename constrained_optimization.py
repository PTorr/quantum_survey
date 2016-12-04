#-------------------------------------------------------------------------------
# Name:        constrained_optimization
# Purpose:
#
# Author:      Goren
#
# Created:     03/11/2015
# Copyright:   (c) Goren 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
from scipy.optimize import minimize
import constrained_funcs as cf
import matplotlib.pyplot as plt

def main(cp,fallacy):
    import temp as tmp
    # this is the main function that minimizes
    # its takes:
    #       func1 is the name of a function that returns a single number (f(x))
    #       init1() is a function that returns the initial vector, x_0
    #       jac=func1_deriv is the name of the function that returns the derivative of f, df/dx(x)
    #       constraints=cons3() is the function that returns a dictionary (see below)
    #       method='SLSQP' the optimizaiton method (don't change)
    #       options={} don't change
    # inp_value(cpv,fallacyv)
    [p1, p2, p12] = prob_value_update(cp)
    if fallacy == 1: # conjunction
        res = minimize(cf.func_prob12, init1(), args=(p1,p2), constraints=cf.cons_prob12(), method='SLSQP', options={'disp': False})
    elif fallacy == 2: # disjunction
        res = minimize(cf.func2, init1(), args=(p1,p2,p12), constraints=cf.cons1(), method='SLSQP', options={'disp': False})
    elif fallacy == 4: # new conjunction
        res = minimize(cf.func_conjunction, init2(), args=(cp), constraints=cf.cons_conjunction(), method='SLSQP', options={'disp': False})

    # res has the following fields:
    # print(res.x) # the x at the solution
    # print(res.fun) # the minimum value of f
    # print res.x, cp
    return res.x, res.fun

# function that returns the initial value of the vector x
def init1():
    x0=[0.5,0.5,0.5,0.5]
    return x0
def init2():
    x0=[0.5,0.5]
    return x0


# f(x) - the function to minimize-
# receives a vector x
def prob_value_update(cp):
    # cp is coefficients probability array
    p1 = [1 - cp[0], cp[0]]
    p2 = [1 - cp[1], cp[1]]
    p12 = [1 - cp[2], cp[2]]
    return p1,p2,p12

# constrinats
# returns a dictionary with equality 'type':'eq' and inequality 'type':'ineq'
# the 'fun' are the functions that describe the constrinats, g(x)
# the format is:
#       "lambda x: np.array" - don't change, keep it
#       ([g_1(x), g(_2(x)])


if __name__ == '__main__':
    main()
