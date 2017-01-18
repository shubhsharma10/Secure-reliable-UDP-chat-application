import sys, socket, json, time


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

"""dictAA = {}
msg = "shubham is my name. What are you doing? How is everything with you. Where are you living nowadays? I am living in Boston."
dictAA["s"] = 23
dictAA["f"] = 38436543643745
dictAA["d"] = msg
newData = json.dumps(dictAA)
print newData
print type(newData)
a = len(msg.encode("utf8"))
b = len(newData.encode("utf8"))
print b
print a
print "diff is: "+str(b-a)"""
testmsg = "A" * 70000
msgList = list(chunkstring(testmsg,1000))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_address = "10.0.0.107"
port = 4567
i = 0
length = len(msgList)
for i in range(length):
    #print type(item)
    dictAA = {}    
    dictAA["code"] = "0"
    dictAA["f"] = str(i)
    if(i==length-1):
        dictAA["more"] = str(False)
    else:
        dictAA["more"] = str(True)
    dictAA["d"] = msgList[i]
    newData = json.dumps(dictAA)
    print len(newData.encode("utf8"))
    #print "current index"+retData["f"]
    sock.sendto(newData, (ip_address, port))
    #time.sleep(1)
