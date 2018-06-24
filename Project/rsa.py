'''
Filename: rsa.py
Author: Pan Yisheng
Description: implement RSA algorithm from sketch

'''

import os
import sys
import time
from modular_arithmetic import *
from numberPrime import *
from convert import *

DEFAULT_BLOCKSIZE = 1024 #128 bytes
BYTE = 8 # 8 bits

def save_rsaKey(filename):
    '''
    generate rsa key pair (RSA key size: 1024 bits)
    save pulickey in filename_pub.txt, privatekey in filename_pri.txt

    publicKey: (n,e)
    privateKey: (n,d)

    '''
    decision = 'y'
    if os.path.exists('%s_pub.txt' % (filename)) or os.path.exists('%s_pri.txt' % (filename)):
        decision = input("the key files already exist, do you want to replace it? (y/n)\n")
    if decision.lower() == 'y' or decision.lower() == 'yes':
        n,d,e = GenParms(512,DEBUG=True)
        public_key = (n,e)
        private_key = (n,d)
        with open('%s_pub.txt' % (filename), 'w') as f:
            f.write('%s,%s' % (public_key[0], public_key[1]))
        with open('%s_pri.txt' % (filename), 'w') as f:
            f.write('%s,%s' % (private_key[0], private_key[1]))
        print("Save new keys successfully\n")
    else:
        print("OK, nothing changed\n")

def read_rsakey(filename):
    '''
    read publicKey or privateKey from txt file

    return: integer key pair (n,EorD)

    '''
    with open(filename) as f:
        content = f.read()
        n, EorD = content.split(',')
    return (int(n),int(EorD))

def expMod_Blocks(blocks,key):
    '''
    encrypt or decrypt substring blocks
    compute pow(block,EorD,n) for blocks

    :param blocks: list of integer(substr)
    :param key: PrivateKey or PublicKey (tuple)
    :return: list of integer
    '''
    expBlocks = []
    for block in blocks:
        expBlocks.append(modExp(block,key[1],key[0]))
    return expBlocks

def rsa_encrypt(message,publicKey,blocksize = DEFAULT_BLOCKSIZE):
    '''
    encrypt the message into encrypted blocks of integer

    :param message: string
    :param publicKey: tuple of integer (n,e)
    :param blocksize: block contain blocksize//bytes char (Default: 128 bytes)

    :return: list of integer (encrypted substr)

    '''
    blocks = str2block(message,blocksize = blocksize)
    eblocks = expMod_Blocks(blocks,publicKey)

    return eblocks

def rsa_decrypt(eblocks,privateKey):
    '''
    decrypt the encrypted blocks into string

    :param eblocks: list of integer
    :param privateKey: tuple of integer (n,d)

    :return:decrpted string
    '''
    blocks = expMod_Blocks(eblocks,privateKey)
    str = block2str(blocks)

    return str


if __name__ == '__main__':
    print('--------gen RSA key-------------')
    save_rsaKey('myrsa')

    privateKey = read_rsakey('project_pri.txt')
    publicKey = read_rsakey('project_pub.txt')

    print('--------verify RSA key pair---------- ')
    e = modExp(142628892054802739147325988843996338543,publicKey[1],publicKey[0])
    print(modExp(e,privateKey[1],privateKey[0]))

    print("------------test---------------")
    message = 'hello world! I love China. 1+2=3'

    emsg = rsa_encrypt(message,publicKey)

    rmsg = rsa_decrypt(emsg,privateKey)

    print(rmsg)

