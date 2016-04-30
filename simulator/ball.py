import pygame

class Ball:
    def __init__(self, pos, radius, color, drag, hit_constant):
        self.pos = pos
        self.last_pos = pos
        self.radius = radius
        self.color = color
        self.drag = drag
        self.speed = 0, 0
        self.hard_physics = 1   # Don't let ball intersect with robots
        self.enabled = 1
        self.hit_constant = hit_constant
        
    def update(self, field_state, dt):
        if self.enabled == 1:
            self.last_pos = self.pos
            self.pos = self.pos[0] + self.speed[0]*dt, self.pos[1] + self.speed[1]*dt
            self.speed = self.speed[0]*self.drag, self.speed[1]*self.drag
        
    def draw(self, window):
        # Draw circle of ball
        pos = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(window, self.color, pos, self.radius)
        
    def accelerate(self, x, y):
        self.speed = self.speed[0] + x, self.speed[1] + y
        
    def enable(self, enabled):
        self.enabled = enabled