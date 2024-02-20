import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
RC_PIN = 27  # 수신기의 신호선에 연결
DC_MOTOR_PIN = 22  # DC 모터의 신호선에 연결

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)  # 출력 모드로 설정

# DC 모터 제어 함수
def control_dc_motor(pwm_value):
    if 1800 <= pwm_value <= 2100:
        GPIO.output(DC_MOTOR_PIN, GPIO.HIGH)  # 모터를 켬
    else:
        GPIO.output(DC_MOTOR_PIN, GPIO.LOW)  # 모터를 끔

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
        control_dc_motor(pwm_value)

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
