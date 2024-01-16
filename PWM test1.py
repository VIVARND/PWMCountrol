import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
input_pin = 18  # PWM 입력 핀 (라즈베리 파이의 GPIO 핀 번호에 따라 수정)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)

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
    print("PWM 읽기를 시작합니다. Ctrl+C를 눌러서 종료하세요.")
    while True:
        # PWM 신호 읽기
        pwm_value = read_pwm()

        # PWM 신호를 어떻게 활용할지는 여기에 추가로 작성
        # 예: 화면에 출력
        print(f"PWM Value: {pwm_value}")

        time.sleep(0.1)  # 0.1초 대기

except KeyboardInterrupt:
    print("사용자에 의해 프로그램이 종료되었습니다.")

finally:
    # 종료 시 GPIO 정리
    GPIO.cleanup()
