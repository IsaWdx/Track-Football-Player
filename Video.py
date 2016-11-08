__author__ = 'Wang Dongxu'
import numpy as np
import cv2
import cv2.cv as cv

__author__ = 'Isa'
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
middlelength = 1920


cap_l = cv2.VideoCapture("football_left.mp4")
cap_m = cv2.VideoCapture("football_mid.mp4")
cap_r = cv2.VideoCapture("football_right.mp4")

fps = int(round(cap_l.get(cv.CV_CAP_PROP_FPS)))
frame_size = [int(cap_l.get(cv.CV_CAP_PROP_FRAME_WIDTH )),int(cap_l.get(cv.CV_CAP_PROP_FRAME_HEIGHT))]

fourcc = int(cap_l.get(cv.CV_CAP_PROP_FOURCC))
iscolor = int(1)
count = int(cap_l.get(7))

print fourcc
newfoucc = int(cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'))
print fps,frame_size,iscolor
videoWriter = cv2.VideoWriter('o.avi',
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
print newfoucc
final_img  =  np.zeros([1080/2,1920,3])


newimg = np.zeros([1080,1920+leftlength+rightlength-3,3])
for i in range(0,12):
    _, left_img = cap_l.read()
    _, mid_img = cap_m.read()
    _,right_img = cap_r.read()
    print i

    for i in range(0,newimg.shape[0]):
        for j in range(0,newimg.shape[1]):
            if j<leftlength:
                a = np.dot(l2m,[i,(j-leftlength),1])
                scale = 1.0/a[2]
                a[0]=int(scale*a[0])
                a[1]=int(scale*a[1])
                if 0<=a[0]<1080 and 0<=a[1]<1920:
                    newimg[i][j] = left_img[a[0]][a[1]]
            elif j<leftlength+middlelength-3:
               newimg[i][j] = mid_img[i][j-leftlength+3]
            else:
                a = np.dot(r2m,[i,j-leftlength-3,1])
                scale = 1.0/a[2]
                a[0]=int(scale*a[0])
                a[1]=int(scale*a[1])
                if 0<=a[0]<1080 and 0<=a[1]<1920:
                    newimg[i][j] = right_img[a[0]][a[1]]
    a = final_img.shape[0]
    b = final_img.shape[1]

    for i in range(0,a):
        for j in range(0,b):
            final_img[i][j] = newimg[i*2][j*8517/1920]


    final_img = final_img .astype('uint8')
    videoWriter.write(final_img)
