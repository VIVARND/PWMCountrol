import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀

def set_servo_angle(angle):
    if angle == 10:
        pwm_value = 0.0009
    elif angle == 40:
        pwm_value = 0.0013
    elif angle == 90:
        pwm_value = 0.0017
    else:
        pwm_value = 0
    
    pwm.ChangeDutyCycle(pwm_value * 100)
    print("현재 서보모터 각도:", angle)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        if 0.0007 <= pulse_duration <= 0.0012:
            set_servo_angle(10)
        elif 0.0013 <= pulse_duration <= 0.0015:
            set_servo_angle(40)
        elif 0.0016 <= pulse_duration <= 0.0021:
            set_servo_angle(90)
        else:
            set_servo_angle(0)
    print("PWM 값:", round(pulse_duration, 4))  # PWM 값 출력

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 서보 모터 PWM 설정
pwm.start(0)

try:
    GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
