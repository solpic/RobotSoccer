class FakeAI:
    def __init__(self, t_left, t_right, forward, backward):
        self.k_left = t_left
        self.k_right = t_right
        self.k_forward = forward
        self.k_backward = backward
        
        self.left = 0
        self.right = 0
        self.forward = 0
        self.backward = 0
               
    def keydown(self, key):
        if key == self.k_left:
            self.left = 1
        if key == self.k_right:
            self.right = 1
        if key == self.k_forward:
            self.forward = 1
        if key == self.k_backward:
            self.backward = 1
            
    def keyup(self, key):
        if key == self.k_left:
            self.left = 0
        if key == self.k_right:
            self.right = 0
        if key == self.k_forward:
            self.forward = 0
        if key == self.k_backward:
            self.backward = 0
            
    def get_move(self, field_state):
        fb = 0
        if self.backward == 1:
            fb = -1
        if self.forward == 1:
            fb = 1
            
        lr = 0
        if self.right == 1:
            lr = 1
        if self.left == 1:
            lr = -1
            
        return fb, lr
            