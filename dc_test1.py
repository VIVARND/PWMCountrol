import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# DC 모터 신호선 핀 설정
PWM_PIN = 18  # 예시, DC 모터의 PWM 신호선에 연결된 GPIO 핀 번호로 수정

# GPIO 핀을 출력 모드로 설정
GPIO.setup(PWM_PIN, GPIO.OUT)

# PWM 객체 생성
pwm_motor = GPIO.PWM(PWM_PIN, 100)  # PWM 주파수 100Hz

try:
    while True:
        # PWM 값을 사용하여 DC 모터 속도 제어 (0~100 사이의 값을 입력)
        speed = float(input("속도를 입력하세요 (0~100): "))
        pwm_motor.start(speed)

        time.sleep(2)

except KeyboardInterrupt:
    # 프로그램 종료 시 PWM 정지 및 GPIO 정리
    pwm_motor.stop()
    GPIO.cleanup()
