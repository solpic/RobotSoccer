import socket

class AIServer:
    def __init__(self, address, port, connections):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((address, port))
        self.socket.listen(connections)
        
        self.connections = []

        while len(self.connections) < connections:
            (clientsocket, address) = self.socket.accept()
            self.connections.append(clientsocket)
            print "Received client #"+str(len(self.connections))
        
        
    def broadcast(self, msg):
        for sock in self.connections:
            sent = sock.send(msg)
            if sent==0:
                raise RuntimeError("socket connection broken")

    def move(self, motor1, motor2):
        msg = str(motor1) + " " + str(motor2) + "\n"
        print "Sending: "+msg
        self.broadcast(msg)
        
