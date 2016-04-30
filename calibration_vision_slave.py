# Import OpenCV and NumPy
import cv2
import numpy as np
import sys

sys.path.append('vision')

from tracking_object import TrackingObject
from vision_server import VisionServer

corner_range_set = 0
corner_range = [0, 0, 0, 0, 0, 0]

ball_range_set = 0
ball_range = [0, 0, 0, 0, 0, 0]

# Returns an image where every pixel in the range is white, everything else is black
# This is for blue
threshold = 5
def getthresholdedimgcorner(hsv):
    global threshold
    return cv2.inRange(hsv,np.array((corner_range[0]-threshold, corner_range[1]-threshold, corner_range[2]-threshold)),
                       np.array((corner_range[3]+threshold, corner_range[4]+threshold, corner_range[5]+threshold)))

# This is for yellow
def getthresholdedimgyellow(hsv):
    global threshold
    return cv2.inRange(hsv,np.array((ball_range[0]-threshold, ball_range[1]-threshold, ball_range[2]-threshold)),
                       np.array((ball_range[3]+threshold, ball_range[4]+threshold, ball_range[5]+threshold)))

hsv = 0

def mouse_callback(event, x, y, flag, param):
    global corner_range_set
    global corner_range
    global ball_range_set
    global ball_range
    
    if event == cv2.EVENT_LBUTTONDOWN:
        h = hsv.item(y, x, 0)
        s = hsv.item(y, x, 1)
        v = hsv.item(y, x, 2)

        if corner_range_set == 0:
            corner_range = [h, s, v, h, s, v]
            corner_range_set = 1
        else:
            if corner_range[0]>h:
                corner_range[0] = h
            if corner_range[1]>s:
                corner_range[1] = s
            if corner_range[2]>v:
                corner_range[2] = v

            if corner_range[3]<h:
                corner_range[3] = h
            if corner_range[4]<s:
                corner_range[4] = s
            if corner_range[5]<v:
                corner_range[5] = v
        print "HSV at "+str(x)+", "+str(y)+" is "+str(h)+", "+str(s)+", "+str(v)+", range is now "+str(corner_range)

    if event == cv2.EVENT_RBUTTONDOWN:
        h = hsv.item(y, x, 0)
        s = hsv.item(y, x, 1)
        v = hsv.item(y, x, 2)

        if ball_range_set == 0:
            ball_range = [h, s, v, h, s, v]
            ball_range_set = 1
        else:
            if ball_range[0]>h:
                ball_range[0] = h
            if ball_range[1]>s:
                ball_range[1] = s
            if ball_range[2]>v:
                ball_range[2] = v

            if ball_range[3]<h:
                ball_range[3] = h
            if ball_range[4]<s:
                ball_range[4] = s
            if ball_range[5]<v:
                ball_range[5] = v
        print "HSV at "+str(x)+", "+str(y)+" is "+str(h)+", "+str(s)+", "+str(v)+", range is now "+str(corner_range)


# Returns a video capture instance
c = cv2.VideoCapture(0)
ball = TrackingObject("Ball", (0, 0))
robot = TrackingObject("Robot", (0, 0))

vision_server = VisionServer("localhost", 10001, 1, [ball, robot])

width,height = c.get(3),c.get(4)
print "frame width and height : ", width, height

show_rects = 1

while(1):
    _,f = c.read()
    
    # Blurs the image and converts it from RGB to HSV
    blur = cv2.medianBlur(f,31)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    
    # We need a separate processed image for the corners of the field and the ball
    corners = getthresholdedimgcorner(hsv)
    erode_corners = cv2.erode(corners,None,iterations = 3)
    dilate_corners = cv2.dilate(erode_corners,None,iterations = 10)

    # Finds the shapes in the corners image
    contours_corners,hierarchy_corners = cv2.findContours(dilate_corners,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # Image processing for ball
    ball_img = getthresholdedimgyellow(hsv)
    erode_ball = cv2.erode(ball_img,None,iterations = 3)
    dilate_ball = cv2.dilate(erode_ball,None,iterations = 10)

    contours_ball,hierarchy_ball = cv2.findContours(dilate_ball,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through shapes in corners image, for BALL
    if len(contours_corners)>0:
        ball_cnt = contours_corners[0]
        
        x,y,w,h = cv2.boundingRect(ball_cnt)
        ball.update(x + (w/2), y + (h/2))
        
        cv2.rectangle(f, (x, y), (x+w, y+h), [0, 255, 255], 2)

    
    # Now look for the ROBOT
    if len(contours_ball)>0:
        robot_cnt = contours_ball[0]
        x,y,w,h = cv2.boundingRect(robot_cnt)
        cx,cy = x+w/2, y+h/2
        
        robot.update(cx, cy)
        
        cv2.rectangle(f, (x, y), (x+w, y+h), [255, 0, 0], 2)

    cv2.imshow('img',f)
    
    # If press ESC exit
    if cv2.waitKey(25) == 27:
        break

    key = cv2.waitKey(25)

    if key == 27:
        break

    if key == 119:
        threshold = threshold + 1
        print threshold

    if key == 115:
        threshold = threshold - 1
        print threshold
    
    # Show the image
    cv2.imshow('img',blur)
    cv2.imshow('corners', corners)
    cv2.imshow('ball', ball_img)
    cv2.setMouseCallback('img', mouse_callback)
    
    vision_server.update()


cv2.destroyAllWindows()
c.release()

