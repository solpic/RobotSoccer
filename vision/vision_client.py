import socket

class VisionClient:
    def __init__(self, address, port, objects):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.objects = objects
        print "Connected"
        self.debug = 0
        
    def receive(self):
        if self.debug == 1:
            print "Receiving message ..."
        count = ''
        while count=='' or count[len(count)-1]!='\n':
            c = self.socket.recv(1)
            if c=='':
                raise RuntimeError("socket connection broken")
            count = count + c
            
        length = int(count[:-1])
        
        if self.debug == 1:
            print "Message length:",length
        
        msg = self.socket.recv(length)
        if msg=='':
            raise RuntimeError("socket connection broken")

        if self.debug == 1:
            print "Message: " + msg
            
        objs = msg.rstrip().split('\n')

        for obj in objs:
            details = obj.split(' ')
            if len(details[0])>0:
                self.objects[details[0]].update(float(details[1]), float(details[2]))
        

