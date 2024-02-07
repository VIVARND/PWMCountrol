import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RC_PIN = 23  # 수신기의 신호선에 연결
SERVO_PIN = 24  # 서보 모터의 신호선에 연결

# PWM 신호를 읽어와 서보 모터를 제어하는 클래스
class ServoControl:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.pin, 50)  # PWM 주파수 50Hz
        self.servo_pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = ((angle + 90) / 180.0) * 10 + 2  # 각도를 듀티 사이클로 변환
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # 안정화를 위해 잠시 대기

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정

# 서보 모터 제어 객체 생성
servo = ServoControl(SERVO_PIN)

try:
    while True:
        # 조종기 값 읽기
        rc_value = # 여기에 조종기(T10J)의 PWM 신호를 읽는 코드를 추가

        # 범위에 따라 서보 모터 각도 설정
        if 900 <= rc_value <= 1100:
            servo.set_angle(0)  # 0도
        elif 1300 <= rc_value <= 1500:
            servo.set_angle(40)  # 40도
        elif 1800 <= rc_value <= 2100:
            servo.set_angle(90)  # 90도
        else:
            servo.set_angle(0)  # 다른 값이면 0도

except KeyboardInterrupt:
    GPIO.cleanup()
