#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os

# 현재 스크립트의 경로 출력
script_path = os.path.realpath(__file__)
print(f"현재 스크립트 경로: {script_path}")

pwm_pin_from_receiver_dc = 17  # DC 모터 PWM 신호를 읽을 GPIO 핀
pwm_pin_from_receiver_servo = 23  # 서보 모터 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 DIR 핀
servo_pwm_pin = 24  # 서보 모터 PWM 핀

SPEED_MIN = 1200
SPEED_MAX = 1950
SPEED_STEP = 10  # DC 모터 속도를 10씩 증가시키도록 변경

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_from_receiver_dc, GPIO.IN)
GPIO.setup(pwm_pin_from_receiver_servo, GPIO.IN)
GPIO.setup(motor_pwm_pin, GPIO.OUT)
GPIO.setup(motor_in1_pin, GPIO.OUT)
GPIO.setup(servo_pwm_pin, GPIO.OUT)
GPIO.output(motor_in1_pin, GPIO.LOW)  # DC 모터를 A방향으로 설정

dc_motor_pwm = GPIO.PWM(motor_pwm_pin, 100)  # DC 모터 PWM 주파수를 100Hz로 설정
servo_pwm = GPIO.PWM(servo_pwm_pin, 50)  # 서보 모터 PWM 주파수를 50Hz로 설정
dc_motor_pwm.start(0)
servo_pwm.start(0)

def control_dc_motor(speed):
    if speed == 0:
        dc_motor_pwm.ChangeDutyCycle(0)  # DC 모터 OFF
        print("PWM1 - DC 모터 OFF")
    else:
        dc_motor_pwm.ChangeDutyCycle(speed)  # DC 모터 속도값 사용
        print(f"PWM1 - DC 모터 ON - 속도: {speed:.1f}%")

def set_servo_angle(angle):
    duty_cycle = angle / 18.0 + 2.5  # 각도에 따른 PWM 듀티 사이클 계산
    servo_pwm.ChangeDutyCycle(duty_cycle)
    print(f"PWM2 - 현재 서보모터 각도: {angle}도")

try:
    while True:
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.RISING)
        pulse_start_dc = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_dc, GPIO.FALLING)
        pulse_end_dc = time.time()

        pulse_duration_dc = pulse_end_dc - pulse_start_dc

        if pulse_duration_dc != 0.0:
            pwm_value_dc = round(pulse_duration_dc * 1000000)  # PWM 값 변환 (마이크로초로 변환)
            
            # 범위 확인
            if SPEED_MIN <= pwm_value_dc <= SPEED_MAX:
                speed_dc = (pwm_value_dc - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100  # 속도 계산 (0 ~ 100)
                control_dc_motor(speed_dc)
                print(f"PWM1 신호: {pwm_value_dc}, PWM1 - DC 모터 ON - 속도: {speed_dc:.1f}%")
            else:
                control_dc_motor(0)  # 범위 밖이면 모터 정지
                print(f"PWM1 신호: {pwm_value_dc}, PWM1 - DC 모터 OFF (범위 밖)")

        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.RISING)
        pulse_start_servo = time.time()
        GPIO.wait_for_edge(pwm_pin_from_receiver_servo, GPIO.FALLING)
        pulse_end_servo = time.time()

        pulse_duration_servo = pulse_end_servo - pulse_start_servo

        if pulse_duration_servo != 0.0:
            pwm_value_servo = round(pulse_duration_servo * 1000000)  # PWM 값 변환 (마이크로초로 변환)

            # 범위 확인
            if 900 <= pwm_value_servo <= 2050:
                if 900 <= pwm_value_servo <= 1200:
                    set_servo_angle(0)
                elif 1250 < pwm_value_servo <= 1400:
                    set_servo_angle(30)
                elif 1450 <= pwm_value_servo <= 1600:
                    set_servo_angle(60)
                elif 1650 <= pwm_value_servo <= 1800:
                    set_servo_angle(90)
                elif 1850 <= pwm_value_servo <= 2050:
                    set_servo_angle(120)
                print(f"PWM2 신호: {pwm_value_servo}")
            else:
                set_servo_angle(0)  # 범위 밖이면 서보 모터 정지
                print(f"PWM2 신호: {pwm_value_servo}, PWM2 - 서보 모터 OFF (범위 밖)")

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
