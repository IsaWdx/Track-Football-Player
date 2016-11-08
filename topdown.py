__author__ = 'GAO RISHENG'
import os
import numpy
import cv2
import math

distancep = 406.0 #pixels
distanceA = 40.3 #meters




colors = [[218,165,8],
		  [133,58,0],
		  [213,149,19],
		  [164,83,0],
		  [204,149,52],
		  [161,80,0],
		  [197,137,78],
		  [164,81,36],
		  [128,41,15],
		  [101,0,2],
		  [130,28,53],
		  [140,20,128],
		  [54,0,77],
		  [77,6,132],
		  [127,0,219],
		  [77,0,197],
		  [37,2,171],
		  [55,2,219],
		  [11,10,174],
		  [7,5,71],
		  [2,9,151]]

colors = [[255,0,255],
		  [0,0,255],
		  [255,0,0],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [0,0,255],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],
		  [255,0,0],

		  [255,0,0]]


distanceAll = np.zeros(21)
speedAll = np.zeros([7210,21])
currentPos = np.zeros([21,2])
previousPos = np.zeros([21,2])
file = open("sequence.txt","r")
index = 0
imgbg = cv2.imread("field.png")
videoWriter = cv2.VideoWriter('topdownview_bluered2.avi',
                              #cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),

                              cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'),
                              #fourcc,
                              24, (1280,880),)
img = imgbg
for line in file:
	imgbg = img.copy()
	if len(line)<2:
            break
	#print index
	temp = line.split(" ")
	
	for i in range(0,len(temp)/2):
		if index == 0:
			previousPos[i][0] = temp[2*i]
			previousPos[i][1] = temp[2*i+1]
			distanceAll[i] = 0
			speedAll[index][i] = 0
		else:
			currentPos[i][0] = temp[2*i]
			currentPos[i][1] = temp[2*i+1]
			distanceAll[i] = distanceAll[i] + sqrt((currentPos[i][0]-previousPos[i][0])**2 + (currentPos[i][1]-previousPos[i][1])**2)/distancep*distanceA
			speedAll[index][i] = sqrt((currentPos[i][0]-previousPos[i][0])**2 + (currentPos[i][1]-previousPos[i][1])**2)/distancep*distanceA*24
			#cv2.line(imgbg,(int(previousPos[i][1]),int(previousPos[i][0])),(int(currentPos[i][1]),int(currentPos[i][0])),(colors[i][0],colors[i][1],colors[i][2]),5)
			#cv2.line(imgbg,(int(previousPos[i][1]),int(previousPos[i][0])),(int(previousPos[i][1]),int(previousPos[i][0])),(colors[i][0],colors[i][1],colors[i][2]),5)
			cv2.line(imgbg,(int((previousPos[i][1]+currentPos[i][1])/2),int((previousPos[i][0]+currentPos[i][0])/2)),((int((previousPos[i][1]+currentPos[i][1])/2)),int((previousPos[i][0]+currentPos[i][0])/2)),(colors[i][0],colors[i][1],colors[i][2]),10)
			previousPos[i][0] = currentPos[i][0]
			previousPos[i][1] = currentPos[i][1]
	videoWriter.write(imgbg)
	index = index+1
	#cv2.imwrite(str(index)+"color.jpg",imgbg)

print distanceAll
