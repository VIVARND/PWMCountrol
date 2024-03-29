import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)

def pwm_callback(channel):
    pulse_start = time.time()
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    print("채널 10 PWM 값:", pulse_duration)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)

GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

try:
    while True:
        time.sleep(0.1)  # 주기적으로 PWM 값을 확인하는 주기를 늦추었습니다.

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
