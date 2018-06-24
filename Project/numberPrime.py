'''
Filename: numberPrime.py
Author: Pan Yisheng
Description: generate big prime and compute rsa key pair
'''

import random
from gcd import *
from primality_tester import *
from random import randrange, getrandbits
import time

# Function to test primality
def NumberIsPrime(n):
	if (n==2 or n==3):
		return True
	if (n<2 or n % 3 == 0):
		return False
	return prime_test_miller_rabin(n)



#Function to generete number primes
#Generete two different prime number
def GenereteNumberPrime(n_bits):
	f = False
	while not f:
		# Generate random numbers
		p = getrandbits(n_bits)
		q = getrandbits(n_bits)
		if NumberIsPrime(p) and NumberIsPrime(q) and p!=q:
			f = True

	return p, q


# Function compute e and d

def GetParams(phi_n):
	d = 0
	e = 65537
	f_e = False
	'''
	while f_e == False:
		e = random.randint(1,phi_n-1)
		if (gcd(e,phi_n) == 1):
			f_e = True
	'''

	_, d,  _ = euclideanExtendedGCD(e,phi_n)
	if(d<0):
		d+= phi_n
	return d, e

def GenParms(n_bits,DEBUG):
	p,q = GenereteNumberPrime(n_bits)
	n = p * q

	phi_n= (p-1) *(q-1)
	d, e = GetParams(phi_n)

	#while(d<0):
	#	d+=y

	if DEBUG == True:
		print("P, Q: ", p, q)
		print("N: ", n)
		print("Phi(n): ", phi_n)
		print("E, D: ", e, d)
	return n, d, e 

#Debuger function GenParms
def Gen_Parms2(p,q,DEBUG=True):
	#p,q = GenereteNumberPrime(n_bits)
	n = p * q
	#y = carmichael(p, q)
	# totiente
	phi_n= (p-1) *(q-1)
	d, e = GetParams(phi_n)

	#while(d<0):
	#	d+=y
	
	if DEBUG == True:
		print("P, Q: ", p, q)
		print("N: ", n)
		print("Phi(n): ", phi_n)
		print("E, D: ", e, d)
	return n, d, e 


#Debuge function
if __name__ == '__main__':
	# Testes 
	begin = time.time()
	GenereteNumberPrime(512)
	print("time1:",time.time()-begin)

	begin = time.time()
	y = randint_bits(512)
	print("time2:",time.time()-begin)


	#p,q= GenereteNumberPrime(n_bits=3)
	print("Numeros primos")
	#print(p,q)


