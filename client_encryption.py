import Crypto
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


def do_encrypt(message,secret):
    obj = AES.new(secret, AES.MODE_CBC,IV='needs to be = 16')
    ciphertext = obj.encrypt(message)
    return ciphertext


def do_decrypt(ciphertext,secret):
    obj2 = AES.new(secret, AES.MODE_CBC,IV='needs to be = 16')
    message = obj2.decrypt(ciphertext)
    return message


private_key = RSA.generate(1024)

#print(private_key.exportKey())

public_key = private_key.publickey()

send_public=public_key.exportKey()

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('127.0.0.1',7071))

sock.send(send_public)

secret_enc=sock.recv(1024)

secret=private_key.decrypt(secret_enc)


sock.send(secret)

sock.send(do_encrypt('this is blablaaa',secret))



