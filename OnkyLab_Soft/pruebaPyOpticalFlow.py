import numpy as np
import cv2


def nothing(x):
    pass

# mouse callback function
flag_comenzar=False
p0 = np.array([[[ .0,  .0]], [[ .0,  .0]]], 'float32')

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global p0
        p0 = np.array([[[ x,  y]], [[ y,  x]]], 'float32')
        cv2.circle(frame,(x,y),100,(255,0,0),-1)
        global flag_comenzar
        flag_comenzar=True
        print(flag_comenzar)

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
##p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

cv2.setMouseCallback('image',draw_circle)

lh =170
hh  = 179
ls = 160
hs = 255
lv = 60
hv = 255


while(1):

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
    ret,frame = cap.read()
    
    if not flag_comenzar:
        cv2.imshow('image',frame)
        continue

    frame = cv2.medianBlur(frame,5)

    # Convert BGR to HSV
##    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
##    red_mask = cv2.inRange(hsv, (lh,ls,lv),(hh,hs,hv))
##    frame = cv2.bitwise_and(frame,frame, mask=red_mask)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    if np.any(st):
        good_new = p1[st==1]
        good_old = p0[st==1]
    else:
        good_new = p0
        good_old = p0

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)

    img = cv2.add(frame,mask)

    cv2.imshow('image',img)
    
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
