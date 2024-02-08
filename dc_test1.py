import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
DIR_PIN = 18  # 모터의 회전 방향을 제어하는 GPIO 핀
PWM_PIN = 19  # 모터의 속도를 제어하는 PWM 핀

# GPIO 핀을 출력 모드로 설정
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)

# PWM 객체 생성
pwm_motor = GPIO.PWM(PWM_PIN, 100)  # PWM 주파수 100Hz

try:
    while True:
        # 모터를 정방향으로 회전
        GPIO.output(DIR_PIN, GPIO.HIGH)
        
        # PWM을 사용하여 모터 속도를 제어 (0~100 사이의 값을 입력)
        speed = float(input("속도를 입력하세요 (0~100): "))
        pwm_motor.start(speed)

        time.sleep(2)

        # 모터를 역방향으로 회전
        GPIO.output(DIR_PIN, GPIO.LOW)
        
        # PWM을 사용하여 모터 속도를 제어 (0~100 사이의 값을 입력)
        speed = float(input("속도를 입력하세요 (0~100): "))
        pwm_motor.start(speed)

        time.sleep(2)

except KeyboardInterrupt:
    # 프로그램 종료 시 PWM 정지 및 GPIO 정리
    pwm_motor.stop()
    GPIO.cleanup()
