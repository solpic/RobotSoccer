import pygame

class StateRepresentation:
    def __init__(self, objects, client):
        self.objects = objects
        self.client = client
        
    def update(self):
        self.client.receive()
        
    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)
           
def state_rep_window(state_rep, dimensions, callback):    
    bg_color = (0, 255, 0)

    pygame.init()

    # Create simulator window
    window = pygame.display.set_mode(dimensions)
    running = 1
    
    while running == 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            break;
        
        callback()
        
        window.fill(bg_color)
        state_rep.update()
        state_rep.draw(window)
        pygame.display.flip()
        
    pygame.quit()
