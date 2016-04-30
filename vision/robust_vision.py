import cv2
import cv2.cv as cv
import numpy as np
from math import pow
from tracking_object import TrackingObject
from vision_server import VisionServer

class ImageTransform:
    def __init__(self, blur, erosions, dilations, threshold, range, range_set):
        self.blur = blur
        self.erosions = erosions
        self.dilations = dilations
        self.threshold = threshold
        self.range = range
        self.range_set = range_set
    
    def add_to_range(self, h, s, v):
        if self.range_set == 0:
            self.range = [h, s, v, h, s, v]
            self.range_set = 1
        else:
            if self.range[0]>h:
                self.range[0] = h
            if self.range[1]>s:
                self.range[1] = s
            if self.range[2]>v:
                self.range[2] = v

            if self.range[3]<h:
                self.range[3] = h
            if self.range[4]<s:
                self.range[4] = s
            if self.range[5]<v:
                self.range[5] = v
    
    def get_threshold(self, hsv):
        return cv2.inRange(hsv, np.array((self.range[0]-self.threshold, self.range[1]-self.threshold, self.range[2]-self.threshold)), np.array((self.range[3]+self.threshold, self.range[4]+self.threshold, self.range[5]+self.threshold)))
    
    def transform_image(self, image):
        blur = cv2.medianBlur(image, self.blur)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        thresholded = self.get_threshold(image)
        erosion = cv2.erode(thresholded, None, iterations = self.erosions)
        dilation = cv2.dilate(erosion, None, iterations = self.dilations)

        return dilation
        
class SingleTracker:
    def __init__(self, transform):
        self.transform = transform
        self.positions = []
        self.radii = []
        self.tracking_objects = []

    def track_one(self, contours, ind):
        pos = self.positions[ind]
        
        closest_dist = -1
        closest = 0, 0
        radius = 0
        
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cx, cy = x+w/2, y+h/2
            
            dist = pow(cx - pos[0], 2) + pow(cy - pos[1], 2)
            if closest_dist<0 or dist<closest_dist:
                closest_dist = dist
                closest = cx, cy
                radius = w+h/4
                
        
        if closest_dist >= 0:
            self.positions[ind] = closest
            self.radii[ind] = radius
            self.tracking_objects[ind].update(closest[0], closest[1])

    def add_tracking_object(self, pos, name):
        self.positions.append(pos)
        self.radii.append(5)
        self.tracking_objects.append(TrackingObject(name, pos))

    def overlay(self, image):
        i = 0
        while i<len(self.positions):
            cv2.circle(image, self.positions[i], self.radii[i]/2, [255, 255, 255], 2)
            cv2.putText(image, self.tracking_objects[i].name, self.positions[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)
            i = i + 1
        
    def track(self, image, overlay):
        transformed = self.transform.transform_image(image)
        contours, hierarchy = cv2.findContours(transformed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if overlay == 1:
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
        
        i = 0
        while i < len(self.positions):
            self.track_one(contours, i)
            i = i + 1
        
class Tracker:
    def __init__(self, width, height):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        
        self.width = self.capture.get(3)
        self.height = self.capture.get(4)
        
        self.transform = ImageTransform(11, 1, 3, 5, [0, 0, 0, 0, 0, 0], 0)
        self.trackers = []

        self.cur_tracker = SingleTracker(self.transform)
        
        self.image = 0
        
        self.server = 0
        
        print "Frame width and height: ", self.width, self.height
        
    def mouse_callback(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.transform.add_to_range(self.image.item(y, x, 0), self.image.item(y, x, 1), self.image.item(y, x, 2))

        if event == cv2.EVENT_RBUTTONDOWN:
            name = raw_input("Type name for tracker: ")
            self.cur_tracker.add_tracking_object((x, y), name)
    
    def run_loop(self):
        running = 1
        while running==1:
            _, frame = self.capture.read()
            self.image = frame
            
            key = cv2.waitKey(25)
            
            if key == 27: # ESCAPE
                running = 0

            if self.server == 0:
                if key == ord('q'):
                    self.transform.blur = self.transform.blur + 2
                    print "Blur at ", self.transform.blur
                if key == ord('a'):
                    self.transform.blur = self.transform.blur - 2
                    print "Blur at ", self.transform.blur
                    
                if key == ord('w'):
                    self.transform.erosions = self.transform.erosions + 1
                    print "Erosions at ", self.transform.erosions
                if key == ord('s'):
                    self.transform.erosions = self.transform.erosions - 1
                    print "Erosions at ", self.transform.erosions
                    
                if key == ord('e'):
                    self.transform.dilations = self.transform.dilations + 1
                    print "Dilations at ", self.transform.dilations
                if key == ord('d'):
                    self.transform.dilations = self.transform.dilations - 1
                    print "Dilations at ", self.transform.dilations
                    
                if key == ord('r'):
                    self.transform.threshold = self.transform.threshold + 1
                    print "Threshold at ", self.transform.threshold
                if key == ord('f'):
                    self.transform.threshold = self.transform.threshold - 1
                    print "Threshold at ", self.transform.threshold

                if key == ord(' '):
                    print "Adding tracker permanently"
                    self.trackers.append(self.cur_tracker)
                    self.transform = ImageTransform(11, 1, 3, 5, [0, 0, 0, 0, 0, 0], 0)
                    self.cur_tracker = SingleTracker(self.transform)

                if key == ord('v'):
                    port = int(raw_input("What port to run server on? "))
                    host = "localhost"
                    connections = 1
                    tracking_objs = []
                    for tracker in self.trackers:
                        tracking_objs.extend(tracker.tracking_objects)

                    self.server = VisionServer(host, port, connections, tracking_objs)
                    

                self.cur_tracker.track(self.image, 1)
                self.cur_tracker.overlay(self.image)

            for tracker in self.trackers:
                tracker.track(self.image, 0)
                tracker.overlay(self.image)
                
            cv2.imshow('img', self.image)
            #cv2.imshow('img2', transformed)
            if self.server == 0:
                cv2.setMouseCallback('img', self.mouse_callback)
            else:
                self.server.update()
                
        cv2.destroyAllWindows()
        self.capture.release()
        
tracker = Tracker(320, 240)
tracker.run_loop()
