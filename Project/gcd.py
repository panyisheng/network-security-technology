'''
Filename : gcd.py
Author: Pan Yisheng
Description: implement two euclidean function

1. gcd() for compute the greatest common divisor
2. euclideanExtendedGCD(a,b) for solve ax+by = gcd(a,b)
'''

import os
import sys
import time


def gcd(p,q):
    '''
    compute the greatest common divisor

    :param p: integer

    :param q: integer

    :return:  integer
    '''

    while q != 0:
        (p,q) = (q,p % q)
    return p

def euclideanExtendedGCD(n1,n2):
    '''
    Implement the euclidean extend GCD algorithm
    solve the indeterminate equation "a*x+b*y = gcd(a,b)"

    :param n1: coefficient a (type integer)

    :param n2: coefficient b (type integer)

    :return: gcd(n1,n2), x , y
    '''
    u,v,s,t = 1, 0 ,0 ,1
    #Swap
    if (n2<n1):
        aux = n2
        n2 =n1
        n1 = aux
    while n2!=0:
        q =n1 // n2
        n1,n2 = n2,n1-q*n2
        u,s = s,u-q*s
        v,t = t,v-q*t
    return n1,u,v



if __name__ == '__main__':
    print('==============test====================')
    b = euclideanExtendedGCD(5023,148)

    d = gcd(18,102)
    print(b)
    print(' ')
    print(' \n : ',d)

    print(5023/1487)