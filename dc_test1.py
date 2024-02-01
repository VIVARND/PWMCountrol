import time
import RPi.GPIO as GPIO

pwm_pin = 17  # PWM 신호를 읽을 GPIO 핀
motor_pin = 25  # DC 모터를 제어할 GPIO 핀
frequency = 50  # PWM 주파수 (Hz)

# PWM 값에 따른 모터 상태 설정
PWM_MIN = 900
PWM_MAX = 1100

def control_dc_motor(pwm_value):
    if PWM_MIN <= pwm_value <= PWM_MAX:
        # PWM 값에 따라 모터 상태 결정
        GPIO.output(motor_pin, GPIO.HIGH)  # 모터 ON
        print("DC 모터 ON")
    else:
        GPIO.output(motor_pin, GPIO.LOW)  # 모터 OFF
        print("DC 모터 OFF")

def pwm_callback(channel):
    pwm_value = round(time.time() * 1000000)  # 현재 시간을 이용하여 PWM 값 계산
    print("PWM 값:", pwm_value)

    # PWM 값에 따라 DC 모터 상태 결정
    control_dc_motor(pwm_value)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(motor_pin, GPIO.OUT)  # DC 모터 제어를 위한 GPIO 핀
GPIO.output(motor_pin, GPIO.LOW)  # 초기에는 모터 OFF로 설정

try:
    GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)
    while True:
        time.sleep(0.5)  # 0.5초 간격으로 PWM 값을 확인
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
