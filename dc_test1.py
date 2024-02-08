import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
RC_PIN = 22  # 수신기의 신호선에 연결
DC_MOTOR_PIN = 27  # DC 모터의 신호선에 연결

# PWM 값을 읽어와 DC 모터를 제어하는 클래스
class MotorControl:
    def __init__(self, dc_motor_pin):
        self.dc_motor_pin = dc_motor_pin
        GPIO.setup(self.dc_motor_pin, GPIO.OUT)
        GPIO.output(self.dc_motor_pin, GPIO.LOW)

    def set_motor_state(self, pwm_value):
        # 범위에 따라 DC 모터를 ON 또는 OFF로 설정
        if 950 <= pwm_value <= 1100:
            GPIO.output(self.dc_motor_pin, GPIO.HIGH)  # DC 모터를 ON으로 설정
            motor_state = "ON"
        else:
            GPIO.output(self.dc_motor_pin, GPIO.LOW)  # DC 모터를 OFF로 설정
            motor_state = "OFF"

        # DC 모터 상태 출력
        print(f"DC 모터 상태: {motor_state}")

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정

# DC 모터 제어 객체 생성
dc_motor_control = MotorControl(DC_MOTOR_PIN)

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
        
        # PWM 값 출력
        print(f"현재 PWM 값: {pwm_value:04d}")
        
        # DC 모터 제어
        dc_motor_control.set_motor_state(pwm_value)

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
