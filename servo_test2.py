import RPi.GPIO as GPIO  # RPi.GPIO 라이브러리를 GPIO로 임포트
import time

GPIO.setwarnings(False)  # GPIO 설정 경고를 비활성화.

# 사용할 GPIO 핀 번호를 설정.
RC_PIN = 17  # RC 수신기의 신호 핀 번호
SERVO_PIN = 27  # 서보 모터의 신호 핀 번호

# 서보 모터를 제어하는 클래스를 정의.
class ServoControl:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)  # GPIO 핀을 출력 모드로 설정.
        self.servo_pwm = GPIO.PWM(self.pin, 50)  # PWM 객체를 생성. 주파수는 50Hz로 설정.
        self.servo_pwm.start(0)  # PWM 신호를 시작. 초기 듀티 사이클은 0으로 설정.

    def set_angle(self, angle):
        # 주어진 각도를 듀티 사이클로 변환.
        duty_cycle = (angle / 180.0) * 10 + 2
        self.servo_pwm.ChangeDutyCycle(duty_cycle)  # 듀티 사이클을 설정.
        time.sleep(0.2)  # 안정화를 위해 잠시 대기.

# GPIO 모드를 설정합니다. BCM 모드로 설정합니다.
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # RC_PIN을 입력 모드로 설정.

# ServoControl 클래스의 인스턴스를 생성합니다.
servo_manual = ServoControl(SERVO_PIN)

try:
    while True:
        # RC 수신기에서 PWM 값 읽기
        channel_pulse_start = time.time()
        GPIO.wait_for_edge(RC_PIN, GPIO.RISING)  # RC_PIN의 상승 에지를 기다립니다.
        pulse_start = time.time()

        GPIO.wait_for_edge(RC_PIN, GPIO.FALLING)  # RC_PIN의 하강 에지를 기다립니다.
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start  # 펄스 지속 시간을 계산합니다.

        pwm_value = round(pulse_duration * 1000000)  # PWM 값으로 변환합니다.
        
        # PWM 값 출력
        print(f"현재 PWM 값: {pwm_value:04d}")
        
        # PWM 값에 따라 서보 모터 각도 설정
        if 850 <= pwm_value <= 1100:
            angle = 0  # 0도
        elif 1400 <= pwm_value <= 1600:
            angle = 100  # 80도
        elif 1800 <= pwm_value <= 2100:
            angle = 140  # 140도
        else:
            angle = None  # 그 외의 경우에는 None (서보 모터 멈춤)
        
        if angle is not None:
            servo_manual.set_angle(angle)  # 서보 모터의 각도를 설정합니다.

        # 설정된 각도 출력
        if angle is not None:
            print(f"현재 각도: {angle} 도")
        else:
            print("서보 모터 멈춤")

        time.sleep(0.1)  # 주기적으로 갱신합니다.

except KeyboardInterrupt:
    GPIO.cleanup()  # KeyboardInterrupt 예외가 발생할 경우 GPIO를 정리합니다.
