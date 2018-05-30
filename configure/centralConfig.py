import cv2
import numpy as np
import pdb

IMG_WIDTH = 512
IMG_HEIGHT = 512 

img = np.zeros((IMG_WIDTH,IMG_HEIGHT,3), np.uint8)
img = cv2.line(img, (0,(int)(IMG_HEIGHT/2)), (IMG_WIDTH, (int)(IMG_HEIGHT/2)), (0,255,0), 5)
img = cv2.line(img, ((int)(IMG_WIDTH/2), 0), ((int)(IMG_WIDTH/2), IMG_HEIGHT), (0,255,0), 5)
cv2.namedWindow('Configure', cv2.WINDOW_NORMAL)
cv2.imshow('Configure', img)
if cv2.waitKey(0)&0xff==27:
    cv2.destroyAllWindows()
