
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
PWM_PIN = 18

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.IN)

try:
    while True:
        # PWM 신호 읽기
        GPIO.wait_for_edge(PWM_PIN, GPIO.BOTH)  # 에지를 기다립니다 (상승 또는 하강 에지).
        start_time = time.time()

        GPIO.wait_for_edge(PWM_PIN, GPIO.BOTH)  # 다음 에지를 기다립니다.
        end_time = time.time()

        # 펄스 지속 시간 계산
        pulse_duration = end_time - start_time

        # PWM 주기 (T) 계산 (초)
        pwm_period = pulse_duration * 2

        # PWM 주파수 (f) 계산 (Hz)
        pwm_frequency = 1 / pwm_period

        # PWM 신호 주기 계산 (%)
        pwm_duty_cycle = pulse_duration / pwm_period * 100

        # 결과 출력
        print(f"PWM 주기: {pwm_period:.6f} 초")
        print(f"PWM 주파수: {pwm_frequency:.2f} Hz")
        print(f"PWM 듀티 사이클: {pwm_duty_cycle:.2f} %")
        print("")

except KeyboardInterrupt:
    GPIO.cleanup()  # Ctrl+C를 눌렀을 때 GPIO 정리
