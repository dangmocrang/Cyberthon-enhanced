#!/usr/bin/python
#!/usr/bin/python
#Program Name: Cyberthon (Python Cyberoam Client)
#Original Coder AppleGrew // Modded by V1n1t
#License GPL
#Version 1.3
cyberroamIP = "172.16.1.1" #The IP of the Cyberoam site.
cyberroamPort = "8090" #Set to "" if not using.
username = "dcadmin" #Your username
passwordFile = "/home/vinit/.passwd" #Path file containing a single string, your password.
sleeptime = 0 #in minutes or set to 0, it will then parse this value from the cyberoam returned page dynamically.
never_quit = True #Once started cyberthon will never, even when the cyberoam server cannot be connected.
import sys
silent = False
nogui = False
for arg in sys.argv:
       if "-silent" == arg:
            silent = True
       if "-nogui" == arg:
            nogui = True
#Parsing and logging in too.
import sgmllib
class MyCyberroamParser(sgmllib.SGMLParser):
   "A simple parser class."
   def parse(self, s):
       "Parse the given string 's'."
       self.feed(s)
       self.close()
   def __init__(self, verbose=0):
       "Initialise an object, passing 'verbose' to the superclass."
       sgmllib.SGMLParser.__init__(self, verbose)
       self.required_entities = ['message','loginstatus','liverequesttime']
       self.frames_attr = []
       self.in_required_entity = False
       self.current_entity = ""
       self.entity_values = {}
   def do_frame(self, attributes):
       for name, value in attributes:
          if name == "src":
               self.frames_attr.append(value)
   def unknown_entityref(self,ref):
       self.current_entity = ref
       if ref in self.required_entities:
            self.in_required_entity=True
   def handle_data(self, data):
       "Try to get the value of entity &message. Used in 2nd pass of parsing."
       if self.in_required_entity:
           self.entity_values[self.current_entity] = data[1:] #To remove the preceeding =
           self.in_required_entity = False
   def get_src(self,index=-1):
       "Return the list of src targets."
       if index == -1:
            return self.frames_attr
       else:
            return self.frames_attr[index]
import urllib, sgmllib,time,commands,os
pf = open(passwordFile)
passwd = pf.readline()
pf.close()
if passwd[-1] == '\n': #Removing terminating newline character.
       passwd = passwd[:-1]
cyberroamAddress = cyberroamIP
if cyberroamPort != "":
       cyberroamAddress = cyberroamAddress+":"+cyberroamPort
sec2sleep = 60*sleeptime
lastmsg = ""
msgChanged = True
lastMsgWasFailMsg = False
sec2sleepOnError = 6
while True:
       try:
       # Logging in and fetching the Cyberroam login page.
                 f = urllib.urlopen("http://"+cyberroamAddress+"/corporate/servlet/CyberoamHTTPClient","mode=191&isAccessDenied=null&url=null&message=&username="+username+"&password="+passwd+"&saveinfo=saveinfo&login=Login")
                 sec2sleepOnError = 6
       except IOError, (errno, strerror):
                 if not silent:
                      print "Connection to Cyberoam server timed out. Error(%s): %s" % (errno, strerror)
                 if sec2sleepOnError > 30:
                      if not silent:
                           if nogui:
                                print "Quitting program."
                           else:
                                if never_quit:
                                       if not lastMsgWasFailMsg:
                                               os.popen('zenity --info --text="Failed to connect to server, but I am NOT quitting." --title="Cyberthon" >/dev/null')
                                       lastMsgWasFailMsg = True
                                else:
                                       commands.getoutput('zenity --info --text="Could not connect to the server. Quitting program." --title="Cyberthon"')
                      if not never_quit:
                           sys.exit(1)
                      else:
                           sec2sleepOnError = 6
                 if not silent:
                      print "Retrying in %s seconds" % sec2sleepOnError
                 time.sleep(sec2sleepOnError)
                 sec2sleepOnError = sec2sleepOnError*2
                 continue
       s = f.read()
       # Try and process the page.
       # The class should have been defined first, remember.
       myparser = MyCyberroamParser()
       myparser.parse(s)
       # Get the the src targets. It contains the status message. And then parse it again for entity &message.
       qindex = myparser.get_src(1).index('?')
       srcstr = myparser.get_src(1)[:qindex+1]+'&'+myparser.get_src(1)[qindex+1:]
       myparser.parse(srcstr)
       message = myparser.entity_values['message']
       if lastmsg != message or lastMsgWasFailMsg:
            lastmsg = message
            msgChanged = True
            lastMsgWasFailMsg = False
       if (not silent) and msgChanged:
            msgChanged = False
            msg=''
            i=0
            while i < len(message): #Converting hex nos. to characters.
                 t=message[i]
                 if message[i]=='%':
                      no=int(message[i+1:i+3],16)
                      t=chr(no)
                      i=i+2
                 msg=msg+t
                 i=i+1
            message = ""
            for x in msg:#Changing all + to space.
                 if x == '+':
                      x = " "
                 message=message+x
            if nogui:
                 print message
            else:
                 os.popen('zenity --info --text="From Cyberoam: '+message+'" --title="Cyberthon" >/dev/null')
       if myparser.entity_values['loginstatus'].lower()!="true":
            break;
       if sleeptime==0:
            sec2sleep = int(myparser.entity_values['liverequesttime'])
       time.sleep(sec2sleep)
