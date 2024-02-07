import RPi.GPIO as GPIO
import time

pwm_pin_from_receiver_dc = 17  # DC 모터 PWM 신호를 읽을 GPIO 핀
pwm_pin_from_receiver_servo = 23  # 서보 모터 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
servo_pwm_pin = 24  # 서보 모터 PWM 핀

SPEED_MIN_DC = 900
SPEED_MAX_DC = 1200
SPEED_MIN_SERVO = 900
SPEED_MAX_SERVO = 2000

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver_dc, GPIO.IN)
GPIO.setup(pwm_pin_from_receiver_servo, GPIO.IN)
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.setup(servo_pwm_pin, GPIO.OUT)

dc_motor_pwm = GPIO.PWM(motor_pwm_pin, 100)  # DC 모터 PWM 주파수를 100Hz로 설정
servo_pwm = GPIO.PWM(servo_pwm_pin, 50)  # 서보 모터 PWM 주파수를 50Hz로 설정
dc_motor_pwm.start(0)
servo_pwm.start(0)

def control_dc_motor(pwm_value_dc):
    if SPEED_MIN_DC <= pwm_value_dc <= SPEED_MAX_DC:
        dc_motor_pwm.ChangeDutyCycle(100)  # DC 모터 ON
        print("PWM1 - DC 모터 ON")
    else:
        dc_motor_pwm.ChangeDutyCycle(0)  # DC 모터 OFF
        print("PWM1 - DC 모터 OFF")

def set_servo_angle(pwm_value_servo):
    if SPEED_MIN_SERVO <= pwm_value_servo <= SPEED_MAX_SERVO:
        angle = (pwm_value_servo - SPEED_MIN_SERVO) / (SPEED_MAX_SERVO - SPEED_MIN_SERVO) * 90  # 0 ~ 90도 변환
        set_servo_angle(angle)
    else:
        stop_servo()  # 서보모터 정지

def set_servo_angle(angle):
    duty_cycle = angle / 18.0 + 2.5  # 각도에 따른 PWM 듀티 사이클 계산
    servo_pwm.ChangeDutyCycle(duty_cycle)
    print(f"PWM2 - 현재 서보모터 각도: {angle:.1f}도")

def stop_servo():
    servo_pwm.ChangeDutyCycle(0)  # PWM 신호를 0으로 설정 (서보 모터 정지)
    print("PWM2 - 서보모터 정지")

try:
    while True:
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.RISING)
        pulse_start_dc = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.FALLING)
        pulse_end_dc = time.time()

        pulse_duration_dc = pulse_end_dc - pulse_start_dc

        if pulse_duration_dc != 0.0:
            pwm_value_dc = round(pulse_duration_dc * 1000000)  # PWM 값 변환 (마이크로초로 변환)

            # PWM1 신호 및 DC 모터 상태 출력
            print(f"PWM1 신호: {pwm_value_dc}")
            control_dc_motor(pwm_value_dc)

        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.RISING)
        pulse_start_servo = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.FALLING)
        pulse_end_servo = time.time()

        pulse_duration_servo = pulse_end_servo - pulse_start_servo

        if pulse_duration_servo != 0.0:
            pwm_value_servo = round(pulse_duration_servo * 1000000)  # PWM 값 변환 (마이크로초로 변환)

            # PWM2 신호 및 서보모터 각도 출력
            print(f"PWM2 신호: {pwm_value_servo}")
            set_servo_angle(pwm_value_servo)

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
