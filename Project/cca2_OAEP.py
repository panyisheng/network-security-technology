'''
Filename: cca2_OAEP.py
Author: Pan Yisheng
Description: implement ccsa2 attack off-line with OAEP
'''

from rsa import *
from aes import *
from convert import *

import hashlib  # sha-256
import binascii  # Used for coverting between Ascii and binary
from random import SystemRandom  # Generate secure random numbers

# constants
nBits = 1024
k0BitsInt = 256
k0BitsFill = '0256b'
errors = 'surrogatepass'
encoding = 'utf-8'
aesKeySize = 128




def CharsToBinary(msg, errors=errors):
    '''
    Helper function to change a Character string into a binary string.
    Making sure to have full byte output (Don't drop leading 0's)
    Funct: CharsToBinary
    Arguments: msg, a Charater string
    		   errors, used when encoding the msg
    return: bits, a binary string'''

    bits = bin(int.from_bytes(msg.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def pad(msg):
    '''
    :param msg: string, original msg
    :return: bin string , bin original msg string length
    '''

    '''
    Create two oracles using sha-256 hash function.
    oracle1 is our first hash function used. Used to hash a random integer.
    oracle2 is the second hash function used. Used to hash the result of XOR(paddedMsg, hash(randBitStr))'''
    oracle1 = hashlib.sha256()
    oracle2 = hashlib.sha256()

    '''
    Generate a random integer that has a size of k0bits. Format the random int as a binary string making 
    sure to maintain leading zeros with the K0BitsFill argument.'''
    randBitStr = format(SystemRandom().getrandbits(k0BitsInt), k0BitsFill)

    '''
    Change our msg string to a binary string. '''
    binMsg = CharsToBinary(msg, errors)

    '''
    If the input msg has a binary length shorter than (nBits-k0Bits) then append k1Bits 0's to the end of the msg.
    Where k1Bits is the number of bits to make len(binMsg) = (nBits-k0Bits).'''
    if len(binMsg) <= (nBits - k0BitsInt):
        k1Bits = nBits - k0BitsInt - len(binMsg)
        zeroPaddedMsg = binMsg + ('0' * k1Bits)
    else:
        zeroPaddedMsg = binMsg
    '''
    Use the hashlib update method to pass the values we wish to be hashed to the oracle. Then use
    the hashlib hexdigest method to hash the value placed in the oracle by the update method, and
    return the hex repersentation of this hash. Change our hash output, zeroPaddedMsg, and
    randBitStr to integeres to use XOR operation. Format the resulting ints as binary strings.
    Hashing and XOR ordering follows OAEP algorithm.'''
    oracle1.update(randBitStr.encode(encoding))
    x = format(int(zeroPaddedMsg, 2) ^ int(oracle1.hexdigest(), 16), '0768b')
    oracle2.update(x.encode(encoding))
    y = format(int(oracle2.hexdigest(), 16) ^ int(randBitStr, 2), k0BitsFill)

    return x + y, len(binMsg)


def unpad(msg, bits):
    '''
    unpad message
    :param msg: bin string, padded msg
    :param bits: int, bin original msg string length
    :return: bin original msg string
    '''

    '''
    Create two oracles using sha-256 hash function.
    oracle1 is our first hash function used. Used to hash a random integer.
    oracle2 is the second hash function used. Used to hash the result of XOR(paddedMsg, hash(randBitStr))'''
    oracle1 = hashlib.sha256()
    oracle2 = hashlib.sha256()

    x = msg[0:768]
    y = msg[768:]

    oracle2.update(x.encode(encoding))
    r = format(int(y, 2) ^ int(oracle2.hexdigest(), 16), k0BitsFill)

    oracle1.update(r.encode(encoding))
    msgWith0s = format(int(x, 2) ^ int(oracle1.hexdigest(), 16), '0768b')
    if(msgWith0s[bits:nBits-k0BitsInt]=='0'*(nBits-k0BitsInt)):
        check = True
    else:
        check = False
    msgWith0s = msgWith0s[0:bits]  # remove the padding 0
    #print("msgw", msgWith0s)
    #print(type(msgWith0s))
    return msgWith0s,check

def attack(C,publicKey,privateKey,original_msg):
    '''

    :param C: int,encrypted padded msg
    :param publicKey: tuple of int, (n,e)
    :param privateKey: tuple of int, (n,d) for server
    :param origial_msg: bin string, for verify whether attack success

    :return:
    '''
    recover_msg = 0
    for i in range(nBits-1):
        print('------------attack {}-------------'.format(i))
        '''
        try to gain the ith bit(0 means the least significant bit)
        C_b = C << (nBits-1-i)*e 
        '''
        be = (nBits-1-i)*publicKey[1]
        C_b = C << be

        '''
        forge padded msg
        Then unpad forged padded msg as K_b 
        Finally encrtpy test WUP with K_b
        We assume the ith msg is 1 
        '''

        forge_msg = (1 << (nBits-1)) | (recover_msg << (nBits-1 - i))
        forge_msg = (bin(forge_msg)[2:]).zfill(nBits)
        K_b,_ = unpad(forge_msg,aesKeySize)

        AES = AESCrypto(bin2str(K_b))
        WUP = 'test WUP request'
        eWUP = AES.encrypt(WUP)

        result,check = response(C_b, eWUP,privateKey)
        if(check==False):
            print("OAEP check fail,attack fail!")
            break
        if (result == True):
            recover_msg = recover_msg + (1 << i)
            cur_bits = 1
            print('the {} bit of aes is 1'.format(i))
        else:
            recover_msg = recover_msg
            cur_bits = 0
            print('the {} bit of aes is 0'.format(i))

        if(cur_bits == original_msg[len(original_msg)-1-i]):
            continue
        else:
            print("attack fail!")
            break
    #convert recover msg from int to bin string
    recover_msg = bin(recover_msg)[2:].zfill(nBits)
    #print("recover_aesKey:",bin2str(unpad(recover_msg,aesKeySize)))

def response(C_b,eWUP,privateKey):
    '''

    :param C_b:
    :param eWUP:
    :param privateKey:
    :return:
    '''
    original_msg = modExp(C_b, privateKey[1], privateKey[0])
    original_msg = choose_least_nbits(original_msg, nBits) #int

    #convert int to binstring
    original_msg = (bin(original_msg)[2:]).zfill(nBits)

    K_b,check = unpad(original_msg,aesKeySize) # unpad result: bin string
    # convert K_b into 128 bit string
    # print("K_b:",K_b)

    K_b = bin2str(K_b)

    AES = AESCrypto(K_b)

    # Note: the result of AES.decrypt is bytes
    if (AES.decrypt(eWUP) == bytes('test WUP request', encoding='utf-8')):
        return True,check
    else:
        return False,check

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

    print('---------compute encrypted padded msg------------')
    original_msg,_ = pad(aesKey) # bin string

    original_msg_int = int(original_msg,2) #integer

    C = modExp(original_msg_int,publicKey[1],publicKey[0]) # Type(C): int
    print("C:",C)
    attack(C,publicKey,privateKey,original_msg)

    veri = read_rsakey('project_aes.txt')

    print("aesKey:",veri)