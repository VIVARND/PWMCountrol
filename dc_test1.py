import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
DC_MOTOR_PIN = 27  # DC 모터의 신호선에 연결

# DC 모터 제어 클래스
class MotorControl:
    def __init__(self, dc_motor_pin):
        self.dc_motor_pin = dc_motor_pin
        GPIO.setup(self.dc_motor_pin, GPIO.OUT)
        GPIO.output(self.dc_motor_pin, GPIO.LOW)

    def rotate_motor(self, duration):
        GPIO.output(self.dc_motor_pin, GPIO.HIGH)  # DC 모터를 ON으로 설정
        print("DC 모터 회전 중...")
        time.sleep(duration)  # 지정된 시간 동안 회전
        GPIO.output(self.dc_motor_pin, GPIO.LOW)  # DC 모터를 OFF로 설정
        print("DC 모터 멈춤")

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# DC 모터 제어 객체 생성
dc_motor_control = MotorControl(DC_MOTOR_PIN)

try:
    while True:
        # DC 모터를 2초 동안 회전하고 2초 동안 멈춤
        dc_motor_control.rotate_motor(2)
        time.sleep(2)  # 2초 대기 후 반복

except KeyboardInterrupt:
    GPIO.cleanup()
