import RPi.GPIO as GPIO
import time

# 모터 제어를 위한 GPIO 핀 설정
motor_pwm_pin = 18  # PWM 제어 핀
motor_in1_pin = 23  # 모터 입력1
motor_in2_pin = 24  # 모터 입력2

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# PWM 객체 초기화
pwm_frequency = 1000  # Hz
pwm = GPIO.PWM(motor_pwm_pin, pwm_frequency)
pwm.start(0)  # 초기 듀티 사이클: 0%

# 모터 제어 핀 초기화
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.setup(motor_in2_pin, GPIO.OUT)

try:
    while True:
        # 모터를 시계방향으로 회전
        GPIO.output(motor_in1_pin, GPIO.HIGH)
        GPIO.output(motor_in2_pin, GPIO.LOW)
        pwm.ChangeDutyCycle(50)  # 듀티 사이클: 50%
        time.sleep(2)

        # 모터를 반시계방향으로 회전
        GPIO.output(motor_in1_pin, GPIO.LOW)
        GPIO.output(motor_in2_pin, GPIO.HIGH)
        pwm.ChangeDutyCycle(50)  # 듀티 사이클: 50%
        time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
