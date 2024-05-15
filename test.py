import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while True:
    ret, frame = capture.read()
    frame2 = frame.copy()
    roi = frame[240:480, 0:640]
    frame2[240:480, 0:640] = roi
    low_b = np.uint8([60,60,60])
    high_b = np.uint8([0,0,0])
    #frame에서 검정색을 찾아서 검정을 흰색으로 바꾸고 나머지는 검정색으로 만들기
    mask = cv2.inRange(frame,high_b,low_b)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #mask로 찾은 검정의 외곽선 검출, 3번째 인자는 검출한 모든 외곽선을 저장
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])    
            print("CX : "+str(cx)+" CY : "+str(cy))
            if cx >= 400:
                print("Turn Left")
            if cx < 400 and cx > 200:
                print("On Track")
            if cx <= 200:
                print("Turn Right")
            cv2.circle(frame, (cx,cy),5,(255,255,255),-1)  
            
            
    #검출한 외곽선을 frame에 초록색으로 그리기
    cv2.drawContours(frame,contours,-1,(0,255,0),1)     
    cv2.imshow("mask",mask)
    cv2.imshow("origin",frame)
    cv2.imshow("frame2",frame2)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌    