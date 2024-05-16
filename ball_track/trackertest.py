from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import os
from LinePosition import frame_set

picar.setup()

rear_wheels_enable  = True
front_wheels_enable = True

img = cv2.VideoCapture(-1)

if not img.isOpened:
    print("not open")
else:
    print("open")
    
SCREEN_WIDTH = 160
SCREEN_HIGHT = 120

img.set(cv2.CAP_PROP_FRAME_WIDTH,SCREEN_WIDTH)
img.set(cv2.CAP_PROP_FRAME_HEIGHT,SCREEN_HIGHT)

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
tilt_servo = Servo.Servo(0)

fw.offset = 0
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
tilt_servo.write(90)

motor_speed = 60

def main():
    print("Begin!")

    while True:
        try:
            _, frame = img.read()
            roi2 = frame[90:120, 0:160]
            roi3 = frame[60:90, 0:160]
            roi4 = frame[30:60, 0:160]
            roi5 = frame[0:30, 0:160]
        except Exception as e:
            print(e)
            continue
        
        low_b = np.uint8([60,60,60])
        high_b = np.uint8([0,0,0])
        
        mask2 = cv2.inRange(roi2,high_b,low_b)
        mask3 = cv2.inRange(roi3,high_b,low_b)
        mask4 = cv2.inRange(roi4,high_b,low_b)
        mask5 = cv2.inRange(roi5,high_b,low_b)
        
        contours2, _ = cv2.findContours(mask2, 1, cv2.CHAIN_APPROX_NONE)
        contours3, _ = cv2.findContours(mask3, 1, cv2.CHAIN_APPROX_NONE)
        contours4, _ = cv2.findContours(mask4, 1, cv2.CHAIN_APPROX_NONE)
        contours5, _ = cv2.findContours(mask5, 1, cv2.CHAIN_APPROX_NONE)
        
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
            fw_angle = 120 # change plz
            if front_wheels_enable:
                 fw.turn(fw_angle)
        elif direction_flag == -1:
            fw_angle = 60 # change plz
            if front_wheels_enable:
                 fw.turn(fw_angle)
        else:
            fw_angle = 90 # change plz
            if rear_wheels_enable:
                bw.speed = motor_speed
                bw.forward()
                
        sleep(0.01)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    
    #press 'q', exits the while and stop 
    bw.stop()
    fw.turn(90)
    cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
