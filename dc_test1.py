import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정
DC_MOTOR_PIN = 18  # DC 모터의 신호선에 연결

# GPIO 핀을 출력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

# PWM 객체 생성
motor_pwm = GPIO.PWM(DC_MOTOR_PIN, 100)  # PWM 주파수 100Hz

def operate_motor(speed):
    motor_pwm.start(speed)
    print(f"DC 모터 회전 중 (속도: {speed}%)")

try:
    while True:
        # 사용자로부터 속도 입력 받아 모터 회전
        speed = float(input("DC 모터 속도 (0~100%): "))
        operate_motor(speed)
        time.sleep(2)  # 2초 동안 회전

except KeyboardInterrupt:
    motor_pwm.stop()
    GPIO.cleanup()
