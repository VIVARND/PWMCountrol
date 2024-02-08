import RPi.GPIO as GPIO
import time

servo_pin = 18  # GPIO 핀 번호 설정

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

servo_pwm = GPIO.PWM(servo_pin, 50)  # PWM 주파수를 50Hz로 설정
servo_pwm.start(0)

def set_servo_angle(angle):
    duty_cycle = angle / 18.0 + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # 서보모터가 움직일 시간을 설정

try:
    while True:
        set_servo_angle(0)    # 0도로 이동
        set_servo_angle(90)   # 90도로 이동

except KeyboardInterrupt:
    pass

finally:
    servo_pwm.stop()
    GPIO.cleanup()
