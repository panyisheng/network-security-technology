
import socket
from rsa import *
from aes import *
from convert import *
import pickle

# read RSA private key
privateKey = read_rsakey('project_pri.txt')

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

HOST = ''  # localhost
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()  # receive connect
print ('Connected by', addr)
while True:
    msg = conn.recv(2000000000)

    if not msg:
        break
    print('--------------------------------')
    print('Received ')
    msg = pickle.loads(msg)
    C_b = msg[0]
    eWUP = msg[1]

    response1 = response(C_b,eWUP,privateKey)
    #print(response1)

    if (response1 == True):
        print("a test WUP request! send true response")
    if (response1 == False):
        print("a invalid WUP request! send false response")

    response2 = pickle.dumps(response1)
    conn.sendall(response2)
    print("send success!")

conn.close()
