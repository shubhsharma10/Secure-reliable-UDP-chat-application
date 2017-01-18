import socket, asyncore   # Import socket module
import sys
import json
import threading
import Queue
import time
import argparse
from threading import Thread

class client:
    #initialize method(constructor)
    def __init__(self,username,serverip,port):
        self.username = username
        self.serverip = serverip
        self.port = port
        self.messageList = []
        self.senderQueue = Queue.Queue()
        self.csock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.csock.bind(('',0))
        self.clientport = self.csock.getsockname()[1]
        print "client's port is "+str(self.clientport)

    #sign in method used to sign in to server
    def signin(self):
        msg = {}
        msg["code"] = "1"
        msg["user"] = self.username
        jsonmsg = json.dumps(msg)
        try:
            self.senderQueue.put((jsonmsg,(self.serverip,self.port)))
        except (socket.error, KeyboardInterrupt):
            print "error happened in sign in"
            sys.exit()

    # send reuest message to sever for retriving other client's info
    def sendP2PMessage(self,username,messageList):
        self.messageList = messageList
        msg = {}
        msg["code"] = "3"
        msg["user"] = username
        jsonmsg = json.dumps(msg)
        try:
            self.senderQueue.put((jsonmsg,(self.serverip,self.port)))
        except socket.error:
            #print "error happened"
            sys.exit()

    # reads input from command line        
    def readInput(self):
        while True:
            try:
                command = raw_input("")
                inputList = command.split()
                if(len(inputList) == 1 and inputList[0] == "list"):
                    self.getUserList()
                elif(len(inputList) > 1 and inputList[0] == "send"):
                    self.sendP2PMessage(inputList[1],inputList[2:])
            except socket.error:
                pass

    # listens to socket for any packet received
    # this is a unblocking call
    def listen(self):
        while True:
            try:
                message, address = self.csock.recvfrom(1024)
                msgdict = json.loads(message)
                self.parseJSONMsg(msgdict,address)
            except socket.error:
                pass
    
    # sends meesage through socket          
    def sendMsg(self):
        while True:
            if not self.senderQueue.empty():
                item = self.senderQueue.get()
                self.csock.sendto(item[0],(item[1]))
                #self.senderQueue.task_done()

    # parses any message received from socket
    def parseJSONMsg(self,msgDict,address):
        if msgDict["code"] == "0":
            threadlock.acquire()
            print_msg("hello")
            threadlock.release()
            
        elif msgDict["code"] == "4":
            sender = msgDict["user"]
            msgList = json.loads(msgDict["message"])
            message = " ".join(msgList)
            threadlock.acquire()
            print_msg("<From "+str(address[0])+":"+str(address[1])+":"+str(sender)+">: "+message)
            threadlock.release()
            
        elif msgDict["code"] == "2" :
            userList = json.loads(msgDict["userlist"])
            threadlock.acquire()
            for i in range(len(userList)):
                print_msg(userList[i])
            threadlock.release()
            
        elif msgDict["code"] == "3": 
            clientMsg = {}
            clientMsg["code"] = "4"
            clientMsg["user"] = self.username
            clientMsg["message"] = json.dumps(self.messageList)
            addressList = json.loads(msgDict["addressList"])
            for address in addressList:
                self.senderQueue.put((json.dumps(clientMsg),
                              (address[0],address[1])))
        else:
            sys.exit()

    # message sent to server for retriving user list
    def getUserList(self):
        msg = {}
        msg["code"] = "2"
        jsonmsg = json.dumps(msg)
        try:
            self.senderQueue.put((jsonmsg,(self.serverip,self.port)))
        except socket.error,msg:
            #print "error happened in userlist"
            sys.exit()

def tryParseInt(input):
    try:
        a = int(input)
    except ValueError:
        return False
    return True

def isValidIP(input):
    try:
        socket.inet_aton(input)
    except socket.error:
        return False;
    return True

def vaildateParams(userName,ip,port):
    if(isValidIP(ip)
       and type(userName) == type("")
       and type(port) == type(5)):
        return True
    return False

threadlock = threading.Lock()

# print can be invoked by different thread,so make it a critical resource
def print_msg(message):
    print message
    

def main():
    clientObj = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",dest="userName",type=str,help="username",required=True)
    parser.add_argument("-sip",dest="ip",type=str,help="server ip address",required=True)
    parser.add_argument("-sp",dest="port",type=int,help="server port number",required=True)
    args = parser.parse_args()
    if(vaildateParams(args.userName,args.ip,args.port)):
        threads = []
        try:
            clientObj = client(args.userName,args.ip,args.port)
            clientObj.signin()
            t1 = threading.Thread(target = clientObj.readInput)
            t2 = threading.Thread(target = clientObj.listen)
            t3 = threading.Thread(target = clientObj.sendMsg)
            t1.daemon = True
            t2.daemon = True
            t3.daemon = True
            t3.start()
            t2.start()
            t1.start()
            threads.append(t1)
            threads.append(t2)
            threads.append(t3)
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    main()
