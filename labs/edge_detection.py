import cv2
import numpy as np
import os
import math


def edge_detection_p(img,num):
	height = img.shape[0]
	width = img.shape[1]
	img_pre = np.zeros([height,width])
	max_pre = 0.0
	min_pre = 100000.0


	for i in range(1,height-1):
		for j in range(1,width-1):
			pre_v = 0.0 -img[i-1][j-1] - img[i][j-1] - img[i+1][j-1] + img[i-1][j+1] + img[i][j+1] + img[i+1][j+1]     	
			pre_h = 0.0 -img[i+1][j-1] - img[i+1][j] - img[i+1][j+1] + img[i-1][j+1] + img[i-1][j] + img[i-1][j-1]
			img_pre[i][j] = math.sqrt(pre_v*pre_v+pre_h*pre_h)
			max_pre = max(max_pre, img_pre[i][j])
			min_pre = min(min_pre, img_pre[i][j])
    
	scale_pre = 255.0/(max_pre-min_pre)
	
	for i in range(1,height-1):
		for j in range(1,width-1):
			img_pre[i][j] = 255 - (img_pre[i][j]-min_pre)*scale_pre   

	
        cv2.imwrite('r_prewitt'+str(num)+'.jpg',img_pre)
	return img_pre

def edge_detection_s(img,num):
	height = img.shape[0]
	width = img.shape[1]
	img_sob = np.zeros([height,width])
	max_sob = 0.0
	min_sob = 100000.0

	for i in range(1,height-1):
		for j in range(1,width-1):
			sob_h = 0.0 -img[i+1][j-1] - 2*img[i+1][j] - img[i+1][j+1] + img[i-1][j+1] + 2*img[i-1][j] + img[i-1][j-1]
			sob_v = 0.0 -img[i-1][j-1] - 2*img[i][j-1] - img[i+1][j-1] + img[i-1][j+1] + 2*img[i][j+1] + img[i+1][j+1]
			img_sob[i][j] = math.sqrt(sob_v*sob_v+sob_h*sob_h)
			max_sob = max(max_sob, img_sob[i][j])        
			min_sob = min(min_sob, img_sob[i][j])
			
	scale_sob = 255.0/(max_sob-min_sob)

	for i in range(1,height-1):
		for j in range(1,width-1):
			img_sob[i][j] = 255 - (img_sob[i][j]-min_sob)*scale_sob
		
	cv2.imwrite('r_sobel'+str(num)+'.jpg',img_sob)
	return img_sob


def edge_thinning(img,num,kind):
	height = img.shape[0]
	width = img.shape[1]
	img_thin = np.zeros([height,width])
	for i in range(1,height-1):
		for j in range(1,width-1):
			if(not(((img[i][j]<img[i][j+1])and(img[i][j]<img[i][j-1])) or ((img[i][j]<img[i+1][j])and(img[i][j]<img[i-1][j])))):
				img_thin[i][j] = 255
			else:
				img_thin[i][j] = img[i][j]
	cv2.imwrite('r_thin'+str(num)+kind+'.jpg',img_thin)


for i in range(1, 4):
	img = cv2.imread('test'
	+str(i)+'.jpg',cv2.CV_LOAD_IMAGE_GRAYSCALE)
	edge_thinning(edge_detection_s(img,i),i,'_sobel')	

	edge_thinning(edge_detection_p(img,i),i,'_prewitt')

