import numpy as np
def main():
    d = np.sqrt(0.6)
    c = np.sqrt(1-d*d)
    d1 = np.sqrt(0.4)
    c1 = np.sqrt(1 - d1 * d1)
    [a,b] = ab(c,c1,d,d1)
    print ang(1)
    print('|s> = %s[%s|00>+%s|11>]+%s[%s|01>-%s|10>]' % ('a', 'c', 'd', 'b', 'c', 'd'))
    print('|s> = %.2f[%.2f|00>+%.2f|11>]+%.2f[%.2f|01>-%.2f|10>]'% (a,c,d,b,c,d))

def coeffs_cd(a,b,c1,d1):
    # c =
    # d =
    # return c,d
    pass
def coeffs_c1d1(a,b,c,d):
    c1 = a*c+b*d
    d1 = a*d-b*c
    return c1, d1
def ab(c,c1,d,d1):
    a = c*c1+d*d1
    b = d*c1-d1*c
    return a,b
def ang(a):
    # calculate the angle between the bits from a.
    import math
    theta = math.degrees(math.acos(a))
    return theta

if __name__ == '__main__':
    main()