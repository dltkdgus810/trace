#
#   공대선배
#   opencv python 코딩
#   카메라 연결 코드
#

import cv2 #opencv 라이브러리를 불러오겠다.
import numpy as np

#색감 변경 함수
#어떤 이미지에서 어떤 색을 얼마나 바꿀 것인가
def color_filter(img, color, scale): #입력변수는 영상, 변경 색상, 변경 비율
    dst = np.array(img, np.uint8) #입력 영상과 같은 영상을 복사
    if color == 'blue' or color == 0: #파란색이면
        dst[:,:,0] = cv2.multiply(dst[:,:,0], scale) #영상중 파란색의 비율을 바꿈
    if color == 'green' or color == 1: #초록색이면
        dst[:,:,1] = cv2.multiply(dst[:,:,1], scale) #영상중 초록색의 비율을 바꿈
    if color == 'red' or color == 2: #빨강색이면
        dst[:,:,2] = cv2.multiply(dst[:,:,2], scale) #영상중 빨강색의 비율을 바꿈
    return dst #처리된 영상을 반환
        
def


# opencv python 코딩 기본 틀
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
capture = cv2.VideoCapture(0) #캡쳐 객체, 0번 웹캠으로서 영상을 가져오겠다.
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #해상도 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #해상도 설정

# 무한루프
while True: #영상의 한 프레임을 받아, 이미지로 보여준다.
    ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
    cv2.imshow("original", frame)   # frame(카메라 영상)을 original 이라는 창에 띄워줌 
    if cv2.waitKey(1) == ord('q'):  # 키보드의 q 를 누르면 무한루프가 멈춤
            break

capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌