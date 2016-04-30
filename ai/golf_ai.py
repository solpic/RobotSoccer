from math import pow, sin, cos, fabs
import vec_math

class SimpleGolfAI:
    def __init__(self):
        print "I'm alive!"
        self.plan = 0
        self.shot_distance = 8  # stay 3 times away from the ball's radius before starting the shot
        self.hole_distance = 4 # stop 2 times away from the hole's radius when finishing the shot
        self.at_pos_tolerance = 20
        self.angle_tolerance = 2
        self.adjusting = 0
        self.ball_movement_tolerance = 10
        
        self.least_at_pos_distance = -1
        self.least_at_pos_tolerance = 20
        
    def get_move(self, field_state):
        if self.plan == 0:
            if self.make_plan(field_state) == 0:
                return 0, 0
        
        self.ball_on_track(field_state.ball, field_state.golf_hole)
        
        if self.adjusting == 0:    
            state = self.at_pos(self.plan[self.plan[2]])
            if state == 1:
                if self.plan[2] == 1:
                    # We're done
                    return 0, 0
                else:
                    self.plan = self.plan[0], self.plan[1], self.plan[2] + 1
            
            if state == -1:
                print "Adjusting because robot off track"
                #self.adjusting = 1
                #self.plan = 0
                return 0, 0
            
            return self.move_to(self.plan[self.plan[2]])
        else:
            if not self.ball_moving(field_state.ball):
                self.make_plan(field_state)
                self.adjusting = 0
                
            return 0, 0
            
    def move_to(self, pos):
        speed = 0.2
        a = self.correct_orientation(pos)
        
        if fabs(a) < self.angle_tolerance:
            return speed, speed
        else:
            if a<0:
                return speed, -speed
            else:
                return -speed, speed
        
    def correct_orientation(self, c):
        a = self.robot.pos
        b = self.robot.pos[0] + cos(self.robot.orientation), self.robot.pos[1] + sin(self.robot.orientation)
        
        return ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]))
        
    def ball_moving(self, ball):
        return vec_math.norm(ball.speed)>self.ball_movement_tolerance
        
    def ball_on_track(self, ball, hole):
        if self.ball_moving(ball):
            # Check if ball will go into hole based on its current speed
            d = vec_math.point_to_line_dist(ball.pos, vec_math.add(ball.pos, vec_math.mult(10000, ball.speed)), hole.pos)
            
            if d>hole.radius:
                # Wait for ball to stop and then make new plan
                print "Adjusting because ball off track"
                self.adjusting = 1
    
    def at_pos(self, pos):
        dx = pos[0] - self.robot.pos[0]
        dy = pos[1] - self.robot.pos[1]
        
        d = pow(dx, 2) + pow(dy, 2)
        
        if d < self.at_pos_tolerance:
            return 1
        else:
            if self.least_at_pos_distance < 0:
                self.least_at_pos_distance = d
            else:
                if d <= self.least_at_pos_distance + self.least_at_pos_tolerance:
                    self.least_at_pos_distance = d
                else:
                    print "Off track at distance",d,"with least distance being",self.least_at_pos_distance
                    self.least_at_pos_distance = -1
                    return -1
                    
            return 0
        
    def make_plan(self, field_state):
        self.least_at_pos_distance = -1
        
        print field_state.ball.pos
        print field_state.golf_hole.pos
        
        print field_state.ball
        print field_state.golf_hole
        
        dx = field_state.ball.pos[0] - field_state.golf_hole.pos[0] 
        dy = field_state.ball.pos[1] - field_state.golf_hole.pos[1]
        
        d = pow(pow(dx, 2) + pow(dy, 2), 0.5)
        if d == 0:
            return 0
        dx = dx/d
        dy = dy/d
        
        first_stop = field_state.ball.pos[0] + field_state.ball.radius*dx*self.shot_distance, field_state.ball.pos[1] + field_state.ball.radius*dy*self.shot_distance
                     
        second_stop = field_state.golf_hole.pos[0] + field_state.golf_hole.radius*dx*self.hole_distance, field_state.golf_hole.pos[1] + field_state.golf_hole.radius*dy*self.hole_distance
                     
        self.plan = first_stop, second_stop, 0
        
        return 1
    