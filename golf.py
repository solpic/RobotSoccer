import sys
import pygame

sys.path.append('simulator')
sys.path.append('ai')
sys.path.append('math')

from robot import Robot
from ball import Ball
from simulation import Simulation
from fake_ai import FakeAI
from golf_ai import SimpleGolfAI
from golf_hole import GolfHole
from window import run_sim

# c1 = FakeAI(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
c1 = SimpleGolfAI()
ai_arr = [c1]

r1 = Robot((100, 300), 0, (255, 0, 0), 40, 5, 10, 2, c1)
robots = [r1]

h1 = GolfHole((200, 100), 5, 0.5)
updaters = [h1]

ball = Ball((250, 150), 3, (0, 255, 255), 0.99, 1.2)
dim = (640, 480)

sim = Simulation(robots, ball, updaters, dim)
sim.golf_hole = h1

run_sim(sim, ai_arr, dim)
