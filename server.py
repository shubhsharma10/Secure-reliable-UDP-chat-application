import socket, sys, json, argparse
from threading import Thread
# Import socket module


class server:    
    def __init__(self,port):
        self.port = port
        self.users = {}
        self.sock = None
    
    def start(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)# Create a udp socket object
        self.sock.bind(('', self.port))# Bind to the port
        self.sock.setblocking(0)
        while True:
            try:
                message, address = self.sock.recvfrom(1024)
                print "message received"
                msgdict = json.loads(message)
                self.parseJSONMsg(msgdict,address)
            except socket.error:
                pass
            except KeyboardInterrupt:
                sys.exit()

    def parseSignInMsg(self,message,address):
        self.users[address] = message["user"]
        """newmsg = {}
        newmsg["code"] = "0"]
        for address in self.users.values():
            self.sock.sendto(json.dumps(newmsg),address)"""

    def replyToList(self,address):
        newmsg = {}
        newmsg["code"] = "2"
        newmsg["userlist"] = json.dumps(list(set(self.users.values())))
        self.sock.sendto(json.dumps(newmsg),address)

    def replyToP2P(self,message,address):
        username = message["user"]
        if(username in self.users.values()):
            msg = {}
            msg["code"] = "3"
            msg["user"] = username
            msg["addressList"] = json.dumps([item[0] for item in self.users.items()
                                             if item[1] == username])            
            self.sock.sendto(json.dumps(msg),address)

    def parseJSONMsg(self,message,address):
        try:
            code = message["code"]
            if(code == "1"):
                #sign in
                self.parseSignInMsg(message,address)
            elif(code == "2"):
                #list users
                self.replyToList(address)
            elif(code == "3"):
                self.replyToP2P(message,address)                
        except socket.error:
            pass   

    


def tryParseInt(input):
    try:
        a = int(input)
    except ValueError:
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp",dest="port",type=int,help="server port number",required=True)
    args = parser.parse_args()
    portNo = args.port    
    serverObj = server(portNo)
    serverObj.start()


if __name__ == "__main__":
    main()
