import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
pwm_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)

# PWM 초기화
pwm = GPIO.PWM(pwm_pin, 50)  # 주파수는 50Hz로 설정
pwm.start(0)

try:
    while True:
        # PWM 신호 읽기
        pwm_value = GPIO.input(pwm_pin)
        print(f"PWM Value: {pwm_value}")

        # 아날로그 값으로 변환 (0~100)
        analog_value = (pwm_value / 1.0) * 100.0
        print(f"Analog Value: {analog_value}")

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    pwm.stop()
    GPIO.cleanup()
