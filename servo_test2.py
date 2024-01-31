import serial
import RPi.GPIO as GPIO

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
    # 시리얼 포트 설정 (사용 가능한 포트로 수정)
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    while True:
        # 시리얼 데이터 읽기
        serial_data = ser.readline().decode('utf-8').strip()
        
        try:
            # 시리얼 데이터를 부동 소수점으로 변환
            input_pwm = float(serial_data)

            # PWM 값 변환 (0~100을 2~12 범위로 변환)
            duty_cycle = (input_pwm / 100.0) * 10.0 + 2.0

            # PWM 업데이트
            pwm.ChangeDutyCycle(duty_cycle)

            # 사용자에게 현재 PWM 값 출력
            print(f"Current PWM value: {input_pwm}")

        except ValueError:
            # 부동 소수점으로 변환할 수 없는 경우
            print("Invalid data received")

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    pwm.stop()
    GPIO.cleanup()
