import pygame
from math import cos, sin, pow

class Robot:
    def __init__(self, pos, orientation, color, speed, radius, line_length, turn_speed, ai):
        self.pos = pos
        self.last_pos = pos
        self.orientation = orientation
        self.color = color
        self.speed = speed
        self.radius = radius
        self.line_length = line_length
        self.turn_speed = turn_speed
        self.ai = ai
        ai.robot = self
        
    # Queries AI for move based on field state
    # Execute move, updating position and rotation
    def update(self, field_state, dt):
        # Get move from AI
        move = self.ai.get_move(field_state)
        
        # Execute move
        self.last_pos = self.pos
        d = self.speed*(move[0] + move[1])*dt
        
        # Update position
        self.pos = self.pos[0] + cos(self.orientation)*d, self.pos[1] + sin(self.orientation)*d
        
        # Update orientation
        self.orientation = self.orientation + self.turn_speed*(move[1]-move[0])*dt
        
        ball = field_state.ball_collide(self)
        if ball != 0:
            d_x = ball.pos[0] - self.pos[0]
            d_y = ball.pos[1] - self.pos[1]
            d = pow(pow(d_x, 2) + pow(d_y, 2), 0.5)
            d_x = d_x/d
            d_y = d_y/d
            
            c = d_x*cos(self.orientation) + d_y*sin(self.orientation)
         
            ball.accelerate(d_x*self.speed*ball.hit_constant*c, d_y*self.speed*ball.hit_constant*c)
        
    # Draws the robot using pygame
    def draw(self, window):
        # Draw circle of robot
        pos = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(window, self.color, pos, self.radius)
        
        # Draw orientation line of robot
        end_pos = self.pos[0] + self.line_length*cos(self.orientation), self.pos[1] + self.line_length*sin(self.orientation)
        pygame.draw.line(window, self.color, pos, end_pos, 2)
        