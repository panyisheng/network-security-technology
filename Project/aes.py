'''
Filename: rsa.py
Author: Pan Yisheng
Description: implement AES algorithm with pycrypto

Note: AES key need to be string!!!!
'''

from Crypto.Cipher import AES
import base64
import random
import string
import os

class AESCrypto():
    """This is an AES Crypto class

    Only two functions: encrypt and decrypt
    There is the document of Crypto.Cipher AES :
    https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.AES-module.html

    Attributes:
        key: 128, 192, or 256 bits long string not integer
        mode: The chaining mode to use for encryption or decryption. Default is MODE_ECB.
    """
    def __init__(self, key, mode = AES.MODE_ECB):
        self.key = key
        self.mode = mode
        self.cryptor = AES.new(self.key,self.mode)

    def encrypt(self, text):
        if len(text) % 16 != 0:
            text = text + str((16 - len(text) % 16) * '0')
        ciphertext = self.cryptor.encrypt(text)
        # return string
        return base64.b64encode(ciphertext).decode()

    def decrypt(self, text):
        text = base64.b64decode(text)
        plain_text  = self.cryptor.decrypt(text)
        #print(type(plain_text))
        # return bytes type
        # when attack, some test may can't convert into string due to left operation
        # some hex may not match any character in ascii
        return plain_text

def gen_aeskey(keysize):
    '''
    generate keysize//BYTE random char as AES key

    :param keysize: 128/192/256 bits
    :return: string
    '''
    aes_key = ''.join(random.sample(string.ascii_letters + string.digits, keysize // 8))
    return aes_key

def save_aeskey(filename,keysize):
    '''
    save aes key in filename_aes.txt

    :param filename: string
    :param keysize: 128/192/256 bits
    '''
    decision = 'y'
    if os.path.exists('%s_aes.txt' % (filename)):
        decision = input("the key files already exist, do you want to replace it? (y/n)\n")
    if decision.lower() == 'y' or decision.lower() == 'yes':
        aes_key = gen_aeskey(keysize)
        with open('%s_aes.txt' % (filename), 'w') as f:
            f.write('%s' % aes_key)
        print("Save new keys successfully\n")
    else:
        print("OK, nothing changed\n")

def read_aeskey(filename):
    '''
    read aes key

    :return: string
    '''
    with open(filename) as f:
        content = f.read()
    return content


if __name__ == '__main__':
    bits =  '0'*128

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

    print(str)


    pc = AESCrypto(str) #初始化密钥
    #e = pc.encrypt('This is the wup.')
    e = pc.encrypt('test WUP request')
    d = pc.decrypt(e) #解密
    print("加密:",e)
    print("解密:",d)
    if(d == bytes('test WUP request',encoding='utf-8')): print("1")
    #save_aeskey('project',128)
    print(read_aeskey('project_aes.txt'))

