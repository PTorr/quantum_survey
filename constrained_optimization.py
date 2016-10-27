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
import matplotlib.pyplot as plt

# This is for changing the coefficients value to the input.
cp = [] # coefficients probabilities
fallacy = [] # conjunction/disjunction/...
def inp_value(cpv,fallacyv):
    global cp,fallacy
    cp = cpv
    fallacy = fallacyv

def main(cpv,fallacyv):
    # this is the main function that minimizes
    # its takes:
    #       func1 is the name of a function that returns a single number (f(x))
    #       init1() is a function that returns the initial vector, x_0
    #       jac=func1_deriv is the name of the function that returns the derivative of f, df/dx(x)
    #       constraints=cons3() is the function that returns a dictionary (see below)
    #       method='SLSQP' the optimizaiton method (don't change)
    #       options={} don't change
    inp_value(cpv,fallacyv)

    if fallacy == 1: # conjunction
        res = minimize(func1, init1(),  # jac=func1_deriv,
                       constraints=cons1(), method='SLSQP', options={'disp': False})
    elif fallacy == 2: # disjunction
        res = minimize(func2, init1(),  # jac=func1_deriv,
                       constraints=cons1(), method='SLSQP', options={'disp': False})

    # res has the following fields:
    # print(res.x) # the x at the solution
    # print(res.fun) # the minimum value of f
    return res.x, res.fun

    # this just plots the resulting x (don't use it for your own code)
    # fig, ax = plt.subplots()
    # ax.bar(np.arange(len(res.x)),res.x)
    # plt.show()

# function that returns the initial value of the vector x
def init1():
    x0=[0.5,0.5,0.5,0.5]
    return x0

# f(x) - the function to minimize-
# receives a vector x
def func1(x):
    # cp is coefficients probability array
    b = [np.sqrt(1-cp[0]), np.sqrt(cp[0])]
    c = [np.sqrt(1-cp[1]), np.sqrt(cp[1])]
    d = [np.sqrt(1-cp[2]), np.sqrt(cp[2])]

    # np.sum(np.multiply(np.abs(x), np.abs(x)))
    return np.power(np.sum(np.multiply(np.abs(x), np.abs(x))) - 1,2)\
    +np.power(np.abs(x[0]*b[0]+x[1]*b[0])*np.abs(x[0]*b[0]+x[1]*b[0])+ np.abs(x[2]*b[1]+x[3]*b[1])*np.abs(x[2]*b[1]+x[3]*b[1])-1,2)\
    +np.power(np.abs(x[0]*c[0]+x[2]*c[0])*np.abs(x[0]*c[0]+x[2]*c[0])+ np.abs(x[1]*c[1]+x[3]*c[1])*np.abs(x[1]*c[1]+x[3]*c[1])-1,2)\
    +np.power(np.abs((x[0]+x[1]+x[2])*d[0])*np.abs((x[0]+x[1]+x[2])*d[0])+ np.abs(x[3]*d[1])*np.abs(x[3]*d[1])-1,2)

def func2(x):
    # cp is coefficients array
    b = [np.sqrt(1-cp[0]), np.sqrt(cp[0])]
    c = [np.sqrt(1-cp[1]), np.sqrt(cp[1])]
    d = [np.sqrt(1-cp[2]), np.sqrt(cp[2])]

    # np.sum(np.multiply(np.abs(x), np.abs(x)))
    return np.power(np.sum(np.multiply(np.abs(x), np.abs(x))) - 1,2)\
    +np.power(np.abs(x[0]*b[0]+x[1]*b[0])*np.abs(x[0]*b[0]+x[1]*b[0])+ np.abs(x[2]*b[1]+x[3]*b[1])*np.abs(x[2]*b[1]+x[3]*b[1])-1,2)\
    +np.power(np.abs(x[0]*c[0]+x[2]*c[0])*np.abs(x[0]*c[0]+x[2]*c[0])+ np.abs(x[1]*c[1]+x[3]*c[1])*np.abs(x[1]*c[1]+x[3]*c[1])-1,2)\
    +np.power(np.abs(x[0]*d[0])*np.abs(x[0]*d[0])+np.abs((x[1]+x[2]+x[3])*d[1])*np.abs((x[1]+x[2]+x[3])*d[1])-1,2)


# df/dx - if you know it, then add it
# the analytical derivative of f
def func1_deriv(x):
    return [x[1]+6*x[0], x[0] - 2]

# constrinats
# returns a dictionary with equality 'type':'eq' and inequality 'type':'ineq'
# the 'fun' are the functions that describe the constrinats, g(x)
# the format is:
#       "lambda x: np.array" - don't change, keep it
#       ([g_1(x), g(_2(x)])
def cons1():
    cons = (#{'type': 'eq',
             #'fun' : lambda x: np.array([x[1]-2, 2*x[0] - x[1]])}, # g(x) = sum(x)-1
            {#'type': 'ineq',
             'type': 'eq',
             'fun' : lambda x: np.array([np.sum(np.multiply(np.abs(x), np.abs(x)))-1])})
    return cons


def mean(x):
    return sum(np.multiply(np.arange(len(x))+1,x))

def cons2():
    cons = ({'type': 'eq',
             'fun' : lambda x: np.array([sum(x)-1,mean(x)-12])}, # g_1(x) = sum(x)-1, g_2(x) = mean(x)-12
            {'type': 'ineq',
             'fun' : lambda x: np.array(x)}) #g(x) : x>0
    return cons

def std(x):
    mx = mean(x)
    return sum( np.multiply(((np.arange(len(x))+1)-mx)**2,x))

def cons3():
    cons = ({'type': 'eq',
             'fun' : lambda x: np.array([sum(x)-1,mean(x)-12,std(x)-10])}, # g_1(x) = sum(x)-1, g_2(x) = mean(x)-12, g_3(x)=std(x)-10
            {'type': 'ineq',
             'fun' : lambda x: np.array(x)}) #g(x) : x>0
    return cons

if __name__ == '__main__':
    main()
