import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
DC_MOTOR_PWM_PIN = 18  # DC 모터의 PWM 신호선에 연결

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC_MOTOR_PWM_PIN, GPIO.OUT)

# PWM 객체 생성
motor_pwm = GPIO.PWM(DC_MOTOR_PWM_PIN, 100)  # PWM 주파수 100Hz

def operate_motor(speed):
    motor_pwm.start(speed)
    print(f"DC 모터 회전 중 (속도: {speed}%)")

try:
    while True:
        # 사용자에게 속도를 입력받아 DC 모터 회전
        speed = float(input("DC 모터 속도 (0~100%): "))
        operate_motor(speed)
        time.sleep(2)  # 2초 동안 회전

except KeyboardInterrupt:
    motor_pwm.stop()
    GPIO.cleanup()
