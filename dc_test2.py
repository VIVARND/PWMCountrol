import RPi.GPIO as GPIO
import time

# 모터 제어를 위한 GPIO 핀
motor_pin = 17

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(motor_pin, GPIO.OUT)

# PWM 주파수와 초기 듀티 사이클 설정
pwm_frequency = 50  # Hz
initial_duty_cycle = 0  # 0% (OFF 상태)

# PWM 객체 초기화
pwm = GPIO.PWM(motor_pin, pwm_frequency)
pwm.start(initial_duty_cycle)

try:
    while True:
        # DC 모터를 1초 동안 회전 (최대 속도)
        pwm.ChangeDutyCycle(100)  # 100% (최대 속도)
        time.sleep(1)

        # DC 모터를 1초 동안 정지
        pwm.ChangeDutyCycle(0)  # 0% (정지)
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
