import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
servo_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM 설정
pwm = GPIO.PWM(servo_pin, 50)  # 주파수는 50Hz로 설정

# PWM 시작
pwm.start(0)

try:
    while True:
        # 여기에서 T16SZ 조종기에서 읽은 PWM 신호 값을 사용
        # (T16SZ에서 읽은 값을 input_pwm 변수에 할당한다고 가정)
        input_pwm = float(input("Enter PWM value (0 to 100): "))
        
        # PWM 값 변환 (0~100을 2~12 범위로 변환)
        duty_cycle = (input_pwm / 100.0) * 10.0 + 2.0

        # PWM 업데이트
        pwm.ChangeDutyCycle(duty_cycle)

        # 사용자에게 현재 PWM 값 출력
        print(f"Current PWM value: {input_pwm}")

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    pwm.stop()
    GPIO.cleanup()
