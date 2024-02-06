import time
import RPi.GPIO as GPIO

pwm_pin_from_receiver_dc = 17  # DC 모터 PWM 신호를 읽을 GPIO 핀
pwm_pin_from_receiver_servo = 23  # 서보 모터 PWM 신호를 읽을 GPIO 핀
motor_pwm_pin = 18  # DC 모터 PWM 핀
motor_in1_pin = 22  # DC 모터 제어 DIR 핀
servo_pwm_pin = 24  # 서보 모터 PWM 핀

SPEED_MIN = 1200
SPEED_MAX = 1950
SPEED_STEP = 10  # DC 모터 속도를 10씩 증가시키도록 변경

SERVO_MIN = 950
SERVO_MAX = 1950

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

def control_dc_motor(pwm_value):
    speed = min(100, max(0, (pwm_value - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100))
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

            # PWM1 신호 및 DC 모터 상태 출력
            print(f"PWM1 신호: {pwm_value_dc}")
            if pwm_value_dc < SPEED_MIN:
                control_dc_motor(0)  # 속도가 0인 경우 모터 정지
            elif pwm_value_dc <= SPEED_MAX:
                if pwm_value_dc > SPEED_MIN + SPEED_STEP:  # 최소 속도에서 STEP 이상인 경우에만 증가
                    control_dc_motor(pwm_value_dc - SPEED_STEP)
                else:
                    control_dc_motor(SPEED_MIN)
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
            if SERVO_MIN <= pwm_value_servo <= SERVO_MAX:
                if 900 <= pwm_value_servo <= 1150:
                    set_servo_angle(0)
                elif 1100 < pwm_value_servo <= 1250:
                    set_servo_angle(30)
                elif 1300 <= pwm_value_servo <= 1450:
                    set_servo_angle(60)
                elif 1500 <= pwm_value_servo <= 1650:
                    set_servo_angle(90)
                elif 1800 <= pwm_value_servo <= 1950:
                    set_servo_angle(120)

except KeyboardInterrupt:
    pass

finally:
    dc_motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
