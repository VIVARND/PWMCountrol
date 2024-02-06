import RPi.GPIO as GPIO
import time

pwm_pin_from_receiver_dc = 17  # DC 모터 PWM 신호를 읽을 GPIO 핀
pwm_pin_from_receiver_servo = 23  # 서보 모터 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 DIR 핀
servo_pwm_pin = 24  # 서보 모터 PWM 핀

SPEED_MIN = 1200
SPEED_MAX = 1950
SPEED_STEP = 10  # DC 모터 속도를 10씩 증가시키도록 변경

SERVO_MIN = 900
SERVO_MAX = 1950

SERVO_ANGLES = {
    (900, 1150): 0,
    (1150, 1300): 30,
    (1300, 1500): 60,
    (1500, 1700): 90,
    (1700, 1950): 120
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = [
    pwm_pin_from_receiver_dc,
    pwm_pin_from_receiver_servo,
    motor_pwm_pin,
    motor_in1_pin,
    servo_pwm_pin
]

# GPIO 핀을 입력으로 설정
for pin in pins:
    GPIO.setup(pin, GPIO.IN)

# GPIO 핀을 출력으로 설정
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.setup(servo_pwm_pin, GPIO.OUT)

# DC 모터 초기 설정
GPIO.output(motor_in1_pin, GPIO.LOW)
dc_motor_pwm = GPIO.PWM(motor_pwm_pin, 100)
dc_motor_pwm.start(0)

# 서보 모터 초기 설정
servo_pwm = GPIO.PWM(servo_pwm_pin, 50)
servo_pwm.start(0)

speed_dc = 0  # 전역 변수로 속도 값 초기화

# 서보 모터 각도 설정 함수 정의
def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pwm_pin, True)
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # 서보 모터의 안정적인 움직임을 위한 추가 대기 시간
    GPIO.output(servo_pwm_pin, False)
    servo_pwm.ChangeDutyCycle(0)

# DC 모터 제어 함수 정의
def control_dc_motor(speed):
    global speed_dc
    if speed == 0:
        dc_motor_pwm.ChangeDutyCycle(0)  # DC 모터 OFF
        print("PWM1 - DC 모터 OFF")
        speed_dc = 0
    else:
        dc_motor_pwm.ChangeDutyCycle(speed)  # DC 모터 속도값 사용
        speed_dc = speed

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

        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.RISING)
        pulse_start_servo = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.FALLING)
        pulse_end_servo = time.time()

        pulse_duration_servo = pulse_end_servo - pulse_start_servo

        if pulse_duration_servo != 0.0:
            pwm_value_servo = round(pulse_duration_servo * 1000000)  # PWM 값 변환 (마이크로초로 변환)

            # PWM2 신호 및 서보모터 각도 출력
            print(f"PWM2 신호: {pwm_value_servo}")
            for (min_value, max_value), angle in SERVO_ANGLES.items():
                if min_value <= pwm_value_servo <= max_value:
                    set_servo_angle(angle)
                    break

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
