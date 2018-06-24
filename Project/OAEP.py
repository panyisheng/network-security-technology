#!/usr/bin/python

'''
Filename: OAEP
Description: Optimal asymmetric encryption padding implementation
'''

import hashlib  # sha-256
import binascii  # Used for coverting between Ascii and binary
from random import SystemRandom  # Generate secure random numbers

# constants
nBits = 1024
k0BitsInt = 256
k0BitsFill = '0256b'
errors = 'surrogatepass'
encoding = 'utf-8'

'''
Helper function to change a Character string into a binary string.
Making sure to have full byte output (Don't drop leading 0's)
Funct: CharsToBinary
Arguments: msg, a Charater string
		   errors, used when encoding the msg
return: bits, a binary string'''


def CharsToBinary(msg, errors=errors):
    bits = bin(int.from_bytes(msg.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


'''
Helper function to change a binary string into a character string.
Funct: BinaryToChars
Arguments: msg, a Charater string
		   errors, used when decoding the bytes
return: n, a character string'''


def BinaryToChars(bits, errors):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def pad(msg):
    '''
    :param msg: string
    :return: bin string , bin msg string length
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

    return x + y,len(binMsg)


def unpad(msg,bits):
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
    msgWith0s = msgWith0s[0:bits] #remove the padding 0
    print("msgw",msgWith0s)
    print(type(msgWith0s))
    return BinaryToChars(msgWith0s, errors)


'''================================TESTING======================================'''

if __name__ == '__main__':

    msg = "hello world"

    binmsg = CharsToBinary(msg,errors)

    #print("ORIGINAL MSG:\n", msg, "\n")

    #print(binmsg)



    #print(len(CharsToBinary(msg,errors)),"\n")


    output,Bits = pad(msg)
    print(type(output))
    print(output)
    print(int(output,2))
    print(len(output))

    print(Bits)

    '''
    print("PADDED MSG:\n", output,
          "\n\nLENGTH OF PADDED MSG:\n", len(output),
          "\nEXPECTED LENGTH:\n", nBits)
    '''
    result = unpad(output,Bits)

    print("\nUNPADDED MSG:\n", result)

    #print(len(result))