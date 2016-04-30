import sys
import pygame

robot_pos_x = 100
robot_pos_y = 100
robot_speed_x = 0
robot_speed_y = 0
robot_mass = 1
robot_drag = 0.99
r_accel = 0.02
robot_radius = 8
robot_color = (255, 255, 0)

ball_pos_x = 150
ball_pos_y = 100
ball_speed_x = 0
ball_speed_y = 0
ball_drag = 0.999
ball_mass = 1
ball_radius = 5
ball_color = (255, 255, 255)

hole_pos = (560, 240)
hole_radius = 10
hole_color = (0, 0, 0)

bg_color = (0, 255, 0)

pygame.init()

# Create simulator window
window = pygame.display.set_mode((640, 480))

def do_some_physics():
    global robot_pos_x, robot_pos_y, robot_speed_x, robot_speed_y, robot_radius, robot_drag
    global ball_pos_x, ball_pos_y, ball_speed_x, ball_speed_y, ball_drag, ball_radius
    d = pow(pow(robot_pos_x - ball_pos_x, 2) + pow(robot_pos_y - ball_pos_y, 2), 0.5)
    
    if d<(robot_radius + ball_radius):
        # COLLISION!
        d_x = ball_pos_x - robot_pos_x
        d_y = ball_pos_y - robot_pos_y

        d_x = d_x/d
        d_y = d_y/d

        robot_speed = pow(pow(robot_speed_x, 2) + pow(robot_speed_y, 2), 0.5)
        
        ball_speed_x = ball_speed_x + d_x*robot_speed
        ball_speed_y = ball_speed_y + d_y*robot_speed

    d_b = pow(pow(ball_pos_x - hole_pos[0], 2) + pow(ball_pos_y - hole_pos[1], 2), 0.5)

    if d_b<(hole_radius - ball_radius):
        print "Hole in one!"
        
    robot_pos_x = robot_pos_x + robot_speed_x
    robot_pos_y = robot_pos_y + robot_speed_y
    
    ball_pos_x = ball_pos_x + ball_speed_x
    ball_pos_y = ball_pos_y + ball_speed_y
    
    #robot_speed_x = robot_speed_x*robot_drag
   # robot_speed_y = robot_speed_y*robot_drag
    
    ball_speed_x = ball_speed_x*ball_drag
    ball_speed_y = ball_speed_y*ball_drag
    

def draw_stuff():
    global window
    window.fill(bg_color)
    pygame.draw.circle(window, hole_color, hole_pos, hole_radius, 0)
    pygame.draw.circle(window, robot_color, (int(robot_pos_x), int(robot_pos_y)), robot_radius, 0)
    pygame.draw.circle(window, ball_color, (int(ball_pos_x), int(ball_pos_y)), ball_radius, 0)
    
running = 1
while running == 1:
    do_some_physics()
    draw_stuff()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = 0
                
            if event.key == pygame.K_LEFT:
                robot_speed_x = -r_accel
            elif event.key == pygame.K_RIGHT:
                robot_speed_x = r_accel
                
            if event.key == pygame.K_UP:
                robot_speed_y = -r_accel
            elif event.key == pygame.K_DOWN:
                robot_speed_y = r_accel
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                robot_speed_x = 0
                
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                robot_speed_y = 0
