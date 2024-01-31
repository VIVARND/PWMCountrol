import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
pwm_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)

try:
    while True:
        # PWM 신호 읽기
        pwm_value = GPIO.input(pwm_pin)

        # 디지털 값으로 출력
        print(f"PWM Value: {pwm_value}")

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    GPIO.cleanup()
