import cv2
import numpy as np

#위치확인 함수
def frame_set(contours,roi):
    if len(contours) > 0:
        a = max(contours, key = cv2.contourArea)
        M2 = cv2.moments(a)
        if M2['m00']!=0:
            x = int(M2['m10']/M2['m00'])
            y = int(M2['m01']/M2['m00'])    
            print("CX : "+str(x)+" CY : "+str(y))
            if x >= 400:
                print("Turn Left")
                return x, y, -1
            if x < 400 and x > 200:
                print("On Track")
                return x, y, 0
            if x <= 200:
                print("Turn Right")
                return x, y, 1
    return 0,0,0

#카메라 영상을 capture에 저장
capture = cv2.VideoCapture(0)
#저장한 영상의 화면 크기 설정
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
#검출할 색 선정
low_b = np.uint8([60,60,60])
high_b = np.uint8([0,0,0])

while True:
    #카메라에서 한장면을 뽑아 frame에 저장한다.
    try:
        ret, frame = capture.read()
        #frame의 특정 위치의 장만면 저장한다.
        roi2 = frame[360:480, 0:640]
        roi3 = frame[240:360, 0:640]
        roi4 = frame[120:240, 0:640]
        roi5 = frame[0:120, 0:640]
    except Exception as e:
        print(e)
        continue
    #frame(roi)에서 검정색을 찾아서 검정을 흰색으로 바꾸고 나머지는 검정색으로 만들기
    mask2 = cv2.inRange(roi2,high_b,low_b)
    mask3 = cv2.inRange(roi3,high_b,low_b)
    mask4 = cv2.inRange(roi4,high_b,low_b)
    mask5 = cv2.inRange(roi5,high_b,low_b)
    #mask로 찾은 검정의 외곽선 검출, 3번째 인자는 검출한 모든 외곽선을 저장
    contours2, hierarchy2 = cv2.findContours(mask2, 1, cv2.CHAIN_APPROX_NONE)
    contours3, hierarchy3 = cv2.findContours(mask3, 1, cv2.CHAIN_APPROX_NONE)
    contours4, hierarchy4 = cv2.findContours(mask4, 1, cv2.CHAIN_APPROX_NONE)
    contours5, hierarchy5 = cv2.findContours(mask5, 1, cv2.CHAIN_APPROX_NONE)
    #검출한 외곽선을 이용해 선의 위치를 확인 
    ax, ay, result2 = frame_set(contours2,roi2)
    bx, by, result3 = frame_set(contours3,roi3)
    cx, cy, result4 = frame_set(contours4,roi4)
    dx, dy, result5 = frame_set(contours5,roi5)
    #확인한 위치 중간에 원을 생성  
    cv2.circle(roi2, (ax,ay),5,(255,255,255),-1)
    cv2.circle(roi3, (bx,by),5,(255,255,255),-1)
    cv2.circle(roi4, (cx,cy),5,(255,255,255),-1)
    cv2.circle(roi5, (dx,dy),5,(255,255,255),-1)
    #검출한 외곽선을 frame에 초록색으로 그리기
    cv2.drawContours(roi2,contours2,-1,(0,255,0),1)     
    cv2.drawContours(roi3,contours3,-1,(0,255,0),1)     
    cv2.drawContours(roi4,contours4,-1,(0,255,0),1)     
    cv2.drawContours(roi5,contours5,-1,(0,255,0),1)  
    #촬영하고 있는 영상을 송출   
    cv2.imshow("origin",frame)
    #1ms마다 'q'를 눌렀는지 확인하고 눌렀으면 반복 끝
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌    

