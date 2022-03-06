# -*- coding: utf-8 -*-

import cv2
import numpy as np

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#These values for light blue color.
lower = np.array([80, 60, 41])
upper = np.array([110, 255, 255])

_, background = cam.read()

kernel1 = np.ones((3, 3), np.uint8)
kernel2 = np.ones((15, 15), np.uint8)
kernel3 = np.ones((19, 19), np.uint8)

while cam.isOpened():
    
    _, frame = cam.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2)
    mask = cv2.dilate(mask, kernel3, iterations = 1)
    mask_not = cv2.bitwise_not(mask)
    
    bg = cv2.bitwise_and(background, background, mask = mask)
    
    fg = cv2.bitwise_and(frame, frame, mask = mask_not)
    
    dst = cv2.addWeighted(bg, 1, fg, 1, 0)
    
    dst = np.hstack((frame, dst))
    
    cv2.imshow("CAMERA", frame)
    cv2.imshow("MASK", mask)
    cv2.imshow("DST", dst)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()