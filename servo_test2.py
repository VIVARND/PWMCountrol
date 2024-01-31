import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀

def set_servo_angle(angle):
    pwm_value = angle / 180.0 * (2000 - 900) + 900
    pwm.ChangeDutyCycle(pwm_value / 20.0)  # PWM 신호 변경
    print(f"서보모터 각도: {angle}도, PWM 값: {round(pwm_value)}")

def move_servo(start_angle, end_angle, step, delay):
    direction = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle, direction * step):
        set_servo_angle(angle)
        time.sleep(delay)

def pwm_callback(channel):
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
        print("현재 PWM 값:", pwm_value)  # PWM 값 출력
        if 1800 <= pwm_value <= 2000:
            move_servo(180, 10, 10, 0.1)  # 180도에서 10도로 이동
        else:
            move_servo(10, 180, 10, 0.1)  # 10도에서 180도로 이동

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.IN)  # PWM 핀을 입력으로 설정
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 서보 모터 PWM 설정
pwm.start(0)

try:
    GPIO.add_event_detect(pwm_pin, GPIO.BOTH, callback=pwm_callback)
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 정리 완료. 프로그램 종료.")
