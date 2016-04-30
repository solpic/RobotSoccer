import pygame
from window import display_text

class SoccerGoals:
    def __init__(self, color, height, width):
        self.color = color
        self.height = height
        self.width = width
        
    def draw(self, window):
        top = int(window.get_height()*0.5 - self.height*0.5)
        goal1 = pygame.Rect(0, top, self.width, self.height)
        goal2 = pygame.Rect(window.get_width() - self.width, top, self.width, self.height)
        pygame.draw.rect(window, self.color, goal1)
        pygame.draw.rect(window, self.color, goal2)
        
    
    def update(self, field_state, dt):
        # Check if ball has hit wall on either side of goal
        
        dim = field_state.dimensions
        ball = field_state.ball
        
        if ball.enabled == 0:
            return
        
        d = ball.pos[1]-(dim[1]*0.5 - self.height*0.5)
        if d>0 and d<self.height:
            if ball.pos[0]<ball.radius:
                # Goal on left side
                ball.enable(0)
                display_text("Goal on left side!", 3)
            if ball.pos[0]>dim[0]-ball.radius:
                # Goal on right side
                ball.enable(0)
                display_text("Goal on right side!", 3)
        