#!/usr/bin/python2
# Filename: Lab4.py

import cv2
import os
import numpy as np

def pixel_b2h(pixel):

    #cv2 reads bgr
    B = pixel[0]/255.0
    G = pixel[1]/255.0
    R = pixel[2]/255.0
    Cmax = max(B, G, R)
    Cmin = min(B, G, R)
    delta = Cmax - Cmin

    #Hue calculation
    
    if (delta ==0):
        
        H = 0
    elif (Cmax == R):
        H = 60 * ((G-B)/delta % 6)
    elif (Cmax == G):    
        H = 60 * ((B-R)/delta + 2)    
    elif (Cmax == B):        
        H = 60 * ((R-G)/delta + 4) 


    #Saturation calculation
    if (Cmax == 0):
        S = 0    
    else:        
        S = delta/Cmax 


    #Value calculation
    V = Cmax

    return np.array([H,S,V])


def bgr2hsv(img):

    height = img.shape[0]

    width = img.shape[1]

    img_h = np.zeros([height, width])

    img_s = np.zeros([height, width])

    img_v = np.zeros([height, width])



    for i in range(0, height):
    
        for j in range(0, width):
            pixel = pixel_b2h(img[i][j])
            
            img_h[i][j] = (int)(pixel[0]*255.0/360)
            
            img_s[i][j] = (int)(pixel[1]*255.0)
            
            img_v[i][j] = (int)(pixel[2]*255.0)


    print img_h
    cv2.imwrite('hue.jpg',img_h)
    
    cv2.imwrite('saturation.jpg',img_s)
    
    cv2.imwrite('value.jpg',img_v)
    

    
    cv2.imshow('hue', img_h)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

    img2 = cv2.imread('hue.jpg',0)
    
    print img2
    
    cv2.imshow('hue',img2)
    
    cv2.waitKey()
    cv2.destroyAllWindows()

    cv2.imshow('saturation',img_s)
    cv2.waitKey()
    cv2.destroyAllWindows()
    

    cv2.imshow('value',img_v)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imshow('flower',img)
    cv2.waitKey()
    cv2.destroyAllWindows()

img = cv2.imread('flower.jpg',1)
bgr2hsv(img)



    


   	





