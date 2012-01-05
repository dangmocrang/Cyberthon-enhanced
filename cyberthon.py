#!/usr/bin/python
#!/usr/bin/python
#Program Name: Cyberthon (Python Cyberoam Client)
#Original Coder AppleGrew // Modded by V1n1t 
#Modified by siddharthaSahu for the new Cyberoam
#License GPL
#Version 2.0
import urllib, sys,time
from xml.dom.minidom import parseString
cyberroamIP = "172.16.1.1" #The IP of the Cyberoam site.
cyberroamPort = "8090" #Set to "" if not using.
cyberroamAddress = cyberroamIP
if cyberroamPort != "":
       cyberroamAddress = cyberroamAddress+":"+cyberroamPort
username = "dcadmin" #Your username
passwd = "passwd" #your password.
sleepsec=180
def login():
       try:
		file = urllib.urlopen("https://"+cyberroamAddress+"/login.xml","mode=191&username="+username+"&password="+passwd+"&a="+(str)((int)(time.time()*1000)))
	except IOError:
		print "Error connecting"
		sys.exit(1)
	data = file.read()
	file.close()
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('message')[0].toxml()
	message=xmlTag.replace('<message>','').replace('</message>','')
	xmlTag = dom.getElementsByTagName('status')[0].toxml()
	status=xmlTag.replace('<status>','').replace('</status>','')
	print message
	loggedIn=True	
	return status

def check():
	try:
		file = urllib.urlopen("https://"+cyberroamAddress+"/live?mode=192&username="+username+"&a="+(str)((int)(time.time()*1000)))
	except IOError:
		print "Error connecting"
		sys.exit(1)
	data = file.read()
	file.close()
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('ack')[0].toxml()
	message=xmlTag.replace('<ack>','').replace('</ack>','')
	print "logged in"
	return message
	
status=login()
if(status.lower()!="live"):
	sys.exit(1)
while True:	
	time.sleep(sleepsec)	
	msg=check()	
	if(msg!="ack"):
		login()
