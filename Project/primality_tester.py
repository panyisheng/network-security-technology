from random import randrange
from modular_arithmetic import *
from gcd import *
import time
import math
import random
import operator


#Rabin Miller Test to check primality

def prime_test_miller_rabin(p, k=25):
    """
    Test for primality by Miller-Rabin
    Stronger than Solovay-Strassen's test
    """
    if p < 2: return False
    if p <= 3: return True
    if p & 1 == 0: return False

    # p - 1 = 2**s * m
    s, m = extract_prime_power(p - 1, 2)

    for j in range(k):
        a = random.randint(2, p - 2)
        if gcd(a, p) != 1:
            return False

        b = pow(a, m, p)
        if b in (1, p - 1):
            continue

        for i in range(s):
            b = pow(b, 2, p)

            if b == 1:
                return False

            if b == p - 1:
                # is there one more squaring left to result in 1 ?
                if i < s - 1: break  # good
                else: return False   # bad
        else:
            # result is not 1
            return False
    return True

def extract_prime_power(a, p):
    """
    Return s, t such that  a = p**s * t,  t % p = 0
    """
    s = 0
    if p > 2:
        while a and a % p == 0:
            s += 1
            a //= p
    elif p == 2:
        while a and a & 1 == 0:
            s += 1
            a >>= 1
    else:
        raise ValueError("Number %d is not a prime (is smaller than 2)" % p)
    return s, a





if __name__ == '__main__':
    print('======================test=========================')

    #print(primality(3))
    begin = time.time()
    xnum = prime_test_miller_rabin(250556952327646214427246777488032351712139094643988394726193347352092526616305469220133287929222242315761834129196430398011844978805263868522770723615504744438638381670321613949280530254014602887707960375752016807510602846590492724216092721283154099469988532068424757856392563537802339735359978831013)
    print(time.time()-begin)
    if(xnum == True ):
    #print(num)
        print('test success!')