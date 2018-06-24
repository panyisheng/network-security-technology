'''
Filename : convert.py
Author: Pan Yisheng
Description： some format convert function
'''

DEFAULT_BLOCKSIZE = 1024 # 128 bytes
BYTES = 8  # 8 bits


def str2long(string):
    '''
    convert string to long int

    :param string:
    :return: int
    '''
    long = 0
    for char in string:
        long = ord(char) + (long<<8)
    return long

def str2block(string,blocksize = DEFAULT_BLOCKSIZE):
    '''
    divide string into fixed-size(blocksize) substring
    Then convert substring to int

    :param string:
    :return list of integer(substring)
    '''
    blocks = []
    for start in range(0,len(string),blocksize//BYTES):
        # convert string of block to int
        block = 0
        end = min(start+ blocksize//BYTES,len(string))
        for char in string[start:end]:
            block = ord(char) + (block<<8)
        blocks.append(block)
    return blocks

def long2str(long):
    '''
    convert long int to substring

    :param int:
    :return: string
    '''

    # fisrt convert int into bin string
    bits = bin(long)[2:]
    str = ''

    for i in range(len(bits), 0, -8):
        if i - 8 < 0:
            byte = int(bits[0:i], 2)
        else:
            byte = int(bits[i - 8:i], 2)
        byte = chr(byte)
        # print(type(byte))
        # print(int(bits[i-8:i],2))
        str = byte + str  # insert in list head
    return str

def block2str(blocks):
    '''
    recover substring block(integer) into string

    :param blocks: list of integer(substring)
    :return: recovered string
    '''
    str = ''
    for block in blocks:
        str += long2str(block)
    return str

def bin2str2(bits):
    '''
    convert bin string ('100.000') to str
    for purpose of adapting AES key

    :param bin: bin string
    :return: enconde str
    '''
    str = ''
    for i in range(len(bits), 0, -8):
        if i - 8 < 0:
            byte = int(bits[0:i], 2)
        else:
            byte = int(bits[i - 8:i], 2)
        byte = chr(byte)
        # print(type(byte))
        # print(int(bits[i-8:i],2))
        str = byte + str

    return str

def bin2str(bin_key):
    div_key = [bin_key[i:i+8] for i in range(0,len(bin_key),8)]
    key = bytes()
    for div in div_key:
        binK = '0b' + ''.join(div)
        intK = int(binK, 2)
        num = bytes([intK])
        key += num
    return key


def choose_least_nbits(integer,n):
    '''
    choose the least n bits of interger
    integer & '1'* n

    :param integer:
    :param n:
    :return:  masked integer
    '''

    # maskbit: '1'*n (integer)
    maskbit = 1
    for i in range(n-1):
        maskbit = (maskbit << 1) | 1

    integer = integer & maskbit
    return integer