'''
Filename: cca2.py
Author: Pan Yisheng
Description: implement ccsa2 attack off-line
'''

from rsa import *
from aes import *
from convert import *
import pickle

def attack(C,publicKey,privateKey):
    '''
    :param C: integer , encrypted AES key
    :param publicKey: tuple of int, (n,e)
    :return: recover_key string
    '''
    recover_key = 0
    for i in range(127):
        print('------------attack {}-------------'.format(i))
        '''
        try to gain the ith bit(0 means the least significant bit)
        C_b = C << (127-i)*e 
        '''
        be = (127-i)*publicKey[1]
        C_b = C<<be  #integer
        #print(be)

        '''
        forge AES key K_b, then encrypt the tset WUP
        assume the ith bit is 1
        '''
        forge_key = (1 << 127) | (recover_key << (127 - i))
        forge_key = bin(forge_key)[2:]
        print("forge key:",forge_key)
        #print(len(forge_key))
        forge_key = bin2str(forge_key)
        #print(forge_key)

        WUP = 'test WUP request'
        # type(forge_key): bytes
        # eg. b'100000...00'
        AES = AESCrypto(forge_key)
        eWUP = AES.encrypt(WUP) #encrypted WUP,string
        #print(bin(C_b))
        #print(C_b)
        #msg = [C_b,str2long(eWUP)]
        #print(msg)
        #msg  = pickle.dumps(msg)

        #msg = pickle.loads(msg)
        #print(msg)

        if (response(C_b, eWUP,privateKey) == True):
            recover_key = recover_key + (1 << i)
            print('the {} bit of aes is 1'.format(i))
        else:
            recover_key = recover_key
            print('the {} bit of aes is 0'.format(i))

        #print('--------------------------------------')
    print("recover key:",long2str(recover_key))


def response(C_b,eWUP,privateKey):
    '''
    :param C_b: integer,RSA-encrypted AES key lefting b bits
    :param eWUP: string, encrpted WUP
    :param privateKey: tuple of integer, (n,d)

    :return: response(bool)
    '''
    # decrypt C_b
    K_b = modExp(C_b,privateKey[1],privateKey[0])
    K_b = choose_least_nbits(K_b,128)
    # convert K_b into 128 bit string
    K_b = (bin(K_b)[2:])
    #print("K_b:",K_b)
    K_b = bin2str(K_b)

    AES = AESCrypto(K_b)



    #Note: the result of AES.decrypt is bytes
    if(AES.decrypt(eWUP)==bytes('test WUP request',encoding='utf-8')):
        return True
    else:
        return False

if __name__ == '__main__':
    print('---------------gen RSA key pair--------------')
    #save_rsaKey('project')


    print('-------------attack----------------')
    publicKey = read_rsakey('project_pub.txt')
    privateKey = read_rsakey('project_pri.txt')

    print('--------------gen AES key-------------------')
    #save_aeskey('project',128) #key sizec: 128 bit

    aesKey = read_aeskey('project_aes.txt')
    print("aesKey:",aesKey)

    print('---------compute encrypted AES key------------')
    #convert AES key string to int
    aesKey = str2long(aesKey)

    C = modExp(aesKey,publicKey[1],publicKey[0]) # Type(C): int
    print("C:",C)
    attack(C,publicKey,privateKey)

    veri = read_aeskey('project_aes.txt')

    print("aesKey:",veri)