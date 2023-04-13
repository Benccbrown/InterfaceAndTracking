# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:03:56 2022

@author: 24234681
"""

import numpy as np
import cv2

#Imports the face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.txt')

#Sets the font
font = cv2.FONT_HERSHEY_SIMPLEX

#define movement threshodls
max_head_movement = 20
gestureBoundary = 100

#Sets up bool for first while loopand other basic variables
faceVisible = False
gesture = False
x_movement = 0
y_movement = 0
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
purple = (130, 0, 75)
arrayA = []
arrayA2 = []
arrayB = []

#The gesture is seen for 10 frames
gesture_show = 20


#Use the camera as the input
#cap = cv2.VideoCapture(0)
#Use a video file as the input 
cap = cv2.VideoCapture('Test.mp4')


#a function to measure the distance of x and y
def distance(x,y):
    import math
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2) 
    


#Lucas and Kanades Method for Optical Flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


#function for getting coordinates of positions
def get_coords(p1):
    try: return int(p1[0][0][0]), int(p1[0][0][1])
    except: return int(p1[0][0]), int(p1[0][1])

#Until the face is first seen, this runs
while not faceVisible:
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
    #below tests to see if this section runs
    print ("Waiting for face")
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),red,2)
        faceVisible = True
    cv2.imshow('image',frame)

    #Waitkey(1) shows one frame per ms making it a video output whereas waitkey(0) returns an image
    cv2.waitKey(1)
    
#returns the centre of the face creating p0
face_center = x+w/2, y+h/3
p0 = np.array([[face_center]], np.float32)


#When the face is first seen this runs
while True:    
    ret,frame = cap.read()
    old_gray = frame_gray.copy()
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi_gray = frame[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]
    #The below creates a square which shows where the face is at the start (mostly for testing)
    #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

            
    #Creates a circle on where the user is first noticed 
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    cv2.circle(frame, get_coords(p1), 4, (0,0,255), -1)

            
    
    #Returns the coordinates for point 0 and 1 for head movements
    a,b = get_coords(p0), get_coords(p1)
    x_movement += abs(a[0]-b[0])
    y_movement += abs(a[1]-b[1])
    
    #the text for both x and y movements is posted
    text = 'x_movement: ' + str(x_movement)
    if not gesture: cv2.putText(frame,text,(50,50), font, 0.8, purple, 2)
    text = 'y_movement: ' + str(y_movement)
    if not gesture: cv2.putText(frame,text,(50,100), font, 0.8, purple, 2)
    
    #if either x or y movement is above the gestureBoundary then...
    if y_movement > gestureBoundary:
        gesture = 'Nodding'
        arrayA.append(a[0])
        arrayA2.append(a[1])
    if x_movement > gestureBoundary:
        gesture = 'Shaking'
        arrayB.append(b)
        #if a gesture is being made and the frames the gesture is shown is equal to 0 then it will say if a gesture is being shown
    if gesture and gesture_show > 0:
        cv2.putText(frame,'Shaking or nodding?: ' + gesture,(50,50), font, 1.2, purple,3)
        #each frame gesture_show decreases
        gesture_show -=1
    if gesture_show == 0:
        gesture = False
        x_movement = 0
        y_movement = 0
        gesture_show = 20 #number of frames a gesture is shown
        
    #shaking loop
    if len(arrayB) > 0:
        i = 0
        while len(arrayB) > i + 1:
            cv2.circle(frame, (arrayB[i]), 10, blue, 4)
            i = i + 1
            print ("i equals = ", + i)
                
    #nodding loop
    if len(arrayA) > 0:
        i = 0
        while len(arrayA) + 1 > i + 1:
            cv2.rectangle(frame, ((arrayA[i]-50), (arrayA2[i]-50)), ((arrayA[i]+50), (arrayA2[i]+50)), green, 2)
            i = i + 1
            print ("i equals = ", + i)
        
    for (x,y,w,h) in faces:
        #Creates a square around all users
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
            
    #The below section tests if faces are present, if so it will say they are showing, if not it will say none show
    if len(faces) > 0:
        Text = ' Showing'
    else:
        Text = ' Not Showing'
    cv2.putText(frame,'Face:' + Text,(50,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, purple, 2, cv2.LINE_AA)
    #the below prints how many faces there are in the console
    print("faces present:", len(faces))
        
    #The below makes the pointer follow the user, but without makes it stay where it first saw the face
    p0 = p1
    cv2.imshow('image',frame)

    #Waitkey(1) shows one frame per ms making it a video output whereas waitkey(0) returns an image
    cv2.waitKey(1)
    
    #If esc is pressed, the application will close
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
#.release closes the IO device
cap.release() 
#.destroyAllWindows closes all the windows that the IO device opened
cv2.destroyAllWindows()
