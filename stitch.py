__author__ = 'Wang Dongxu'
import numpy as np
import cv2
import cv2.cv as cv

l2m = [[ -1.69785456e+03,  -6.11337180e+01,  -7.05433527e+04],
 [  2.50271374e+02,  -7.66438434e+02,  -2.68484830e+06],
 [ -8.39661750e-02,   5.11169339e-01,  -1.69302582e+03]]
r2m = [[  1.63972393e+03,   1.36522399e+02,  -2.49521497e+05],
 [  2.00536899e+02,   1.74530149e+03,  -2.70504261e+06],
 [  2.59606442e-02,   5.90282775e-01,   6.33491962e+02]]

leftlength = 2900
rightlength = 3700
middlelength = 1920-3


cap_l = cv2.VideoCapture("football_left.mp4")
cap_m = cv2.VideoCapture("football_mid.mp4")
cap_r = cv2.VideoCapture("football_right.mp4")

fps = 24
frame_size = [int(cap_l.get(cv.CV_CAP_PROP_FRAME_WIDTH )),int(cap_l.get(cv.CV_CAP_PROP_FRAME_HEIGHT))]

fourcc = int(cap_l.get(cv.CV_CAP_PROP_FOURCC))
iscolor = int(1)
count = int(cap_l.get(7))

#print fourcc
newfoucc = int(cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'))
#print fps,frame_size,iscolor
videoWriter = cv2.VideoWriter('out.avi',
                              #cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),

                              newfoucc,
                              #fourcc,
                              fps, (frame_size[0]
                              ,
                               frame_size[1]/2))
#writer = cv2.VideoWriter("panorama.mp4",
#                              fourcc,
#                              fps,
#                              (frame_size[0]+leftlength,frame_size[1]),
#                              )
#print newfoucc
final_img  =  np.zeros([1080/2,1920,3])
translated_location = np.zeros([1080/2,1920,2])


for i in range(0,540):
    for j in range(0,1920):
        if j<leftlength*1920/8517+3:
            a = np.dot(l2m,[i*2,(j-leftlength*1920/8517)*8517/1920,1])
            scale = 1.0/a[2]
            a[0]=int(scale*a[0])
            a[1]=int(scale*a[1])

            translated_location[i][j][0] = a[0]+4
            translated_location[i][j][1] = a[1]
        elif j<(leftlength+middlelength)*1920/8517:
            translated_location[i][j][0] = i*2
            translated_location[i][j][1] = j*8517/1920-leftlength
        else:
            a = np.dot(r2m,[i*2,j*8517/1920-leftlength,1])
            scale = 1.0/a[2]
            a[0]=int(scale*a[0])
            a[1]=int(scale*a[1])
            translated_location[i][j][0] = a[0]
            translated_location[i][j][1] = a[1]



for i in range(0,count):
    _, left_img = cap_l.read()
    _, mid_img = cap_m.read()
    mid_img = mid_img[:,3:,:]
    _,right_img = cap_r.read()
    for i in range(0,540):
        for j in range(0,1920):
            if j<leftlength*1920/8517+3:
                if 0<=translated_location[i][j][0]<1080 and 0<=translated_location[i][j][1]<1920:
                    final_img[i][j] = left_img[translated_location[i][j][0]][translated_location[i][j][1]]
            elif j<(leftlength+middlelength)*1920/8517:
                if 0<=translated_location[i][j][0]<1080 and 0<=translated_location[i][j][1]<1917:
                    final_img[i][j] = mid_img[translated_location[i][j][0]][translated_location[i][j][1]]

            else:
                if 0<=translated_location[i][j][0]<1080 and 0<=translated_location[i][j][1]<1920:
                    final_img[i][j] = right_img[translated_location[i][j][0]][translated_location[i][j][1]]


    final_img = final_img .astype('uint8')
	
    #cv2.imwrite("final_img.jpg",final_img)
    videoWriter.write(final_img)
