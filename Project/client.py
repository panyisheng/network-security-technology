# -*- coding: utf-8 -*-
##
# Filename: client.py
# Author: Pan Yisheng
# Description: implement attacker
##
import socket
from rsa import *
from aes import *
from convert import *
import pickle

# read public key
publicKey = read_rsakey('project_pub.txt')

def attack(C,publicKey,recover_key,i):
    '''
    :param C: integer , encrypted AES key
    :param publicKey: tuple of int, (n,e)
    :return: recover_key string
    '''
    #recover_key = 0
    #for i in range(127):
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
    '''
    if (response(C_b, eWUP,privateKey) == True):
        recover_key = recover_key + (1 << i)
        print('the {} bit of aes is 1'.format(i))
    else:
        recover_key = recover_key
        print('the {} bit of aes is 0'.format(i))

    #print('--------------------------------------')
    print("recover key:",long2str(recover_key))
    '''
    return (C_b,eWUP)


HOST = 'localhost'
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print('--------------gen AES key-------------------')
#save_aeskey('project',128) #key sizec: 128 bit

aesKey = read_aeskey('project_aes.txt')
print("aesKey:",aesKey)

#print('---------compute encrypted AES key------------')
#convert AES key string to int
aesKey = str2long(aesKey)

C = modExp(aesKey,publicKey[1],publicKey[0]) # Type(C): int
#print("C:",C)

recover_key = 0
for i in range(127):

    msg = input("do you wanna continue to attack(Y/N):").strip()
    if msg.lower() == 'y' or msg.lower() == 'yes':
        C_b,eWUP = attack(C,publicKey,recover_key,i)
        #print(C_b)
        #print(eWUP)
    elif msg == "exit":
        break
        # s.sendall('Hello Huangpingyi')
    else:
        continue
        #C_b,eWUP = attack()
    #s.sendall(msg.encode())

    msg = pickle.dumps([C_b,eWUP])
    #print(msg)
    s.sendall(msg)
    print("send C_b and eWUP to server")
    response = s.recv(2000000)
    response = pickle.loads(response)
    #print(response)
    if response== True:
        recover_key = recover_key + (1 << i)
        print('the {} bit of aes is 1'.format(i))
    if response == False:
        recover_key = recover_key
        print('the {} bit of aes is 0'.format(i))
    print("recover key:",(bin(recover_key)[2:]).zfill(i+1))
    #print('Received', data.decode())
#print('--------------------------------------')
print("recover key:",long2str(recover_key))
aesKey = read_aeskey('project_aes.txt')
print("original aes key:",aesKey)

s.close()
