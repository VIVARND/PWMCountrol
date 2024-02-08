import time
import RPi.GPIO as GPIO

pwm_pin_from_receiver_dc = 17  # DC 모터 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀

SPEED_MIN = 1200
SPEED_MAX = 1950
SPEED_STEP = 10  # DC 모터 속도를 10씩 증가시키도록 변경

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver_dc, GPIO.IN)
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.output(motor_pwm_pin, GPIO.LOW)  # DC 모터를 A방향으로 설정

dc_motor_pwm = GPIO.PWM(motor_pwm_pin, 100)  # DC 모터 PWM 주파수를 100Hz로 설정
dc_motor_pwm.start(0)

def control_dc_motor(speed):
    if speed == 0:
        dc_motor_pwm.ChangeDutyCycle(0)  # DC 모터 OFF
        print("PWM1 - DC 모터 OFF")
    else:
        dc_motor_pwm.ChangeDutyCycle(speed)  # DC 모터 속도값 사용
        print(f"PWM1 - DC 모터 ON - 속도: {speed:.1f}%")

try:
    while True:
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.RISING)
        pulse_start_dc = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.FALLING)
        pulse_end_dc = time.time()

        pulse_duration_dc = pulse_end_dc - pulse_start_dc

        if pulse_duration_dc != 0.0:
            pwm_value_dc = round(pulse_duration_dc * 1000000)  # PWM 값 변환 (마이크로초로 변환)
            speed_dc = min(100, max(0, (pwm_value_dc - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100))  # 속도 계산 (0 ~ 100)

            # PWM1 신호 및 DC 모터 상태 출력
            print(f"PWM1 신호: {pwm_value_dc}")
            if pwm_value_dc < SPEED_MIN:
                control_dc_motor(0)  # 속도가 0인 경우 모터 정지
            elif pwm_value_dc <= SPEED_MAX:
                control_dc_motor(speed_dc)
            else:
                control_dc_motor(100)  # 최대 속도로 모터 동작

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
