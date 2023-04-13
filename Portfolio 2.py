# -*- coding: utf-8 -*-
"""
Created on Thu Feb 3 11:22:05 2022

@author: 24234681
"""


import numpy as np
import cv2
import random
import time

#black template at 1024 by 1024
img = np.zeros((1024,1024,3), np.uint8)
        

#gets the coordinates of the middle of the image
(centerX, centerY) = (img.shape[1] // 2, img.shape[0] // 2)


#The below draws the name in the middle
#B of the name done using two curves and a line
imgBCurv1 = cv2.ellipse(img,(200, centerY-100),(100,200),270,0,180,(0, 128, 255),0)
imgBCurv2 = cv2.ellipse(imgBCurv1,(200, centerY+100),(100,200),270,0,180,(0, 128, 255),0)
imgBLine = cv2.line(imgBCurv2, (200, centerY-200), (200, centerY+200), (0,128,255),1)

#E of the name done using two squares and a line
imgESquare1 = cv2.rectangle(imgBLine,(centerX-100, centerY-200),(centerX+100, centerY),(0, 128, 255),0)
imgESquare2 = cv2.rectangle(imgESquare1,(centerX-100, centerY),(centerX+100, centerY+200),(0, 128, 255),0)
imgELine = cv2.line(imgESquare2, (centerX+100, centerY-200), (centerX+100, centerY+200), (0, 0, 0),1)

#N of the name done using a polygon and a line
pts = np.array([[centerX+200, centerY-200], [centerX+200, centerY+200], [centerX+400, centerY-200],
                [centerX+400, centerY+200]], np.int32)
pts = pts.reshape((-1,1,2))
imgNPoly = cv2.polylines(imgELine,[pts],True,(0,128,255), 1)
imgNLine = cv2.line(imgNPoly, (centerX+200, centerY+200), (centerX+400, centerY-200), (0, 0, 0),1)

#a list which uses a range
list(range(0, 600, 25))
[0, 25, 75, 125, 150, 500, 250, 200, 300, 550, 600]
#for loop for the range at the top to help create the circles
for r in range(0, 600, 50):
    #draws a circle at the given range
    cv2.circle(img, (centerX, centerY), r, [160, 160, 160])

#Circles looping at the top changing colour throughout
i = 0
x = 0
colour1 = 0
colour2 = 0
colour3 = 0
number = 128
while i < 8:
    

    imgCirc = cv2.circle(imgNLine,(x,128),number,(colour1,colour2,colour3),1,cv2.LINE_AA)
    i = i + 1
    colour1 = random.randint(0, 255)
    colour2 = random.randint(0, 255)
    colour3 = random.randint(0, 255)
    x = x + number

#Rectangles looping at the top changing colour throughout
i = 0
x = 0
xend = number
while i < 8:
    
    imgRec = cv2.rectangle(imgCirc,(x,5),(xend,261),(colour1,colour2,colour3),3)
    i = i + 1
    x = x + number
    xend = xend + number
    colour1 = random.randint(0, 255)
    colour2 = random.randint(0, 255)
    colour3 = random.randint(0, 255)
    
    
#Squares looping at the bottom changing colour throughout
i = 0
x = 0
xend = number
while i < 8:
    
    imgRec = cv2.rectangle(imgCirc,(x,1019-number),(xend,1019),(colour1,colour2,colour3),3)
    i = i + 1
    x = x + number
    xend = xend + number
    colour1 = random.randint(0, 255)
    colour2 = random.randint(0, 255)
    colour3 = random.randint(0, 255)
    
    
#small Squares looping at the bottom just above the bottom squares changing colour throughout
i = 0
x = 0
smallsquares = 32
while i < 32:
    
    imgRec = cv2.rectangle(imgCirc,(x,885-smallsquares),(xend,885),(colour1,colour2,colour3),3)
    i = i + 1
    x = x + smallsquares
    xend = xend + 32
    colour1 = random.randint(0, 255)
    colour2 = random.randint(0, 255)
    colour3 = random.randint(0, 255)
    
    
#32 small Squares looping randomly around the screen between the x and y axis
i = 0
smallsquares = 32
while i < 32:
    
    x = random.randint(0, 992)
    xend = x + 32
    y = random.randint(266, 853)
    imgRec = cv2.rectangle(imgCirc,(x,y-smallsquares),(xend,y),(colour1,colour2,colour3),3)
    i = i + 1
    x = x + smallsquares
    y = y + smallsquares
    xend = x + 32
    colour1 = random.randint(0, 255)
    colour2 = random.randint(0, 255)
    colour3 = random.randint(0, 255)
    

#Purple Square border
imgSqu = cv2.rectangle(imgRec,(2,2),(1022,1022),(153,0,153),3)


#While loop for the animated polygon to move CURRENTLY MOVES WHEN CLOSED AND DOESNT DELETE ORIGINAL
#Polygon
randompoly = random.randint(0, 816)
pts = np.array([[25+randompoly, 70], [25+randompoly, 160], [110+randompoly, 20], [200+randompoly, 160], 
                [200+randompoly, 70], [110+randompoly,200]],
               np.int32)
pts = pts.reshape((-1,1,2))
imgPoly = cv2.polylines(imgSqu,[pts],True,(0,255,255), 5)
    

cv2.imshow('animation',imgPoly) #the whole image is shown with the name 'animation
cv2.waitKey(0) #The program ends if any key is presed
cv2.destroyAllWindows() #Then all windows close


