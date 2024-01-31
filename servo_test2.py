import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
pwm_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)

try:
    while True:
        pwm_value = GPIO.input(pwm_pin)
        print(f"PWM Value: {pwm_value}")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    GPIO.cleanup()
