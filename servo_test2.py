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
        # 각도를 듀티 사이클로 변환
        duty_cycle = (angle / 180.0) * 10 + 2
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # 안정화를 위해 잠시 대기

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정

# 서보 모터 제어 객체 생성
servo = ServoControl(SERVO_PIN)

try:
    while True:
        # PWM 값 읽어오기
        channel_pulse_start = time.time()
        GPIO.wait_for_edge(RC_PIN, GPIO.RISING)
        pulse_start = time.time()

        GPIO.wait_for_edge(RC_PIN, GPIO.FALLING)
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        pwm_value = round(pulse_duration * 1000000)
        
        # 주파수와 각도 출력
        print(f"현재 PWM 값: {pwm_value:04d}")
        
        # 범위에 따라 서보 모터 각도 설정
        if 940 <= pwm_value <= 1100:
            angle = 0  # 0도
        elif 1120 <= pwm_value <= 1280:
            angle = 20  # 20도
        elif 1300 <= pwm_value <= 1460:
            angle = 40  # 40도
        elif 1480 <= pwm_value <= 1640:
            angle = 60  # 60도
        elif 1660 <= pwm_value <= 1820:
            angle = 80  # 80도
        elif 1840 <= pwm_value <= 2000:
            angle = 100  # 100도
        elif 2020 <= pwm_value <= 2180:
            angle = 120  # 120도
        elif 2200 <= pwm_value <= 2360:
            angle = 140  # 140도
        elif 2380 <= pwm_value <= 2540:
            angle = 160  # 160도
        elif 2560 <= pwm_value <= 2720:
            angle = 180  # 180도
        else:
            angle = None  # 다른 값이면 None (멈춤)
        
        if angle is not None:
            servo.set_angle(angle)

        # 각도 출력
        if angle is not None:
            print(f"현재 각도: {angle} 도")
        else:
            print("서보 모터 멈춤")

        time.sleep(0.5)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
