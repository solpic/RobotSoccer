import sys
import pygame

text_message = ""
text_start_time = 0
text_display_time = 0
text_box = (100, 400)
    
def display_text(msg, duration):
    global text_message, text_start_time, text_display_time
    
    text_message = msg
    text_start_time = pygame.time.get_ticks()/1000.0
    text_display_time = duration

def run_sim(sim, ai_arr, dimensions):    
    bg_color = (0, 255, 0)

    pygame.init()

    # Create simulator window
    window = pygame.display.set_mode(dimensions)
    running = 1
    last_tick = pygame.time.get_ticks()
    while running == 1:
        # Update fake AIs
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            break;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = 0
                break;
            for ai in ai_arr:
                ai.keydown(event.key)
        if event.type == pygame.KEYUP:
            for ai in ai_arr:
                ai.keyup(event.key)
        
        window.fill(bg_color)
        
        # Get dt
        cur_time = pygame.time.get_ticks()
        dt = (cur_time - last_tick)/1000.0
        last_tick = cur_time
        sim.update(dt)
        sim.draw(window)
        
        # Check if we should be displaying a message
        if cur_time/1000.0 < text_start_time + text_display_time:
            fnt = pygame.font.SysFont("monospace", 15)
            lbl = fnt.render(text_message, 1, (0, 0, 0))
            window.blit(lbl, text_box)
        
        pygame.display.flip()
        
    pygame.quit()
