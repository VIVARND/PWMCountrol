import time
import RPi.GPIO as GPIO

pwm_pin_from_receiver = 17  # R3008SB의 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 핀

servo_pwm_pin = 23  # PWM 신호를 읽을 GPIO 핀
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀

SPEED_MIN = 1200
SPEED_MAX = 2000
SPEED_STEP = 10  # 속도를 10씩 증가시키도록 변경

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver, GPIO.IN)
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.output(motor_in1_pin, GPIO.LOW)  # 모터를 A방향으로 설정

GPIO.setup(servo_pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(servo_pin, GPIO.OUT)

motor_pwm = GPIO.PWM(motor_pwm_pin, 100)  # DC 모터 PWM 설정
motor_pwm.start(0)

servo_pwm = GPIO.PWM(servo_pin, 50)  # 서보 모터 PWM 설정
servo_pwm.start(0)

def control_dc_motor(speed):
    if speed == 0:
        motor_pwm.ChangeDutyCycle(0)  # 모터 OFF
        print("DC 모터 OFF")
    else:
        motor_pwm.ChangeDutyCycle(speed)  # 속도값 사용
        print(f"DC 모터 ON - 속도: {speed:.1f}%")

def set_servo_angle(angle):
    duty_cycle = angle / 18.0 + 2.5  # 각도에 따른 PWM 듀티 사이클 계산
    servo_pwm.ChangeDutyCycle(duty_cycle)
    print(f"현재 서보모터 각도: {angle}도")

def stop_servo():
    servo_pwm.ChangeDutyCycle(0)  # PWM 신호를 0으로 설정 (서보 모터 정지)
    print("서보모터 정지")

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
        print("PWM 값:", pwm_value)

        # PWM 값에 따라 DC 모터 상태 결정
        if pwm_value < SPEED_MIN:
            control_dc_motor(0)  # 속도가 0인 경우 모터 정지
        elif pwm_value <= SPEED_MAX:
            control_dc_motor(speed)
        else:
            control_dc_motor(100)  # 최대 속도로 모터 동작

        # PWM 값에 따라 서보모터 각도 설정
        if 900 <= pwm_value <= 1100:
            set_servo_angle(0)
        elif 1100 < pwm_value <= 1200:
            set_servo_angle(30)
        elif 1300 <= pwm_value <= 1400:
            set_servo_angle(60)
        elif 1500 <= pwm_value <= 1600:
            set_servo_angle(90)
        elif 1800 <= pwm_value <= 2000:
            set_servo_angle(120)
        else:
            stop_servo()

try:
    GPIO.add_event_detect(pwm_pin_from_receiver, GPIO.BOTH, callback=pwm_callback)
    while True:
        time.sleep(0.1)  # 작은 값으로 설정하여 실시간으로 PWM 값을 확인
except KeyboardInterrupt:
    pass
finally:
    motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
