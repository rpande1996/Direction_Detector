import cv2
import imutils
import numpy as np
import time
from datetime import datetime, timedelta


cap = cv2.VideoCapture(0)
time.sleep(0.1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('../media/output.avi', fourcc, 10, (640, 480))

upper = np.array([95, 255, 255])
lower = np.array([40, 40, 150])
count = 1
t = time.time()

while True:
    start = datetime.now()
    d, img = cap.read()
    img = imutils.resize(img, width = 640)
    lis = list()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    blur = cv2.GaussianBlur(mask, (3,3),0)
    corner = cv2.goodFeaturesToTrack(blur,7,0.4,10)
    corner = np.int0(corner)

    for i in corner:
        x,y = i.ravel()
        cv2.circle(img, (x,y),2,(0,0,255),-1)
    miny = None
    maxy = None
    maxx = None
    minx = None
    for i in corner:
        for j in i:
            ax = j[0]
            ay = j[1]
            if minx == None or ax < minx:
                minx = ax
            if maxx == None or ax > maxx:
                maxx = ax
            if miny == None or ay < miny:
                miny = ay
            if maxy == None or ay > maxy:
                maxy = ay


    x_threshold = minx + (maxx - minx)/2
    y_threshold = miny + (maxy - miny)/2


    if (maxx - minx) > (maxy - miny):
        pointless = 0
        pointmore = 0
        for i in corner:
            for j in i:
                if j[0] < x_threshold:
                    pointless += 1
                else:
                    pointmore += 1
        if pointless > pointmore:
            cv2.putText(img, "Left", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        elif pointless < pointmore:
            cv2.putText(img, "Right", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    if (maxx - minx) < (maxy - miny):
        pointless = 0
        pointmore = 0
        for i in corner:
            for j in i:
                if j[1] < y_threshold:
                    pointless += 1
                else:
                    pointmore += 1
        if pointless > pointmore:
            cv2.putText(img, "Up", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        elif pointless < pointmore:
            cv2.putText(img, "Down", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imshow("original", img)

    out.write(img)

    stop = datetime.now()
    diff = stop - start
    fd = diff.total_seconds() * 1000
    fh = open("../output/data.txt", "a")
    lis.append(str(fd))
    lis.append("\n")
    for i in lis:
        fh.write(i)
    fh.close()
    t1 = time.time()

    key = cv2.waitKey(1)
    if key == 27 or 0XFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
