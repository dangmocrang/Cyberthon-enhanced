#!/usr/bin/python
#Program Name: Cyberthon (Python Cyberoam Client)
#Original Coder AppleGrew // Modded by V1n1t 
#Modified by siddharthaSahu for the new Cyberoam
#License GPL
#Version 2.5
import urllib, sys,time, getpass,base64
from xml.dom.minidom import parseString
cyberoamAddress = "" #the cyberoam login page address
username = "" #Your username
passwd = "" #your password.
sleepsec=180 #login status check every 3 minutes
if(len(sys.argv)>1):
	if(sys.argv[1]=="-f" and sys.argv[2]!=""):
		try:
			infile=open(sys.argv[2],"rU")
		except IOError:
			print "could not open file"
			sys.exit(1)
		a=infile.readline()
		if(a==""):
			print "error reading file"
			sys.exit(1)
		cyberoamAddress=a.rstrip("\r\n")
		a=infile.readline()
		if(a==""):
			print "error reading file"
			sys.exit(1)
		username=a.rstrip("\r\n")
		a=infile.readline()
		if(a==""):
			print "error reading file"
			sys.exit(1)
		passwd=base64.b64decode(a.rstrip("\r\n"))
		infile.close()
else:
	a=raw_input("Enter full cyberoam site Address (Default: https://172.16.1.1:8090): ")
	if(a==""):
		a="https://172.16.1.1:8090"
	cyberoamAddress=a
	a=raw_input("Enter user name: ")
	if(a==""):
		print "empty input. program terminated"
		sys.exit(1)
	username=a
	a=getpass.getpass("Enter password: ")
	if(a==""):
		print "empty input. program terminated"
		sys.exit(1)
	passwd=a
	a=raw_input("Save to file ? [y/n]: ")
	if(a=="y"):
		try:
			ofile=open("cyberoam.config","w")
			ofile.write(cyberoamAddress+"\n"+username+"\n"+base64.b64encode(passwd))
			ofile.close()
		except IOError:
			print "Error saving file"
def login():
	try:
		file = urllib.urlopen(cyberoamAddress+"/login.xml","mode=191&username="+username+"&password="+passwd+"&a="+(str)((int)(time.time()*1000)))
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
		file = urllib.urlopen(cyberoamAddress+"/live?mode=192&username="+username+"&a="+(str)((int)(time.time()*1000)))
	except IOError:
		print "Error connecting"
		sys.exit(1)
	data = file.read()
	file.close()
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('ack')[0].toxml()
	message=xmlTag.replace('<ack>','').replace('</ack>','')
	return message
	
status=login()
if(status.lower()!="live"):
	sys.exit(1)
while True:	
	time.sleep(sleepsec)	
	msg=check()	
	if(msg!="ack"):
		login()
