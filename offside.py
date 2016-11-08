import numpy as np
import cv2.cv as cv
import compute_h
import cv2
__author__ = 'Wang Dongxu'

cap1 = cv2.VideoCapture("out.avi")
fps = 24
frame_size = [int(cap1.get(cv.CV_CAP_PROP_FRAME_WIDTH )),int(cap1.get(cv.CV_CAP_PROP_FRAME_HEIGHT))]
videoWriter = cv2.VideoWriter('out_offside.avi',
                              cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'),                             
                              fps, (frame_size[0],frame_size[1]),)
side_pts = [[170,891],
            [123,628],
            [113,1146],
            [307,1543],
            [520,4]
]
top_pts = [[350,630],#circle up
             [72,74],#left up corner
             [72,1186],#right up corner
             [646,1186],#right door down right
             [813,74]]#bottom left

s2t = compute_h.homography(side_pts, top_pts)

file = open("sequence3.txt",'r')
index = 0

for line in file:
    
    temp = line.split(" ")
    if len(line)<2:
        break
    index+=1
    print index
    temp = line.split(" ")
    ret,frame = cap1.read()	
    if not ret:
	print index-1
	break
    if int(float(temp[1]))>1:
    	a = np.dot(s2t,[100,int(float(temp[1])),1])
    	scale = 1.0/a[2]
    	a[0]=int(scale*a[0])
    	a[1]=int(scale*a[1])

    	b = np.dot(s2t,[800,int(float(temp[1])),1])
    	scale = 1.0/b[2]
    	b[0]=int(scale*b[0])
    	b[1]=int(scale*b[1])

    	cv2.line(frame,(int(b[1]),int(b[0])),(int(a[1]),int(a[0])),(255-int(temp[0])*255,colors[i][1],int(temp[0])*255),4)
	#print b[1]
    videoWriter.write(frame)
	

