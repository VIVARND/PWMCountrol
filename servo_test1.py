import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀 (라즈베리파이에 연결된 실제 핀 번호에 따라 수정하세요)

def set_servo_angle(angle):
    if 0.0007 <= angle <= 0.0012:
        angle = 10
    elif 0.0013 <= angle <= 0.0015:
        angle = 40
    elif 0.0016 <= angle <= 0.0021:
        angle = 90
    else:
        angle = 0
    
    pwm.ChangeDutyCycle(angle * 100)
    print("현재 서보모터 각도:", angle)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        set_servo_angle(pulse_duration)
    print("PWM 값:", round(pulse_duration, 3))  # 소수점 3자리까지 출력

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 경고 메시지 비활성화
GPIO.setup(pwm_pin, GPIO.OUT)  # PWM 핀을 출력으로 설정
GPIO.setup(servo_pin, GPIO.OUT)  # 서보 모터 핀을 출력으로 설정

pwm = GPIO.PWM(pwm_pin, 50)  # PWM 객체를 생성
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
