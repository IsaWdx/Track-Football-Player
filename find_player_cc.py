import numpy as np
import cv2.cv as cv
import compute_h
import cv2
__author__ = 'Wang Dongxu'

#corners = [72.0,74.0,813.0,1186.0]
corners = [90.0,74.0,800.0,1186.0]

cap1 = cv2.VideoCapture("out_sub.avi")
fileobj = open("rawtraj.txt",'w') 

index = 0
fps = 24
frame_size = [int(cap1.get(cv.CV_CAP_PROP_FRAME_WIDTH )),int(cap1.get(cv.CV_CAP_PROP_FRAME_HEIGHT))]
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

s2t = np.linalg.inv(compute_h.homography(side_pts, top_pts))
fourcc = int(cap1.get(cv.CV_CAP_PROP_FOURCC))
iscolor = int(1)
videoWriter = cv2.VideoWriter('out_con_sub.avi',
                              #cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),

                              cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'),
                              #fourcc,
                              fps, (frame_size[0],frame_size[1]),)
player = []#final player put here
font=cv2.cv.InitFont(cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 1, 0, 3, 8)

 
while True:
	index = index +1
	#print index
	_,img = cap1.read()
	#if index<230:
	#    continue
	#print img
	if not _:
		break
        player_frame = []
	inside = False
	#print img.shape
	for j in range(0,img.shape[1]):
	    count = [0,0,0]
	    num = 0
	    
	    for i in range(0,img.shape[0]):
		s = 0.9+i*2.0/540
		if inside == True:
	            if(img[i][j][0]>5 or img[i][j][1]>5 or img[i][j][2]>5): 
			count[0] += 1.0*img[i][j][0]/s
			count[1] += 1.0*img[i][j][1]/s
			count[2] += 1.0*img[i][j][2]/s
		        num += 1
		    else:
		        if (count[0]+count[2]+count[1])>300*s and num>4*s:
			    inside = False
			    
			    flag = 1
			    for element in player_frame:
				if(-4*s<element[1]-j<4*s and -10*s<i-element[0]<=0):
				    flag = 0
				    element[2] += count[0]
				    element[3] += count[1]
				    element[4] += count[2]
				    break
				    
			        if(-4*s<element[1]-j<4*s and 0<i-element[0]<10*s):				    
				    
				    count[0] += element[2]
				    count[1] += element[3]
				    count[2] += element[4]
			     	    player_frame.remove(element)
				    flag = 1      
				    		    	    
			  	    
			    if flag == 1:
			        player_frame.append([i,j,count[0],count[1],count[2]])
			count = [0,0,0]
			num = 0
			        
			    
			
		else:
		    if(img[i][j][0]>20 or img[i][j][1]>20 or img[i][j][2]>20):
		    	inside = True
		        num = 0
			count[0] += 1.0*img[i][j][0]/s
			count[1] += 1.0*img[i][j][1]/s
			count[2] += 1.0*img[i][j][2]/s
		    else:
			inside = False
	

	
	tri = 0
	player_frame.sort(lambda x,y:cmp(x[2]+x[4]+x[3],y[2]+y[4]+y[3]),reverse = True) 
	print "frame"+str(index)
	x = 0
	string = ''
	for i in range(0,len(player_frame)):
		a = np.dot(s2t,[player_frame[i][0],player_frame[i][1],1])
		scale = 1.0/a[2]
		a[0]=int(scale*a[0])
		a[1]=int(scale*a[1])
		
		if(a[0]>corners[0] and a[0]<corners[2] and a[1]>corners[1] and a[1] <corners[3] and player_frame[i][2]>800):
		   x+=1
		   string+=str(player_frame[i][0])+' '+str(player_frame[i][1])+' '+str(player_frame[i][2])+' '+str(player_frame[i][3])+' '+str(player_frame[i][4])+'\n'
		   cv2.rectangle(img, (player_frame[i][1]-5, player_frame[i][0]), (player_frame[i][1]+5, player_frame[i][0]), (255, 0, 0), 2)
		   
                if x>=40:
		    break
	fileobj.write(str(x))
	fileobj.write("\n")
	fileobj.write(string)
	print x
	print string
	#cv2.imwrite("contour"+str(index)+".jpg",img)
	videoWriter.write(img)
