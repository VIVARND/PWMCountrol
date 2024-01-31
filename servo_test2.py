import pigpio
import time

# 사용할 GPIO 핀 번호 설정 (예: 18)
pwm_pin = 18

# pigpio 객체 생성
pi = pigpio.pi()

try:
    while True:
        # PWM 신호 읽기
        pwm_value = pi.read(pwm_pin)

        # 디지털 값으로 출력
        print(f"PWM Value: {pwm_value}")

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # pigpio 객체 정리
    pi.stop()
