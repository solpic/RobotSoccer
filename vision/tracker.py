# Holds an array of tracking objects
# On each frame update updates the position of a tracking object
import cv2
import numpy as np

class Tracker:
    def __init__(self):
        self.tracking_objs = []
        
    def track(self, hsv):
        for obj in self.tracking_objs:
            obj.track(hsv)
        
class TrackingObject:
    def __init__(self, range, pos):
        self.range = range
        self.pos = pos
        
    # Returns a thresholded image using the range given
    def get_thresholded_img(self, hsv):
        return cv2.inRange(hsv,np.array((self.range[0], self.range[1], self.range[2])),
                       np.array((self.range[3], self.range[4], self.range[5])))
    
    # Calculates the location of the object and stores it
    def track(self, hsv):
        self.pos = pos
        
    # Returns the tracked position
    def get_pos(self):
        return self.pos
        
    def crawl(self, pos