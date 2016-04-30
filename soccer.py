import sys
import pygame

sys.path.append('simulator')
sys.path.append('ai')

from robot import Robot
from ball import Ball
from simulation import Simulation
from fake_ai import FakeAI
from soccer_goal import SoccerGoals
from window import run_sim

c1 = FakeAI(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
c2 = FakeAI(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
ai_arr = [c1, c2]

r1 = Robot((100, 100), 0, (255, 0, 0), 40, 5, 10, 5, c1)
r2 = Robot((100, 100), 0, (0, 0, 255), 40, 5, 10, 5, c2)
robots = [r1, r2]

goals = SoccerGoals((0, 0, 0), 100, 4)
updaters = [goals]

ball = Ball((150, 100), 3, (0, 255, 255), 0.999, 2)
dim = (640, 480)
sim = Simulation(robots, ball, updaters, dim)
run_sim(sim, ai_arr, dim)
