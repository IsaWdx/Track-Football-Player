import os
import numpy as np
import cv2
import cv2.cv as cv

def subtraction(img,bg):
    newImg = np.zeros([img.shape[0],img.shape[1],3])
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            if(not (abs(int(img[i][j][0])-bg[i][j][0])<20 and abs(int(img[i][j][1])-bg[i][j][1])<20 and abs(int(img[i][j][2])-bg[i][j][2])<20)):
                newImg[i][j] = img[i][j]
    return newImg

capture = cv2.VideoCapture("out.avi")
imgbg = cv2.imread("Background.jpg")
frameCount = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT))

fps = int(round(capture.get(cv.CV_CAP_PROP_FPS)))
frame_size = [int(capture.get(cv.CV_CAP_PROP_FRAME_WIDTH )),int(capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT))]

fourcc = int(capture.get(cv.CV_CAP_PROP_FOURCC))
iscolor = int(1)


print fourcc
newfoucc = int(cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'))
print fps,frame_size,iscolor
videoWriter = cv2.VideoWriter('out_sub.avi',
                              #cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),

                              newfoucc,
                              #fourcc,
                              fps, (frame_size[0]
                              ,
                               frame_size[1]))

for i in range(0,3600):
    _,img = capture.read()
    if i>=3400:
        print i
        print str(float(i)/float(3600)*100)+"%"

        final_img = subtraction(img,imgbg)
        final_img = final_img .astype('uint8')

        videoWriter.write(final_img)
