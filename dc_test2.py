import RPi.GPIO as GPIO
import time

motor_in1_pin = 17  # DIR 핀
motor_pwm_pin = 18  # PWM 핀

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.setup(motor_pwm_pin, GPIO.OUT)

pwm = GPIO.PWM(motor_pwm_pin, 100)  # PWM 주파수를 100Hz로 설정
pwm.start(0)

try:
    while True:
        # 전진
        GPIO.output(motor_in1_pin, GPIO.HIGH)
        pwm.ChangeDutyCycle(50)  # 속도를 50%로 설정
        time.sleep(2)

        # 정지
        GPIO.output(motor_in1_pin, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)

        # 후진
        GPIO.output(motor_in1_pin, GPIO.LOW)
        pwm.ChangeDutyCycle(50)
        time.sleep(2)

        # 정지
        GPIO.output(motor_in1_pin, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
