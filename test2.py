import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while True:
    ret, frame = capture.read()
    frame2 = frame.copy()
    frame3 = frame.copy()
    frame4 = frame.copy()
    frame5 = frame.copy()
    roi2 = frame[360:480, 0:640]
    frame2[360:480, 0:640] = roi2
    roi3 = frame[240:360, 0:640]
    frame3[240:360, 0:640] = roi3
    roi4 = frame[120:240, 0:640]
    frame4[120:240, 0:640] = roi4
    roi5 = frame[0:120, 0:640]
    frame5[0:120, 0:640] = roi5
    low_b = np.uint8([60,60,60])
    high_b = np.uint8([0,0,0])
    #frame에서 검정색을 찾아서 검정을 흰색으로 바꾸고 나머지는 검정색으로 만들기
    mask2 = cv2.inRange(roi2,high_b,low_b)
    mask3 = cv2.inRange(roi3,high_b,low_b)
    mask4 = cv2.inRange(roi4,high_b,low_b)
    mask5 = cv2.inRange(roi5,high_b,low_b)
    #mask로 찾은 검정의 외곽선 검출, 3번째 인자는 검출한 모든 외곽선을 저장
    contours2, hierarchy2 = cv2.findContours(mask2, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours2) > 0:
        a = max(contours2, key = cv2.contourArea)
        M2 = cv2.moments(a)
        if M2['m00']!=0:
            ax = int(M2['m10']/M2['m00'])
            ay = int(M2['m01']/M2['m00'])    
            print("CX : "+str(ax)+" CY : "+str(ay))
            if ax >= 400:
                print("Turn Left")
            if ax < 400 and ax > 200:
                print("On Track")
            if ax <= 200:
                print("Turn Right")
            cv2.circle(roi2, (ax,ay),5,(255,255,255),-1)
    contours3, hierarchy3 = cv2.findContours(mask3, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours3) > 0:
        b = max(contours3, key = cv2.contourArea)
        M3 = cv2.moments(b)
        if M3['m00']!=0:
            bx = int(M3['m10']/M3['m00'])
            by = int(M3['m01']/M3['m00'])    
            print("CX : "+str(bx)+" CY : "+str(by))
            if bx >= 400:
                print("Turn Left")
            if bx < 400 and bx > 200:
                print("On Track")
            if bx <= 200:
                print("Turn Right")
            cv2.circle(roi3, (bx,by),5,(255,255,255),-1)  
    contours4, hierarchy4 = cv2.findContours(mask4, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours4) > 0:
        c = max(contours4, key = cv2.contourArea)
        M4 = cv2.moments(c)
        if M4['m00']!=0:
            cx = int(M4['m10']/M4['m00'])
            cy = int(M4['m01']/M4['m00'])    
            print("CX : "+str(cx)+" CY : "+str(cy))
            if cx >= 400:
                print("Turn Left")
            if cx < 400 and cx > 200:
                print("On Track")
            if cx <= 200:
                print("Turn Right")
            cv2.circle(roi4, (cx,cy),5,(255,255,255),-1)        
    contours5, hierarchy5 = cv2.findContours(mask5, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours5) > 0:
        d = max(contours5, key = cv2.contourArea)
        M5 = cv2.moments(d)
        if M5['m00']!=0:
            dx = int(M5['m10']/M5['m00'])
            dy = int(M5['m01']/M5['m00'])    
            print("CX : "+str(dx)+" CY : "+str(dy))
            if dx >= 400:
                print("Turn Left")
            if dx < 400 and dx > 200:
                print("On Track")
            if dx <= 200:
                print("Turn Right")
            cv2.circle(roi5, (dx,dy),5,(255,255,255),-1)        
    #검출한 외곽선을 frame에 초록색으로 그리기
    cv2.drawContours(roi2,contours2,-1,(0,255,0),1)     
    cv2.drawContours(roi3,contours3,-1,(0,255,0),1)     
    cv2.drawContours(roi4,contours4,-1,(0,255,0),1)     
    cv2.drawContours(roi5,contours5,-1,(0,255,0),1)     
    cv2.imshow("origin",frame)
    cv2.imshow("frame2",frame2)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌    