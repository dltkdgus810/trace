#
#   공대선배
#   opencv python 코딩
#   카메라 연결 코드
#

import cv2 #opencv 라이브러리를 불러오겠다.
import numpy as np
# opencv python 코딩 기본 틀
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
capture = cv2.VideoCapture(0) #캡쳐 객체, 0번 웹캠으로서 영상을 가져오겠다.
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #해상도 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #해상도 설정

# 무한루프
while True: #영상의 한 프레임을 받아, 이미지로 보여준다.
    ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
    #noise 생성
    noise = np.uint8(np.random.normal(loc=0,scale=0.4,size=[480,640,3]))
    noised_img = cv2.add(frame,noise) #현재 영상에 noise 추가
    
    #화면을 흐리게 만들어 노이즈 제거 인자(입력이미지,(필터가로, 세로 크기))
    blur = cv2.blur(noised_img,(5,5)) 
    #blur필터보다 외곽선이 살아남
    gaussian = cv2.GaussianBlur(noised_img,(5,5),0)
    #gaussian필터보다 외곽선을 더 살려줌
    bilateral = cv2.bilateralFilter(noised_img,9,75,75)
    
    median = cv2.medianBlur(frame,5)
    
    cv2.imshow("original", frame)   # frame(카메라 영상)을 original 이라는 창에 띄워줌 
    cv2.imshow("noised", noised_img)
    cv2.imshow("blur",blur)
    cv2.imshow("gaussian",gaussian)
    cv2.imshow("bilateral",bilateral)
    cv2.imshow("median",median)
    if cv2.waitKey(1) == ord('q'):  # 키보드의 q 를 누르면 무한루프가 멈춤
            break

capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌