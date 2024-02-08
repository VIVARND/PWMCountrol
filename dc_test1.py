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
        # DC 모터를 50% 속도로 회전
        operate_motor(50)
        time.sleep(2)  # 2초 동안 회전

except KeyboardInterrupt:
    motor_pwm.stop()
    GPIO.cleanup()
