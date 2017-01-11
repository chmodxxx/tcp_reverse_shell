HTTP Backdoor python :
Low level python network programming using sockets 
There are two files HTTP Server and HTTP client , these are the basics for this project, after that you can use the Data exfiltration scripts to get data from the targeted machine (the data goes through port 80 so it's not blocked by any firewall) the grab command is implemented to get files 
Example : grab*test.txt
there is a setup file to make your files executable (you need the py2exe lib)
Finally there is a persistent backdoor to wrap up things and to make the backdoor start whenever the targeted computer starts, so it's not for one session.
One last thing, this project was tested on LAN network, it can work on WAN network just need to put your Public IP address if it's static, otherwise you can use DYnamic DNS if your Router~Modem Changes the IP whenever you restart it.




~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ By Salah Baddou ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
