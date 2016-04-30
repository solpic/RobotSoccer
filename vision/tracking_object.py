import pygame

class TrackingObject:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.speed = (0, 0)
        self.pos_smooth = 0.3
        
    def to_string(self):
        return self.name + " " + str(self.pos[0]) + " " + str(self.pos[1])
        
    def update(self, x, y):
        old_pos = self.pos
        
        self.pos = (self.pos[0]*self.pos_smooth + (1.0 - self.pos_smooth)*x, self.pos[1]*self.pos_smooth + (1.0 - self.pos_smooth)*y)
        
        self.speed = self.pos[0] - old_pos[0], self.pos[1] - old_pos[1]
        
class DrawableTrackingObject:
    def __init__(self, name, pos, color, radius):
        self.name = name
        self.pos = pos
        self.color = color
        self.radius = radius
        self.speed = (0, 0)
        self.pos_smooth = 0.3
        
    def draw(self, window):
        pos = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(window, self.color, pos, self.radius)
        
    def update(self, x, y):
        old_pos = self.pos
        
        self.pos = (self.pos[0]*self.pos_smooth + (1.0 - self.pos_smooth)*x, self.pos[1]*self.pos_smooth + (1.0 - self.pos_smooth)*y)
        
        self.speed = self.pos[0] - old_pos[0], self.pos[1] - old_pos[1]