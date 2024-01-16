import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
input_pin = 18  # PWM 입력 핀 (라즈베리 파이의 GPIO 핀 번호에 따라 수정)

# 10번 채널에 해당하는 변수
channel_10_pin = 10

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(channel_10_pin, GPIO.OUT)

# PWM 객체 생성
channel_10_pwm = GPIO.PWM(channel_10_pin, 50)  # 주파수 50Hz

def read_pwm():
    start_time = time.time()

    # PWM 신호의 rising edge 기다리기
    while GPIO.input(input_pin) == GPIO.LOW:
        pass

    # rising edge 이후, falling edge 까지의 시간 측정
    while GPIO.input(input_pin) == GPIO.HIGH:
        pass
    pulse_duration = time.time() - start_time

    return pulse_duration

try:
    # PWM 시작
    channel_10_pwm.start(0)

    print("10번 채널 PWM 읽기를 시작합니다. Ctrl+C를 눌러서 종료하세요.")
    while True:
        # PWM 신호 읽기
        pwm_value = read_pwm()

        # PWM 값을 10번 채널에 적용
        duty_cycle = (pwm_value / 0.02) + 3
        channel_10_pwm.ChangeDutyCycle(duty_cycle)

        # 10번 채널 PWM 신호 출력
        print(f"10번 채널 PWM Value: {pwm_value}")

        time.sleep(0.5)  # 0.5초 대기

except KeyboardInterrupt:
    print("사용자에 의해 프로그램이 종료되었습니다.")

finally:
    # 종료 시 PWM 및 GPIO 정리
    channel_10_pwm.stop()
    GPIO.cleanup()
