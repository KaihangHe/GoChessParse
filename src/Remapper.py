#!/usr/bin/python3
# code by nicapoet
import cv2
import numpy as np
import random
import struct


def remapImage(InputArray, corners, output_size):
    if (len(corners) != 4):
        print("corner num err")
    src_Mat = []
    dst_Mat = np.float32(
        [[0, 0],
         [output_size[0], 0],
         [output_size[0], output_size[1]],
        [0, output_size[1]]])
    for i, pt in enumerate(corners):
        src_Mat.append(list(pt))
    src_Mat = np.float32(src_Mat)
    perspective_mat = cv2.getPerspectiveTransform(src_Mat, dst_Mat)
    dstImage = cv2.warpPerspective(InputArray, perspective_mat, output_size)
    # cv2.imshow("dstImage", dstImage)
    # cv2.imwrite("dstImage7.jpg", dstImage)
    return perspective_mat,dstImage

def createLineIterator(P1, P2, img_shape):
   #define local variables for readability
   img=np.zeros([img_shape[0],img_shape[1]],np.uint8)
   imageH = img.shape[0]
   imageW = img.shape[1]
   P1X = P1[0]
   P1Y = P1[1]
   P2X = P2[0]
   P2Y = P2[1]

   #difference and absolute difference between points
   #used to calculate slope and relative location between points
   dX = P2X - P1X
   dY = P2Y - P1Y
   dXa = np.abs(dX)
   dYa = np.abs(dY)

   #predefine numpy array for output based on distance between points
   itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32)
   itbuffer.fill(np.nan)

   #Obtain coordinates along the line using a form of Bresenham's algorithm
   negY = P1Y > P2Y
   negX = P1X > P2X
   if P1X == P2X: #vertical line segment
       itbuffer[:,0] = P1X
       if negY:
           itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
       else:
           itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
   elif P1Y == P2Y: #horizontal line segment
       itbuffer[:,1] = P1Y
       if negX:
           itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
       else:
           itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
   else: #diagonal line segment
       steepSlope = dYa > dXa
       if steepSlope:
           slope = dX.astype(np.float32)/dY.astype(np.float32)
           if negY:
               itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
           else:
               itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
           itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
       else:
           slope = dY.astype(np.float32)/dX.astype(np.float32)
           if negX:
               itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
           else:
               itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
           itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

   #Remove points outside of image
   colX = itbuffer[:,0]
   colY = itbuffer[:,1]
   itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

   #Get intensities from img ndarray
   itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]
   return itbuffer

def mouse_call_back(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(param[0], (x, y), 5, (0, 255, 0), -1)
        param[1].append((x, y))
    cv2.imshow('image', param[0])
    if (cv2.waitKey(1) == 27 or len(param[1]) == 4):
        remapImage(param[0], param[1], (600, 600))


if __name__ == '__main__':
    srcImage = cv2.imread('../dataset/test_image/1.jpg')
    srcImage = cv2.GaussianBlur(srcImage, (5, 5), 1)
    edgeImage = cv2.Canny(srcImage, 60, 100)
    edgeImage = cv2.dilate(edgeImage, cv2.getStructuringElement(0, (2, 2)))
    # edgeImage = cv2.erode(edgeImage, cv2.getStructuringElement(0, (3, 3)))
    contours, hierary = cv2.findContours(edgeImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contoursImage = srcImage
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) < 50:
            continue
        # approx = cv2.approxPolyDP(contours[i], 5, True)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.drawContours(contoursImage, contours[i], i, color, -1)
        cv2.imshow('contoursImage', contoursImage)
        cv2.waitKey()
    cv2.imshow('edge', edgeImage)
    cv2.imshow('imaqge', srcImage)
    cv2.waitKey(0)
