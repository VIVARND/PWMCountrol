import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀 (라즈베리파이에 연결된 실제 핀 번호에 따라 수정하세요)

def set_servo_angle(angle):
    # 각도에 따라 PWM 신호 값을 설정합니다.
    if angle == 10:
        # 10도에 해당하는 PWM 신호 값
        # 서보 모터에 맞게 수정이 필요할 수 있습니다.
        # 실제 서보 모터와 PWM 신호 값 사이의 매핑을 확인하세요.
        pwm_value = 0.0090
    elif angle == 40:
        # 40도에 해당하는 PWM 신호 값
        pwm_value = 0.0013
    elif angle == 90:
        # 90도에 해당하는 PWM 신호 값
        pwm_value = 0.0017
    else:
        # 기타 경우, 멈춤
        pwm_value = 0
    
    # 서보 모터에 PWM 신호 값을 전달합니다.
    # 이 부분은 실제 서보 모터에 따라 적절히 수정해야 할 수 있습니다.
    # PWM 신호와 서보 모터 각도 사이의 매핑은 제조사의 데이터시트를 참조하세요.
    # pwm.ChangeDutyCycle()을 사용하여 PWM 신호를 설정합니다.
    # 실제 동작을 확인하면서 매핑을 조정해야 할 수 있습니다.
    pwm.ChangeDutyCycle(pwm_value * 100)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start  # pulse_end 초기화
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        # PWM 값을 분석하여 각도를 설정합니다.
        if 0.0090 <= pulse_duration <= 0.0011:
            set_servo_angle(10)
        elif 0.0012 <= pulse_duration <= 0.0014:
            set_servo_angle(40)
        elif 0.0015 <= pulse_duration <= 0.0019:
            set_servo_angle(90)
        else:
            # 기타 경우, 서보 모터를 멈춤
            set_servo_angle(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)  # 서보 모터 핀을 출력으로 설정합니다.

pwm = GPIO.PWM(pwm_pin, 50)  # PWM 객체를 생성합니다.
pwm.start(0)  # PWM 신호를 초기화합니다.

GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

# PWM 신호를 읽고 서보 모터를 제어합니다.
try:
    while True:
        time.sleep(0.1)  # 주기적으로 PWM 값을 확인하는 주기를 늦추었습니다.
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()  # PWM 객체를 정리합니다.
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
