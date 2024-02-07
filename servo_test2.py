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
        self.current_angle = 0  # 현재 각도 변수 추가

    def set_angle(self, angle):
        duty_cycle = ((angle + 90) / 180.0) * 10 + 2  # 각도를 듀티 사이클로 변환
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # 안정화를 위해 잠시 대기
        self.current_angle = angle  # 현재 각도 업데이트

    def get_current_angle(self):
        return self.current_angle  # 현재 각도 반환

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정

# 서보 모터 제어 객체 생성
servo = ServoControl(SERVO_PIN)

# 각도를 설정하는 함수
def set_servo_angle(angle):
    servo.set_angle(angle)

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
        if 900 <= pwm_value <= 1100:
            set_servo_angle(0)
        elif 1100 < pwm_value <= 1200:
            set_servo_angle(30)
        elif 1300 <= pwm_value <= 1400:
            set_servo_angle(60)
        elif 1500 <= pwm_value <= 1600:
            set_servo_angle(90)
        elif 1800 <= pwm_value <= 2000:
            set_servo_angle(120)

        # 각도 출력
        print(f"현재 각도: {servo.get_current_angle()} 도")

        time.sleep(0.5)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
