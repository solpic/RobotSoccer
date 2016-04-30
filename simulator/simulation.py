class Simulation:
    def __init__(self, robots, ball, updateables, dimensions):
        self.robots = robots
        self.ball = ball
        self.updateables = updateables
        self.dimensions = dimensions
        
    def is_colliding(self, pos1, rad1, pos2, rad2):
        d = pow(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2), 0.5)
        
        return (d < (rad1 + rad2))
        
    def ball_collide(self, robot):
        if self.is_colliding(self.ball.pos, self.ball.radius, robot.pos, robot.radius):
            return self.ball
        else:
            return 0
        
    def update(self, dt):
        for robot in self.robots:
            robot.update(self, dt)
        
        self.ball.update(self, dt)
        
        for updater in self.updateables:
            updater.update(self, dt)
        
    def draw(self, window):
        for robot in self.robots:
            robot.draw(window)
            
        for updater in self.updateables:
            updater.draw(window)
            
        self.ball.draw(window)