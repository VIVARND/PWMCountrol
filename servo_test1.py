import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀
servo_pin = 24  # 서보모터를 제어할 GPIO 핀

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
    print("PWM 값:", round(pulse_duration, 4))  # 소수점 4자리까지 출력

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 경고 메시지 비활성화
GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(servo_pin, GPIO.OUT)  # 서보모터 핀을 출력으로 설정

pwm = GPIO.PWM(servo_pin, 50)  # PWM 객체를 생성
pwm.start(0)  # PWM 신호를 초기화

GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

try:
    while True:
        time.sleep(0.5)  # 0.5초마다 실행되도록 설정
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
