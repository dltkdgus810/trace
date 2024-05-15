from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os
from LinePosition import frame_set

picar.setup()
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

if (show_image_enable or draw_circle_enable) and "DISPLAY" not in os.environ:
    print('Warning: Display not found, turn off "show_image_enable" and "draw_circle_enable"')
    show_image_enable   = False
    draw_circle_enable  = False

kernel = np.ones((5,5),np.uint8)
img = cv2.VideoCapture(-1)

if not img.isOpened:
    print("not open")
else:
    print("open")
    
SCREEN_WIDTH = 160
SCREEN_HIGHT = 120
# img.set(3,SCREEN_WIDTH)
# img.set(4,SCREEN_HIGHT)
img.set(cv2.CAP_PROP_FRAME_WIDTH,SCREEN_WIDTH)
img.set(cv2.CAP_PROP_FRAME_HEIGHT,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
BALL_SIZE_MIN = SCREEN_HIGHT/10
BALL_SIZE_MAX = SCREEN_HIGHT/3

# Filter setting, DONOT CHANGE
hmn = 12
hmx = 37
smn = 96
smx = 255
vmn = 186
vmx = 255

# camera follow mode:
# 0 = step by step(slow, stable), 
# 1 = calculate the step(fast, unstable)
follow_mode = 1

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

SCAN_POS = [[20, TILT_ANGLE_MIN], [50, TILT_ANGLE_MIN], [90, TILT_ANGLE_MIN], [130, TILT_ANGLE_MIN], [160, TILT_ANGLE_MIN], 
            [160, 80], [130, 80], [90, 80], [50, 80], [20, 80]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)

motor_speed = 60

def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 90             # initial angle for tilt
    fw_angle = 90

    scan_count = 0
    
    low_b = np.uint8([60,60,60])
    high_b = np.uint8([0,0,0])
    print("Begin!")

    while True:
        try:
            _, frame = img.read()
            #frame의 특정 위치의 장만면 저장한다.
            roi2 = frame[90:120, 0:160]
            roi3 = frame[60:90, 0:160]
            roi4 = frame[30:60, 0:160]
            roi5 = frame[0:30, 0:160]
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
        
        results = [result2, result3, result4, result5]
        direction_flag = 0
        
        for result in results:
            if result == 1 or result == -1:
                direction_flag = result
                break
            else:
                continue
            
        if direction_flag ==1:
            pan_angle += CAMERA_STEP
            if pan_angle > PAN_ANGLE_MAX:
                pan_angle = PAN_ANGLE_MAX
        elif direction_flag == -1:
            pan_angle -= CAMERA_STEP
            if pan_angle < PAN_ANGLE_MIN:
                pan_angle = PAN_ANGLE_MIN
        else:
            if front_wheels_enable:
                fw.turn(fw_angle)
            if rear_wheels_enable:
                bw.speed = motor_speed
                bw.forward()
        
        
if __name__ == "__main__":
    main()