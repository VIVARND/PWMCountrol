import RPi.GPIO as GPIO
import time

pwm_pin_from_receiver = 17  # R3008SB의 PWM 신호를 읽을 GPIO 핀
dc_motor_pwm_pin = 18  # DC 모터 PWM 핀
servo_pwm_pin = 23  # 서보 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 핀

SPEED_MIN = 1200
SPEED_MAX = 2000
SPEED_STEP = 10  # DC 모터 속도를 10씩 증가시키도록 변경

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver, GPIO.IN)
GPIO.setup(dc_motor_pwm_pin, GPIO.OUT)
GPIO.setup(servo_pwm_pin, GPIO.OUT)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.output(motor_in1_pin, GPIO.LOW)  # DC 모터를 A방향으로 설정

dc_motor_pwm = GPIO.PWM(dc_motor_pwm_pin, 100)  # DC 모터 PWM 주파수를 100Hz로 설정
servo_pwm = GPIO.PWM(servo_pwm_pin, 50)  # 서보 모터 PWM 주파수를 50Hz로 설정
dc_motor_pwm.start(0)
servo_pwm.start(0)

def control_dc_motor(speed):
    if speed == 0:
        dc_motor_pwm.ChangeDutyCycle(0)  # DC 모터 OFF
    else:
        dc_motor_pwm.ChangeDutyCycle(speed)  # DC 모터 속도값 사용

def set_servo_angle(angle):
    duty_cycle = angle / 18.0 + 2.5  # 각도에 따른 PWM 듀티 사이클 계산
    servo_pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        GPIO.wait_for_edge(pwm_pin_from_receiver, GPIO.RISING)
        pulse_start = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver, GPIO.FALLING)
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        if pulse_duration != 0.0:
            pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
            speed = min(100, max(0, (pwm_value - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100))

            # PWM1 신호 출력
            print(f"PWM1 신호: {pwm_value}")
            
            # 서보모터 각도 설정 및 출력
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
            print(f"서보모터 각도: {servo_pwm._current_duty_cycle}")
            
            # PWM2 신호 및 DC 모터 속도 출력
            print(f"PWM2 신호: {speed}")
            control_dc_motor(speed)

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
