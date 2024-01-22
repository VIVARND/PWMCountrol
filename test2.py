import RPi.GPIO as GPIO
import time

# RC 조종기 핀 설정
rc_pin = 14  # RC 조종기 신호 핀 번호

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(rc_pin, GPIO.IN)

try:
    print("Reading PWM signals from RC controller...")

    while True:
        pulse_width = GPIO.input(rc_pin)
        # GPIO.input() 함수는 0 또는 1을 반환하므로, 이 값을 사용하여 PWM 값을 읽을 수 있습니다.

        # 10번 채널 값 출력
        print("Channel 10 PWM:", pulse_width)

        time.sleep(0.1)

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 리소스 해제
    GPIO.cleanup()
    print("Program terminated.")    print("Program terminated.")
