import RPi.GPIO as GPIO
import time

pwm_pin_from_receiver = 17  # R3008SB의 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 핀

SPEED_MIN = 1200
SPEED_MAX = 1900

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver, GPIO.IN)
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.output(motor_in1_pin, GPIO.LOW)  # 초기에는 모터 OFF로 설정

pwm = GPIO.PWM(motor_pwm_pin, 100)  # PWM 주파수를 100Hz로 설정
pwm.start(0)

def control_dc_motor(speed):
    if SPEED_MIN <= speed <= SPEED_MAX:
        GPIO.output(motor_in1_pin, GPIO.HIGH)  # 모터 ON
        pwm.ChangeDutyCycle(100 - speed)  # 반전된 속도값 사용
        print(f"DC 모터 ON - 속도: {speed:.1f}%")
    else:
        GPIO.output(motor_in1_pin, GPIO.LOW)  # 모터 OFF
        print("DC 모터 OFF")

try:
    while True:
        GPIO.wait_for_edge(pwm_pin_from_receiver, GPIO.RISING)
        pulse_start = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver, GPIO.FALLING)
        pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start

        if pulse_duration != 0.0:
            pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
            speed = min(100, max(0, (pwm_value - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100))  # 속도 계산 (0 ~ 100)

            print("PWM 값:", pwm_value)

            # PWM 값에 따라 DC 모터 상태 결정
            control_dc_motor(speed)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
