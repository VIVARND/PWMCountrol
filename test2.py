import pigpio
import time

# RC 조종기 핀 설정
rc_pin = 14  # RC 조종기 신호 핀 번호

# GPIO 설정
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio. Make sure pigpiod is running.")
    exit()

try:
    print("Reading PWM signals from RC controller...")

    while True:
        pulse_width = pi.get_servo_pulsewidth(rc_pin, 10)  # 최근 10개의 샘플을 사용하여 중간값 계산

        if pulse_width > 0:
            # 10번 채널 값 출력
            print("Channel 10 PWM:", pulse_width)

        time.sleep(0.1)

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 리소스 해제
    pi.stop()
    print("Program terminated.")
