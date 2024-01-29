import time
import RPi.GPIO as GPIO
import sys

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀 (라즈베리파이에 연결된 실제 핀 번호에 따라 수정하세요)

def set_servo_angle(angle):
    if angle == 10:
        pwm_value = 0.0090
    elif angle == 40:
        pwm_value = 0.0013
    elif angle == 90:
        pwm_value = 0.0017
    else:
        pwm_value = 0
    
    pwm.ChangeDutyCycle(pwm_value * 100)
    print("현재 서보모터 각도:", angle)
    sys.stdout.flush()

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        if 0.0090 <= pulse_duration <= 0.0011:
            set_servo_angle(10)
        elif 0.0012 <= pulse_duration <= 0.0014:
            set_servo_angle(40)
        elif 0.0015 <= pulse_duration <= 0.0019:
            set_servo_angle(90)
        else:
            set_servo_angle(0)
    print("PWM 값:", round(pulse_duration, 4))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 50)
pwm.start(0)

GPIO.setup(pwm_pin, GPIO.IN)
GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
