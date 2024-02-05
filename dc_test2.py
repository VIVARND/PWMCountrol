import RPi.GPIO as GPIO
import time

pwm_pin_from_receiver = 17  # R3008SB의 PWM 신호를 읽을 GPIO 핀
motor_pin = 18  # DC 모터를 제어할 GPIO 핀
frequency = 50  # PWM 주파수 (Hz)

# PWM 값에 따른 모터 상태 설정
PWM_ON_MIN = 1200
PWM_ON_MAX = 1900

def control_dc_motor(pwm_value):
    if PWM_ON_MIN <= pwm_value <= PWM_ON_MAX:
        # PWM 값에 따라 모터 상태 결정
        GPIO.output(motor_pin, GPIO.HIGH)  # 모터 ON
        print(f"DC 모터 ON - 속도: {((pwm_value - PWM_ON_MIN) / (PWM_ON_MAX - PWM_ON_MIN)) * 100:.1f}%")
    else:
        GPIO.output(motor_pin, GPIO.LOW)  # 모터 OFF
        print("DC 모터 OFF")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin_from_receiver, GPIO.IN)  # R3008SB 수신기의 PWM 핀을 입력으로 설정
GPIO.setup(motor_pin, GPIO.OUT)  # DC 모터 제어를 위한 GPIO 핀
GPIO.output(motor_pin, GPIO.LOW)  # 초기에는 모터 OFF로 설정

try:
    GPIO.setup(pwm_pin_from_receiver, GPIO.OUT)  # PWM 핀을 출력으로 설정
    pwm = GPIO.PWM(pwm_pin_from_receiver, frequency)
    pwm.start(0)

    while True:
        pwm_value = GPIO.input(pwm_pin_from_receiver)
        pwm.ChangeDutyCycle((pwm_value / 4096) * 100)  # PWM 신호를 퍼센트로 변환
        print("PWM 값:", pwm_value)

        # PWM 값에 따라 DC 모터 상태 결정
        control_dc_motor(pwm_value)
        time.sleep(0.5)  # 0.5초 간격으로 PWM 값을 확인

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
