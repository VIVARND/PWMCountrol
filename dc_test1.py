import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
DC_MOTOR_PIN = 27  # DC 모터의 신호선에 연결

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

def rotate_motor(duration):
    GPIO.output(DC_MOTOR_PIN, GPIO.HIGH)  # DC 모터를 ON으로 설정 (회전)
    print("DC 모터 회전 중...")
    time.sleep(duration)  # 지정된 시간 동안 회전
    GPIO.output(DC_MOTOR_PIN, GPIO.LOW)  # DC 모터를 OFF로 설정 (정지)
    print("DC 모터 멈춤")

try:
    while True:
        # DC 모터를 2초 동안 회전하고 2초 동안 멈춤
        rotate_motor(2)
        time.sleep(2)  # 2초 대기 후 반복

except KeyboardInterrupt:
    GPIO.cleanup()
