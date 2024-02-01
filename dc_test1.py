import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀
motor_pin = 24  # DC 모터를 제어할 GPIO 핀
frequency = 50  # PWM 주파수 (Hz)

# PWM 값에 따른 모터 속도 조절 관련 상수
PWM_MIN = 900
PWM_MAX = 1100
SPEED_MIN = 0
SPEED_MAX = 100

# Software Debouncing 관련 변수
last_pulse_time = 0
debounce_duration = 0.05  # 50ms

def control_dc_motor(pwm_value):
    if PWM_MIN <= pwm_value <= PWM_MAX:
        # PWM 값에 따라 속도 계산
        speed = (pwm_value - PWM_MIN) / (PWM_MAX - PWM_MIN) * (SPEED_MAX - SPEED_MIN) + SPEED_MIN
        pwm.ChangeDutyCycle(speed)  # PWM 신호 변경 (속도 조절)
        print(f"DC 모터 회전 - 속도: {speed}%")
    else:
        pwm.ChangeDutyCycle(0)  # DC 모터 정지
        print("DC 모터 정지")

def pwm_callback(channel):
    global last_pulse_time
    pulse_start = time.time()
    pulse_duration = pulse_start - last_pulse_time

    # Software Debouncing 적용
    if pulse_duration > debounce_duration:
        last_pulse_time = pulse_start
        pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
        print("PWM 값:", pwm_value)

        # PWM 값에 따라 DC 모터 속도 조절
        control_dc_motor(pwm_value)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(motor_pin, GPIO.OUT)  # DC 모터 제어를 위한 GPIO 핀

pwm = GPIO.PWM(motor_pin, frequency)  # PWM 설정
pwm.start(0)

try:
    GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)
    while True:
        time.sleep(0.1)  # 작은 값으로 설정하여 실시간으로 PWM 값을 확인
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
