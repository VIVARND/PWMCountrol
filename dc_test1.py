import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정
DC_MOTOR_PIN = 18  # DC 모터의 신호선에 연결

# GPIO 핀을 출력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

try:
    while True:
        # DC 모터를 ON 상태로 설정
        GPIO.output(DC_MOTOR_PIN, GPIO.HIGH)
        
        # 현재 GPIO 핀의 상태를 읽어와 출력
        motor_signal = GPIO.input(DC_MOTOR_PIN)
        print(f"DC 모터 신호 값: {motor_signal}")

        time.sleep(1)  # 1초 동안 대기

except KeyboardInterrupt:
    GPIO.cleanup()
