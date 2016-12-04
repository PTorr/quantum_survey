import numpy as np

def func_prob12(x,p1,p2):
    # conjunction - new
    # x[0] = a_1, x[1] = b_1, x[2] = a_2, x[3] = b_2
    return np.sum(np.power(np.power(np.abs(2*x[2]*x[0]*p1[0]+2*x[2]*x[1]*p1[1]),2)+np.power(np.abs(2*x[1]*x[3]*p1[1]+2*x[3]*x[0]*p1[0]),2)-1.0,2)\
    +np.power(np.power(np.abs(2*x[2]*x[0]*p2[0]+2*x[0]*x[3]*p2[1]),2)+np.power(np.abs(2*x[1]*x[3]*p2[1]+2*x[1]*x[2]*p2[0]),2)-1.0,2))

def func1_01(x,p1,p2):
    # conjunction - old
    # x[0] = a, x[1] = b, x[2] = c, x[3] = d
    # return (0.5*x[1]-1)**2
    return np.sum(np.power(np.power(np.abs(x[0]*x[2]*p1[0]-x[1]*x[3]*p1[1]),2)+np.power(np.abs(x[1]*x[2]*p1[0]+x[0]*x[3]*p1[1]),2)-1.0,2)\
    +np.power(np.power(np.abs(x[0]*x[2]*p2[0]+x[1]*x[2]*p2[1]),2)+np.power(np.abs(x[0]*x[3]*p2[1]-x[1]*x[3]*p2[0]),2)-1.0,2))

def func2(x,b,c,d):

    return np.power(np.power(np.abs(x[0]*b[0]+x[1]*b[0]),2)+np.power(np.abs(x[2]*b[1]+x[3]*b[1]),2)-1,2)\
    +np.power(np.power(np.abs(x[0]*c[0]+x[2]*c[0]),2)+np.power(np.abs(x[1]*c[1]+x[3]*c[1]),2)-1,2)\
    +np.power(np.power(np.abs(x[0]*d[0]),2)+np.power(np.abs((x[1]+x[2]+x[3]),2)*d[1])-1,2)

def func3(x,b,c,d):
    return np.power(np.power(np.abs(x[0]*b[0]+x[1]*b[0]),2)+np.power(np.abs(x[2]*b[1]+x[3]*b[1]),2)-1,2)\
    +np.power(np.power(np.abs(x[0]*c[0]+x[2]*c[0]),2)+np.power(np.abs(x[1]*c[1]+x[3]*c[1]),2)-1,2)\
    +np.power(np.power(np.abs((x[0]+x[1]+x[2])*d[0]),2)+ np.power(np.abs(x[3]*d[1]),2)-1,2)

def func_conjunction(x,cp):
    #  new - calculates p12
    [a1,b1,a2,b2]= cp
    # x[0] = p12_0, x[1] = p12_1
    return np.power((np.power(np.abs(2*x[1]*b1*b2),2)+np.power(np.abs(2*x[0]*(a1*a2+a1*b2+b1*a2)),2))-1,2)

def func4(x,cp):
    # old - calculates p12
    [a, b, c, d] = cp
    # x[0] = p12_0, x[1] = p12_1
    return np.power((np.power(np.abs(x[1]*a*d),2)+np.power(np.abs(x[0]*(a*c+b*c-b*d)),2))-1,2)
# ---------------------------------------------------------------------------------------------------------------------
def cons_conjunction():
    cons = (#{'type': 'eq',
             #'fun' : lambda x: np.array([x[1]-2, 2*x[0] - x[1]])}, # g(x) = sum(x)-1
            {#'type': 'ineq',
             'type': 'eq',
             'fun': lambda x: np.array([np.sum(np.abs(x))-1])})
    return cons

def cons1():
    cons = (#{'type': 'eq',
             #'fun' : lambda x: np.array([x[1]-2, 2*x[0] - x[1]])}, # g(x) = sum(x)-1
            {#'type': 'ineq',
             'type': 'eq',
             'fun': lambda x: np.array([np.sum(np.power(np.abs(x), 2))-1])})
    return cons

def cons_prob12():
    # new conjunction constrains
    cons = [{'type': 'eq', 'fun': lambda x: np.array([np.power(np.abs(x[0]), 2) + np.power(np.abs(x[1]), 2) - 1])}, # a^2+b^2=1
            {'type': 'eq', 'fun': lambda x: np.array([np.power(np.abs(x[2]), 2) + np.power(np.abs(x[3]), 2) - 1])}] # c^2+d^2=1
    return cons

def cons11_01():
    # old conjunction constrains
    cons = [{'type': 'eq', 'fun': lambda x: np.array([np.power(np.abs(x[0]), 2) + np.power(np.abs(x[1]), 2) - 1])}, # a^2+b^2=1
            {'type': 'eq', 'fun': lambda x: np.array([np.power(np.abs(x[2]), 2) + np.power(np.abs(x[3]), 2) - 1])}] # c^2+d^2=1
    return cons
