import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정
DC_MOTOR_PIN = 18  # DC 모터의 신호선에 연결

# GPIO 핀을 출력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

def operate_motor():
    try:
        while True:
            user_input = input("DC 모터를 켜려면 'on', 끄려면 'off'를 입력하세요 (종료하려면 'exit'): ")
            
            if user_input.lower() == 'on':
                GPIO.output(DC_MOTOR_PIN, GPIO.HIGH)  # DC 모터를 ON으로 설정
                print("DC 모터 켜짐")
            elif user_input.lower() == 'off':
                GPIO.output(DC_MOTOR_PIN, GPIO.LOW)  # DC 모터를 OFF로 설정
                print("DC 모터 꺼짐")
            elif user_input.lower() == 'exit':
                break
            else:
                print("올바른 명령을 입력하세요.")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# DC 모터 동작 시작
operate_motor()
