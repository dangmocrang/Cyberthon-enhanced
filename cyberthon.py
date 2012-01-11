#!/usr/bin/python
#Program Name: Cyberthon (Python Cyberoam Client)
#Original Coder AppleGrew // Modded by V1n1t 
#Modified by siddharthaSahu for the new Cyberoam
#License GPL
#Version 3.0
import urllib, sys,time, getpass,base64
from xml.dom.minidom import parseString
cyberoamAddress = "" #the cyberoam login page address
username = "" #Your username
passwd = "" #your password.
sleepsec=180 #login status check every 3 minutes
def readfile(filename):
	try:
		infile=open(filename,"rU")
	except IOError:
		return -1
	a=infile.readline()
	if(a==""):
		print "eeor" 
		return -1
	cyberoamAddress=a.rstrip("\r\n")
	a=infile.readline()
	if(a==""):
		print "eeor" 
		return -1
	username=a.rstrip("\r\n")
	a=infile.readline()
	if(a==""):
		print "eeor" 
		return -1
	passwd=base64.b64decode(a.rstrip("\r\n"))
	infile.close()
	return 0

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
	
def logout():
	try:
		file = urllib.urlopen(cyberoamAddress+"/logout.xml","mode=193&username="+username+"&a="+(str)((int)(time.time()*1000)))
	except IOError:
		print "Error connecting"
		sys.exit(1)
	data = file.read()
	file.close()
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('message')[0].toxml()
	message=xmlTag.replace('<message>','').replace('</message>','')
	print message

def printhelp():
	print "Usage:\n\tli\t\t\t\tlogin interactively\n\tli -f ./cyberoam.config\t\tlogin with path to configuration file\n\tlo\t\t\t\tlogout"

if(len(sys.argv)>1):
	if(sys.argv[1]=="li"):
		if(len(sys.argv)>2 and sys.argv[2]=="-f"):
			if(len(sys.argv)>3 and sys.argv[3]!=""):
				try:
					infile=open(sys.argv[3],"rU")
				except IOError:
					print "Error reading file"
					sys.exit(1)
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				cyberoamAddress=a.rstrip("\r\n")
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				username=a.rstrip("\r\n")
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				passwd=base64.b64decode(a.rstrip("\r\n"))
				infile.close()
			else:
				print "no configuration file"
				sys.exit(1)
		else:
			try:
				infile=open("cyberoam.config","rU")
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				cyberoamAddress=a.rstrip("\r\n")
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				username=a.rstrip("\r\n")
				a=infile.readline()
				if(a==""):
					print "Error reading file"
					sys.exit(1)
				passwd=base64.b64decode(a.rstrip("\r\n"))
				infile.close()
			except IOError:
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
				try:
					ofile=open("cyberoam.config","w")
					ofile.write(cyberoamAddress+"\n"+username+"\n"+base64.b64encode(passwd))
					ofile.close()
				except IOError:
					print "Warning: could not saving configuration"
		print "Logging in "+username
		status=login()
		if(status.lower()!="live"):
			sys.exit(1)
		while True:	
			time.sleep(sleepsec)	
			msg=check()	
			if(msg!="ack"):
				login()
			print username+" is logged in"
	elif(sys.argv[1]=="lo"):
		try:
			infile=open("cyberoam.config","rU")
			a=infile.readline()
			if(a==""):
				a=raw_input("Enter full cyberoam site Address (Default: https://172.16.1.1:8090): ")
				if(a==""):
					a="https://172.16.1.1:8090"
				username=raw_input("Enter username: ")
			cyberoamAddress=a.rstrip("\r\n")
			a=infile.readline()
			if(a==""):
				a=raw_input("Enter full cyberoam site Address (Default: https://172.16.1.1:8090): ")
				if(a==""):
					a="https://172.16.1.1:8090"
				username=raw_input("Enter username: ")
			username=a.rstrip("\r\n")			
			infile.close()			
		except IOError:
			a=raw_input("Enter full cyberoam site Address (Default: https://172.16.1.1:8090): ")
			if(a==""):
				a="https://172.16.1.1:8090"
			username=raw_input("Enter username: ")
		print "Logging out "+username
		logout()
	else:
		printhelp()
else:
	printhelp()
