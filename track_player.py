import numpy as np
import cv2.cv as cv
import compute_h
import cv2
import string
import math
__author__ = 'Wang Dongxu'

pre_locations = np.array([[179, 1039, 941.61199021, 2487.48484553, 1992.786414 ,0],#judge
[204, 683, 3826.01994904, 4539.3298937, 4403.13134649,0],#left goal keeper
[181,1273,2631.61058134,3432.05155356,3252.92390565,0],#right,goal,keeper
[189,913,2936.66456565,4725.15260391,6126.15904849,0],#red team
[160,1005,1339.53459995,2078.18029726,2159.24800515,0],
[285,1039,1882.23602588,3303.78531417,6791.94054729,0],
[192,1020,2552.11628923,4172.69169484,5930.41499026,0],
[243,1218,4555.38120296,6498.21089546,8623.74584165,0],
[138,945,1214.0297678,1563.85501088,1742.50035816,0],
[139,1079,2003.17439257,2623.77950713,2928.95030828,0],
[165,1058,814.454457608,965.834154588,945.573874296,0],

[206,930,3128.32871562,3741.7848697,3555.07056542,0],#blue team
[237,1013,4183.71076564,4862.89942183,4720.96043363,0],
[176,1066,4139.95716288,5227.80005128,6420.09715651,0],
[199,1154,3464.01764982,3718.90695133,3613.51675608,0],
[161,1082,2737.81174638,3063.37497066,2787.8791129,0],
[176,1093,3073.84184799,3492.98223587,3467.84082036,0],
[150,1096,2063.9712204,2161.3107087,2107.52333471,0],
[148,1041,1550.43126297,1624.99459014,1624.99459014,0],
[178,1131,814.454457608,965.834154588,945.573874296,0],
[225,1215,814.454457608,965.834154588,945.573874296,0]]
)

side_pts = [[170,891],
            [123,628],
            [113,1146],
            [307,1543],
            [520,4]
]
middle = (72 + 1186)/2
top_pts = [[350,630],#circle up
             [72,74],#left up corner
             [72,1186],#right up corner
             [646,1186],#right door down right
             [813,74]]#bottom left

s2t = np.linalg.inv(compute_h.homography(side_pts, top_pts))

def eudistance(a,b):
    dis = math.sqrt(sum(np.power((a - b)[0:5], 2)))  
    #if dis<2000:
    #    print dis
    return math.sqrt(sum(np.power((a - b)[0:5], 2)))  
	    
def assign(pre_locations,cur_locations,assignment,pre_isfound,cur_isfound,depth,num_players = 21):
    usagetable = np.zeros([cur_locations.shape[0],21])
    for i in range(0, 21):
	if pre_isfound[i][0]>0:
	    continue
	minDist = 10*pre_locations[i][5]+10
	minIndex = -1
	for j in range(0, cur_locations.shape[0]):
	    if cur_isfound[j][0]>0:
	        continue
	    distance = eudistance(pre_locations[i,:],cur_locations[j,:])
	    
	    if (not ((cur_locations[j,1]<1000) and i == 2)) and (not ((cur_locations[j,1]>700 )and i == 1)):
		
	    #print distance
	    	if minDist>distance:
		    minDist = distance
		    minIndex = j
	
        if minIndex == -1:
	    assignment[i] = pre_locations[i]
	    assignment[i][5]+=1
	    pre_isfound[i][0] = 1
	   
	else:
	    usagetable[minIndex][i] = 1
	    
    for j in range(0,cur_locations.shape[0]):
	if cur_isfound[j][0]>0:
	    continue

	if(sum(usagetable[j,:])==1):
	    for i in range(0,21):
	        if usagetable[j][i] == 1:
		    assignment[i] = cur_locations[j]
	            pre_isfound[i][0] = 1
		   	    
	            cur_isfound[j][0] = 1
		  
	elif(sum(usagetable[j,:])>1):
	 
	    minDist = 300
	    minIndex = -1
            for i in range(0,21):
	        if usagetable[j][i] == 1:
		    distance = eudistance(pre_locations[i,:],cur_locations[j,:])
                    if minDist>distance:
			minDist = distance
			minIndex = i
	    if minIndex != -1:
	    	assignment[minIndex] = cur_locations[j]
	        pre_isfound[minIndex][0] = 1	
	      
	        cur_isfound[j][0] = 1	
    
   
    if sum(pre_isfound[:,0])==21.0 :
        return assignment
    else:

        return assign(pre_locations,cur_locations,assignment,pre_isfound,cur_isfound,depth+1)

def checkcolor(a):
    b = string.atof(a[2])
    g = string.atof(a[3])
    r = string.atof(a[4])
    indensity = math.log(0.0+b+g+r)/3
   
    if r>g*1.2:
        return [3, 0,indensity]
    if g>r*1.2:
	return [-3,0,indensity]
    return [0,0,0]


    

f0 = open("rawtraj0-4500.txt",'r')
f1 = open("rawtraj4500-5100e.txt",'r')
f2 = open("rawtraj5100-5400.txt",'r')
f3 = open("rawtraj5400-7200.txt",'r')

out2 = open("sequence2.txt",'w')

out3 = open("sequence3.txt",'w')
out = open("sequence.txt",'w')
for i in range(0,21):
	b = np.dot(s2t,[pre_locations[i][0],pre_locations[i][1],1])
	scale = 1.0/b[2]
	b[0]=int(scale*b[0])
	b[1]=int(scale*b[1])
	pre_locations[i][0] = b[0]
	pre_locations[i][1] = b[1]
	pre_locations[i][2:5] = checkcolor(pre_locations[i])
        pre_locations[i][5] = 0
	
index = 0

def findmin(player,left,right):
    minindex = -1
    mini = 10000000
    for i in range(left,right):
	if(player[i][1]<mini):
	    minindex = i
	    mini = player[i][1]
    return minindex,mini

def findmax(player,left,right):
    maxindex = -1
    maxi = 0
    for i in range(left,right):
	if(player[i][1]>maxi):
	    maxindex = i
	    maxi = player[i][1]
    return maxindex,maxi

def offside(pre_locations, middle):
    leftnum = 0
    leftIndex = -1
    rightIndex = -1
    leftlocation = 1000
    rightlocation = 0 
    
    leftredIndex = -1
    leftredlocation = 1000

    rightbluelocation = 0
    rightblueIndex = -1

    minredindex, minred = findmin(pre_locations,3,11)
    maxblueindex, maxblue = findmax(pre_locations,11,21) 
	

    for i in range(3,21):
	if pre_locations[i][1]<middle:
	    leftnum+=1
	if pre_locations[i][1]<leftlocation:
	    leftlocation = pre_locations[i][1]
	    leftIndex = i
	if pre_locations[i][1]>rightlocation:
	    rightlocation = pre_locations[i][1]
	    rightIndex = i
    if leftnum>11:#attack blue left most :offside remember the left most red
	if 10<leftIndex<21:
	    return [1,minred]
    if leftnum<9:#attack red right most: offside
	if 2<rightIndex<11:
	    return [0,maxblue]
    return [-1,-1]
	
	



while True:
    
    index+=1
    print index
    #if index>2:
    #	break
    word = ''
    word2 = ''
    word3 = ''
    yw = offside(pre_locations, middle)   
    for i in range(0,21):
	for j in range(0,2):
	    word+=str(round(pre_locations[i][j]))+' ' 	
    word+='\n'
    out.write(word)

    for i in range(0,21):
	for j in range(0,6):
	    word2+=str(pre_locations[i][j])+' ' 
        word2+=str(yw[0])+' '+str(yw[1])+'\n'
    word2+='\n'
    out2.write(word2)
    out3.write(str(yw[0])+' '+str(yw[1])+'\n')
    if index<=4500:
    	line = f0.readline()
    elif index<=5100:
	line = f1.readline()
    elif index<=5400:
	line = f2.readline()

    elif index<=7200:
	line = f3.readline()
    else:
	break


    cursize = string.atoi(line)

    cur_locations = np.zeros([cursize, 6])
    
    assignment = np.zeros([21,6])# x, y, g, b, r, of new positions, times of being static
    pre_isfound = np.zeros([21,1])#whether a prelocation finds a successor
    cur_isfound = np.zeros([cur_locations.shape[0],1])
    for i in range(0,cursize):
	if index<=4500:
    	    line = f0.readline()
        elif index<=5100:
	    line = f1.readline()
        elif index<=5400:
	    line = f2.readline()

        elif index<=7200:
	    line = f3.readline()
        
        if (len(line)<10):
	    break
        
    	a = line.split(' ')
	b = np.dot(s2t,[string.atof(a[0]),string.atof(a[1]),1])
	scale = 1.0/b[2]
	b[0]=int(scale*b[0])
	b[1]=int(scale*b[1])
	cur_locations[i][0] = b[0]
	cur_locations[i][1] = b[1]
	cur_locations[i][2:5] = checkcolor(a)
        cur_locations[i][5] = 0
    pre_locations = assign(pre_locations,cur_locations,assignment,pre_isfound,cur_isfound,0)
	
    
            
	
    
