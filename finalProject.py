import Image
import numpy as np
import math
from copy import deepcopy
from random import randint
import cv2.cv as cv
import cv2


sobelX =  np.array([[-1,0,1],
 					[-2,0,2],
 					[-1,0,1]])

sobelY =  np.array([[1,2,1],
 					[0,0,0],
 					[-1,-2,-1]])


def edgeDetection(gray, height, width):
	output = np.zeros( (height,width,3), dtype=np.uint8)
	for y in range(1,height-1):
		for x in range(1,width-1):
			pixelX = [0,0,0]
			pixelY = [0,0,0]
			for i in range(-1,1):
				for j in range(-1,1):
					pixelX[0] += int(sobelX[j][i]) * int(gray[y+i][x+j][0])
					pixelY[0] += int(sobelY[j][i]) * int(gray[y+i][x+j][0])
					pixelX[1] += int(sobelX[j][i]) * int(gray[y+i][x+j][1])
					pixelY[1] += int(sobelY[j][i]) * int(gray[y+i][x+j][1])
					pixelX[2] += int(sobelX[j][i]) * int(gray[y+i][x+j][2])
					pixelY[2] += int(sobelY[j][i]) * int(gray[y+i][x+j][2])
			output[y][x] = [
				math.sqrt((pixelX[0] * pixelX[0]) + (pixelY[0] * pixelY[0])),
				math.sqrt((pixelX[1] * pixelX[1]) + (pixelY[1] * pixelY[1])),
				math.sqrt((pixelX[2] * pixelX[2]) + (pixelY[2] * pixelY[2]))]
	return output, height, width


def printImage(array):
	newImg = Image.fromarray(array,'RGB')
	newImg.show()

def tresh(image, height, width):

	T = 12

	for y in range(height):
		for x in range(width):
			if(int(image[y][x][0]) > T):
				image[y][x][0] = 255
			else:
				image[y][x][0] = 0
			if(int(image[y][x][1]) > T*1.5):
				image[y][x][1] = 255
			else:
				image[y][x][1] = 0
			if(int(image[y][x][2]) > T):
				image[y][x][2] = 255
			else:
				image[y][x][2] = 0

	return(image)

##
#
# TASK 1 
#
##

def find():
	img = Image.open("image2.png")
	width, height = img.size
	image = np.zeros( (height,width,3), dtype=np.uint8)
	for y in range(height):
		for x in range(width):
			image[y][x] = img.getpixel((x, y))
	image, height, width = edgeDetection(image, height, width)
	tresh(image, height, width)
	return image


pilImage = find()
img = cv2.imread("image2.png")
height, width, channels = img.shape
for i in range(height):
	for j in range(width):
		img[i][j] = pilImage[i][j]


circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT,0.5,0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()