import lgpio  # RPi.GPIO 대신 lgpio를 사용
import time

# 사용할 GPIO 핀 번호를 설정.
RC_PIN = 17  # RC 수신기의 신호 핀 번호
SERVO_PIN = 27  # 서보 모터의 신호 핀 번호

# 서보 모터를 제어하는 클래스를 정의.
class ServoControl:
    def __init__(self, h, pin):
        self.h = h
        self.pin = pin
        lgpio.gpio_claim_output(self.h, self.pin)  # GPIO 핀을 출력 모드로 설정.
        self.servo_pwm = lgpio.tx_pwm(self.h, self.pin, 50, 0)  # PWM 객체를 생성. 주파수는 50Hz, 초기 듀티 사이클은 0으로 설정.

    def set_angle(self, angle):
        # 주어진 각도를 듀티 사이클로 변환.
        duty_cycle = (angle / 180.0) * 10 + 2
        lgpio.tx_pwm(self.h, self.pin, 50, duty_cycle)  # 듀티 사이클을 설정.
        time.sleep(0.2)  # 안정화를 위해 잠시 대기.

# GPIO 핸들 생성 및 핀 설정
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, RC_PIN)  # RC_PIN을 입력 모드로 설정.

# ServoControl 클래스의 인스턴스를 생성합니다.
servo_manual = ServoControl(h, SERVO_PIN)

try:
    while True:
        # RC 수신기에서 PWM 값 읽기
        pulse_start = time.time()
        while lgpio.gpio_read(h, RC_PIN) == 0:
            pulse_start = time.time()
        
        while lgpio.gpio_read(h, RC_PIN) == 1:
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
    lgpio.gpiochip_close(h)  # GPIO 핸들을 정리합니다.
