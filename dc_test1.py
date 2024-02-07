import RPi.GPIO as GPIO
import time

MOTOR_PIN = 27  # 모터를 제어하기 위한 GPIO 핀

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

try:
    while True:
        # 모터를 전진 방향으로 회전
        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        time.sleep(2)  # 2초간 회전
        
        # 모터를 정지
        GPIO.output(MOTOR_PIN, GPIO.LOW)
        time.sleep(2)  # 2초간 정지

except KeyboardInterrupt:
    GPIO.cleanup()
