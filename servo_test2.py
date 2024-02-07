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
        # 조종기 값 읽기 (RPi.GPIO를 사용하는 경우)
        rc_value = GPIO.input(RC_PIN)

        # 주파수와 각도 출력
        print(f"Current PWM Value: {rc_value}")
        
        # 범위에 따라 서보 모터 각도 설정
        if 900 <= rc_value <= 1100:
            angle = 0  # 0도
        elif 1300 <= rc_value <= 1500:
            angle = 40  # 40도
        elif 1800 <= rc_value <= 2100:
            angle = 90  # 90도
        else:
            angle = 0  # 다른 값이면 0도
        
        servo.set_angle(angle)

        # 각도 출력
        print(f"Current Angle: {angle} degrees")

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
