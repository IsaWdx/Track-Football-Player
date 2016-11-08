import numpy as np
import cv2
__author__ = 'Wang Dongxu'


def homography(pts, perspectivepts):

    line0 = np.array([[pts[0][0],pts[0][1],1,0,0,0,-pts[0][0]*perspectivepts[0][0],-pts[0][1]*perspectivepts[0][0],-perspectivepts[0][0]]])
    line1 = np.array([[0,0,0,pts[0][0],pts[0][1],1,-pts[0][0]*perspectivepts[0][1],-pts[0][1]*perspectivepts[0][1],-perspectivepts[0][1]]])

    line2 = np.array([[pts[1][0],pts[1][1],1,0,0,0,-pts[1][0]*perspectivepts[1][0],-pts[1][1]*perspectivepts[1][0],-perspectivepts[1][0]]])
    line3 = np.array([[0,0,0,pts[1][0],pts[1][1],1,-pts[1][0]*perspectivepts[1][1],-pts[1][1]*perspectivepts[1][1],-perspectivepts[1][1]]])

    line4 = np.array([[pts[2][0],pts[2][1],1,0,0,0,-pts[2][0]*perspectivepts[2][0],-pts[2][1]*perspectivepts[2][0],-perspectivepts[2][0]]])
    line5 = np.array([[0,0,0,pts[2][0],pts[2][1],1,-pts[2][0]*perspectivepts[2][1],-pts[2][1]*perspectivepts[2][1],-perspectivepts[2][1]]])

    line6 = np.array([[pts[3][0],pts[3][1],1,0,0,0,-pts[3][0]*perspectivepts[3][0],-pts[3][1]*perspectivepts[3][0],-perspectivepts[3][0]]])
    line7 = np.array([[0,0,0,pts[3][0],pts[3][1],1,-pts[3][0]*perspectivepts[3][1],-pts[3][1]*perspectivepts[3][1],-perspectivepts[3][1]]])
    if np.array(pts).shape[0]>4:
        line8 = np.array([[pts[4][0],pts[4][1],1,0,0,0,-pts[4][0]*perspectivepts[4][0],-pts[4][1]*perspectivepts[4][0],-perspectivepts[4][0]]])
        line9 = np.array([[0,0,0,pts[4][0],pts[4][1],1,-pts[4][0]*perspectivepts[4][1],-pts[4][1]*perspectivepts[4][1],-perspectivepts[4][1]]])

        line = np.concatenate((line0,line1,line2,line3,line4,line5,line6,line7,line8,line9), axis=0)
    else:
        line = np.concatenate((line0,line1,line2,line3,line4,line5,line6,line7), axis=0)
    U, s, V = np.linalg.svd(line, full_matrices=False)

    min = s[0]
    minnum = 0
    size = np.array(pts).shape[0]*2-1
    for i in range(0, size):
        if(s[i]<min):
            min = s[i]
            minnum = i
    solution = V[minnum,:]
    h = np.zeros([3,3])
    for i in range(0,9):
        h[i/3][i%3] = solution[i]
    return np.linalg.inv(h)



left_img = cv2.imread("left_16.jpg")
mid_img = cv2.imread("mid_16.jpg")



left_pts = [[349,1630],
            [328,1879],
            [685,1799],
            [569,1629],
            [1003,1411]]

mid_pts=[[295,118],
         [243,345],
         [576,351],
         [505,168],
         [991+1,47]]


l2m = homography(left_pts, mid_pts)
print l2m


right_pts = [[574,312],
             [1069,136],
             [977,446],
             [395,224+1],
             [299,162+1]]

mid_pts2 = [[600,1785],
            [1051,1552],
            [1050+1,1882],
            [408,1717],
            [309+1,1665+1]]
r2m = homography(right_pts, mid_pts2)
print r2m

top_pts = [[350,630],#circle up
             [72,74],#left up corner
             [72,1186],#right up corner
             [646,1186],#right door down right
             [813,74]]#bottom left

side_pts = [[170,891],
            [123,628],
            [113,1146],
            [307,1543],
            [520,4]]
s2t = homography(side_pts, top_pts)
print s2t