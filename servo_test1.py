import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보모터의 신호선이 연결된 GPIO 핀

def set_servo_angle(angle):
    pulse_width = (angle / 180.0) * (2.5 - 0.5) + 0.5
    duty_cycle = pulse_width * 100 / 20
    pwm.ChangeDutyCycle(duty_cycle)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start  # pulse_end 초기화
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        print("채널 10 PWM 값: {:.4f}".format(pulse_duration)[2:])  # 소수점 이하 3자리부터 4자리까지 출력

        if 0.0011 >= pulse_duration >= 0.0090:
            set_servo_angle(10)
        elif 0.0019 >= pulse_duration >= 0.0017:
            set_servo_angle(170)
        else:
            set_servo_angle(90)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 주파수는 50Hz로 설정
pwm.start(7.5)  # 중립 위치

GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)

try:
    while True:
        time.sleep(0.1)  # 주기적으로 PWM 값을 확인하는 주기를 늦추었습니다.

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
