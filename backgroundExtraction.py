__author__ = "GAO RISHENG A0101891L"
import os
import numpy as np
import cv2
import cv2.cv as cv


def background_extraction():
    capture1 = cv2.VideoCapture("out.avi"))
    _,img = capture1.read()
    avgImg = np.float32(img)

    index = 0;
    for fr in range(1,7200):

        _,img = capture1.read()

        cv2.accumulateWeighted(img,avgImg,1.0-(float(index)/float(index+1.0)))
        normImg = cv2.convertScaleAbs(avgImg) # convert into uint8 image

        index = index +1
        if(index == 7199):
            cv2.imwrite("Background.jpg",avgImg)


    capture1.release()





background_extraction()

