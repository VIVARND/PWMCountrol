import RPi.GPIO as GPIO
import time

pwm_pin = 17  # PWM 신호를 읽을 GPIO 핀
motor_in1_pin = 18  # DIR 핀
SPEED_MIN = 900
SPEED_MAX = 1100

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin, GPIO.IN)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.output(motor_in1_pin, GPIO.LOW)  # 초기에는 모터 OFF로 설정

def control_dc_motor(pwm_value, speed):
    if SPEED_MIN <= pwm_value <= SPEED_MAX:
        # PWM 값에 따라 모터 상태 결정
        GPIO.output(motor_in1_pin, GPIO.HIGH)  # 모터 ON
        print(f"DC 모터 ON - 속도: {speed}%")
    else:
        GPIO.output(motor_in1_pin, GPIO.LOW)  # 모터 OFF
        print("DC 모터 OFF")

try:
    while True:
        pulse_start = time.time()
        pulse_end = pulse_start
        while GPIO.input(pwm_pin) == GPIO.HIGH:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start

        if pulse_duration != 0.0:
            pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
            speed = (pwm_value - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100  # 속도 계산
            print("PWM 값:", pwm_value)

            # PWM 값에 따라 DC 모터 상태 결정
            control_dc_motor(pwm_value, speed)
        time.sleep(0.5)  # 0.5초 간격으로 PWM 값을 확인

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
