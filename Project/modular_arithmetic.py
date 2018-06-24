'''
Filename: modular_arithmetic.py
Author : Pan Yisheng
Description: 蒙哥马利大整数模幂算法
'''
import os
import sys
import time


def modExp(base, exponent, n):
    '''
    compute the result of base^exponent (mod n)
    :param base: integer
    :param exponent: integer
    :param n: integer
    :return: base^exponent (mod n) , integer
    '''

    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array)
    return a_w_b % n

def __multi(array, bin_array):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
    return result

if __name__ == '__main__':
    print('Debug')
    begin = time.time()
    a = modExp(1112232323, 200000000000000000000000000000000000000000000012321312312312400000000000000000012, 33323)
    print(time.time()-begin)



    print(a)