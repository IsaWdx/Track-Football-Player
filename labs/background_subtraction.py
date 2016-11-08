import os

import cv2
import numpy as np




for num in range(1,6):
        

        	img = cv2.imread('pic'+str(num)+'.jpg',1)
        	height = img.shape[0]#height
        	width = img.shape[1]#width

        	bins = height*width/256
        	frequency = np.zeros([1,256])
        	intensity = np.zeros([1,256])

        	for i in range(0,height):
    
                	for j in range(0,width):
        
                        	frequency[0][img[i][j][0]]= frequency[0][img[i][j][0]]+1
        	total = 0

        	for i in range(0,256):
    
                	total = total+frequency[0][i]
    
                	intensity[0][i] = min(total/bins,255)
    


        	for i in range(0,height):    
                	for j in range(0,width):        
                        	img[i][j][0] =intensity[0][img[i][j][0]]
                        	img[i][j][1] =intensity[0][img[i][j][1]]
                        	img[i][j][2] =intensity[0][img[i][j][2]]
        
                
                cv2.imwrite('pic'+str(num)+'_new.jpg',img)
        
   	   	


        




