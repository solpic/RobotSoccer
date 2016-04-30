from math import pow
import pygame
from window import display_text

def get_golf_hole(pos, radius, tip_point):
    return GolfHole(pos, radius, tip_point)

class GolfHole:
    def __init__(self, pos, radius, tip_point):
        self.pos = pos
        self.radius = radius
        self.tip_point = tip_point
        
    # Check if ball has fallen into hole
    def update(self, field_state, dt):
        d_x = field_state.ball.pos[0] - self.pos[0]
        d_y = field_state.ball.pos[1] - self.pos[1]
        
        d = pow(pow(d_x, 2) + pow(d_y, 2), 0.5)
        
        if d < self.radius - field_state.ball.radius*self.tip_point and field_state.ball.enabled == 1:
            # Ball has fallen in!
            field_state.ball.enable(0)
            display_text("Ball is in hole!", 3)
            
    def draw(self, window):
        # Draw circle of hole
        pygame.draw.circle(window, (0, 0, 0), self.pos, self.radius)