import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# DC 모터 제어 핀 설정
MOTOR_PIN = 22  # 예시, 모터의 신호선에 연결된 GPIO 핀 번호로 수정

# GPIO 핀을 출력 모드로 설정
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def set_motor_direction(direction):
    if direction == "forward":
        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        print("DC 모터 정방향 동작 중...")
    elif direction == "backward":
        GPIO.output(MOTOR_PIN, GPIO.LOW)
        print("DC 모터 역방향 동작 중...")
    else:
        print("올바르지 않은 방향입니다.")

try:
    while True:
        # DC 모터를 정방향으로 회전
        set_motor_direction("forward")
        time.sleep(2)

        # DC 모터를 역방향으로 회전
        set_motor_direction("backward")
        time.sleep(2)

except KeyboardInterrupt:
    # GPIO 정리
    GPIO.cleanup()
