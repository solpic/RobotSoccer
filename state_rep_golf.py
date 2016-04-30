import sys

sys.path.append("simulator")
sys.path.append("vision")
sys.path.append("ai")

from tracking_object import DrawableTrackingObject
from state_rep import *
from vision_client import VisionClient
from golf_ai import SimpleGolfAI
from robot import Robot
from ai_server import AIServer
from simulation import Simulation
from math import atan2

ball = DrawableTrackingObject("Ball", (0, 0), (255, 0, 0), 5)
hole = DrawableTrackingObject("Hole", (0, 0), (0, 0, 0), 5)
robot_front = DrawableTrackingObject("RobotFront", (0, 0), (255, 255, 255), 10)
robot_back = DrawableTrackingObject("RobotBack", (0, 0), (128, 128, 128), 10)

ai = SimpleGolfAI()
robot = Robot((0, 0), 0, [0, 0, 0], 1, 1, 1, 1, ai)
ai.robot = robot

ai_server = AIServer("localhost", int(raw_input("What port for AI server? ")), 1)

def state_rep_callback():
    global ball, hole, robot_front, robot_back

    fieldstate = Simulation([], ball, [], (640, 480))
    fieldstate.golf_hole = hole
    robot.pos = (robot_front.pos[0] + robot_back.pos[0])/2, (robot_front.pos[1]+robot_back.pos[1])/2
    robot.orientation = atan2(robot_front.pos[1] - robot_back.pos[1], robot_front.pos[0] - robot_back.pos[0])
    
    print "Ball pos: " + str(ball.pos)
    print "Ball speed: "+ str(ball.speed)

    move = ai.get_move(fieldstate)
    print move
    
    ai_server.move(move[0], move[1])

host = "localhost"
port = int(raw_input("What port? "))

client = VisionClient(host, port, {'Ball': ball, 'Hole': hole, 'RobotFront': robot_front,
                                   'RobotBack': robot_back})

state_rep = StateRepresentation([ball, hole, robot_back, robot_front], client)

state_rep_window(state_rep, (320, 240), state_rep_callback)
