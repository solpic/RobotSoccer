import sys
sys.path.append("ai")
from ai_server import AIServer

ai_server = AIServer("localhost", 10041, 1)

while 1:
    ai_server.move(-1, 0.1)
