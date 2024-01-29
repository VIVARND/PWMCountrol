import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보모터 핀

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 50)  # PWM 객체를 생성, 주파수는 50Hz로 설정
pwm.start(0)

def set_servo_angle(pulse_duration):
    if 0.0007 <= pulse_duration <= 0.0012:
        angle = 10  # 10도
    elif 0.0013 <= pulse_duration <= 0.0015:
        angle = 40  # 40도
    elif 0.0016 <= pulse_duration <= 0.0021:
        angle = 90  # 90도
    else:
        angle = 90  # 기본값은 90도
    print("서보모터 각도:", angle)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        set_servo_angle(pulse_duration)
    print("PWM 값:", round(pulse_duration, 3))  # 소수점 3자리까지 출력
    time.sleep(0.5)  # 0.5초 간격으로 출력

GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
