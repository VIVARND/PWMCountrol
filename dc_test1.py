import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
PWM_PIN = 27  # DC 모터를 제어하기 위한 GPIO 핀
RC_PIN = 22   # 수신기의 PWM 신호를 받기 위한 GPIO 핀

# PWM 신호를 읽어와 DC 모터를 제어하는 클래스
class DCMotorControl:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.dc_pwm = GPIO.PWM(self.pin, 50)  # PWM 주파수 50Hz
        self.dc_pwm.start(0)

    def turn_on(self):
        self.dc_pwm.ChangeDutyCycle(100)  # 100% duty cycle (ON)

    def turn_off(self):
        self.dc_pwm.ChangeDutyCycle(0)    # 0% duty cycle (OFF)

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정

# DC 모터 제어 객체 생성
dc_motor = DCMotorControl(PWM_PIN)

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
        
        # 현재 PWM 값과 상태 출력
        print(f"현재 PWM 값: {pwm_value:04d}")
        
        # 범위에 따라 DC 모터 상태 제어
        if 900 <= pwm_value <= 1200:
            print("DC 모터 ON")
            dc_motor.turn_on()
        else:
            print("DC 모터 OFF")
            dc_motor.turn_off()

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
