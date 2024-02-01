import time
import RPi.GPIO as GPIO

pwm_pin = 17  # PWM 신호를 읽을 GPIO 핀
motor_pin = 25  # DC 모터를 제어할 GPIO 핀

# PWM 값에 따른 모터 상태 설정
PWM_MIN = 850
PWM_MAX = 1100

def control_dc_motor(pulse_duration):
    if PWM_MIN <= pulse_duration <= PWM_MAX:
        # PWM 값에 따라 모터 상태 결정
        GPIO.output(motor_pin, GPIO.HIGH)  # 모터 ON
        print("DC 모터 ON")
    else:
        GPIO.output(motor_pin, GPIO.LOW)  # 모터 OFF
        print("DC 모터 OFF")

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(pwm_pin) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        print("펄스 길이:", pulse_duration)

        # 펄스 길이에 따라 DC 모터 상태 결정
        control_dc_motor(pulse_duration)

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
