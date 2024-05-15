#
#   공대선배
#   opencv python 코딩
#   카메라 연결 코드
#

import cv2 #opencv 라이브러리를 불러오겠다.

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