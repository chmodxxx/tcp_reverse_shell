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


secret='SECRET P@$$w0rd_ N33DS TO B3 b!G'

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(('127.0.0.1',7071))

sock.listen(1)

conn,add=sock.accept()

print 'got a connection '

client_public_text=conn.recv(1024)

client_public=RSA.importKey(client_public_text)

secret_encrypted=client_public.encrypt(secret, None)

conn.send(secret_encrypted[0])

client_secret=conn.recv(1024)
if client_secret==secret:
	print 'The secret key was sent successfully'
print do_decrypt(conn.recv(1024),secret)
