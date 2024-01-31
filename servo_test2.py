from gpiozero import InputDevice, PWMOutputDevice
import time

# GPIO 핀 번호 설정
pwm_pin = 18

# PWMOutputDevice 초기화
pwm_device = PWMOutputDevice(pwm_pin)

# InputDevice 초기화
input_device = InputDevice(pwm_pin)

try:
    while True:
        # PWM 신호 읽기
        pwm_value = pwm_device.value
        print(f"PWM Value: {pwm_value:.2f}")

        # 아날로그 값으로 변환 (0~100)
        analog_value = pwm_value * 100.0
        print(f"Analog Value: {analog_value:.2f}")

        # Digital 값 읽기
        digital_value = input_device.value
        print(f"Digital Value: {digital_value}")

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    pwm_device.close()
    input_device.close()
