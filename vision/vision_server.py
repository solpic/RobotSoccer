import socket

class VisionServer:
    def __init__(self, address, port, connections, objects):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((address, port))
        self.socket.listen(connections)
        
        self.connections = []
        self.objects = objects

        print "Waiting for connections, 0/" + str(connections) + " . . ."
        while len(self.connections) < connections:
            (clientsocket, address) = self.socket.accept()
            self.connections.append(clientsocket)
            print "Received client #"+str(len(self.connections))
        
        
    def broadcast(self, msg):
        final_msg = str(len(msg)) + "\n" + msg
        for sock in self.connections:
            sent = sock.send(final_msg)
            if sent==0:
                raise RuntimeError("socket connection broken")

    def update(self):
        msg = ""
        for obj in self.objects:
            msg = msg + obj.to_string() + "\n"

        self.broadcast(msg)
        
