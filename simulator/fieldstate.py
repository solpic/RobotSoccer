class Simulation:
    def __init__(self, robots, ball):
        self.robots = robots
        self.ball = ball
        
    def is_colliding(pos1, rad1, pos2, rad2):
        d = pow(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2), 0.5)
        
        return (d < (rad1 + rad2))
        
    def ball_collide(self, robot):
        if is_colliding(self.ball.pos, self.ball.radius, robot.pos, robot.radius):
            return self.ball
        else:
            return 0
        