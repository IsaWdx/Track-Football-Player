__author__ = "GAO RISHENG A0101891L"
import os
import numpy as np
import cv2
import math

def process(img):
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            if(img[i][j][0] == 0 and img[i][j][1]<128 and img[i][j][2]==0):
                img[i][j][1] = 128
    return img




img = cv2.imread("fieldInitial.png")

outputImg = process(img)
cv2.imwrite("field.png",outputImg)
