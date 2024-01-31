import time
import RPi.GPIO as GPIO

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀
servo_pin = 24  # 서보 모터를 제어할 GPIO 핀

debounce_delay = 0.02  # 디바운싱을 위한 딜레이 설정

def set_servo_angle(angle):
    pwm_value = angle / 180.0 * (2000 - 900) + 900
    pwm.ChangeDutyCycle(pwm_value / 20.0)  # PWM 신호 변경
    print(f"현재 서보모터 각도: {angle}도, PWM 값: {round(pwm_value)}")

def pwm_callback(channel):
    time.sleep(debounce_delay)  # 디바운싱을 위한 딜레이 추가
    pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(channel) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    if pulse_duration != 0.0:
        pwm_value = round(pulse_duration * 1000000)  # PWM 값 변환 (마이크로초로 변환)
        if 900 <= pwm_value <= 1200:
            set_servo_angle(10)
        elif 1300 <= pwm_value <= 1500:
            set_servo_angle(50)
        elif 1800 <= pwm_value <= 2000:
            set_servo_angle(90)
        else:
            print("다른 신호가 들어왔습니다. 서보 모터 동작을 잠시 멈춥니다.")
            time.sleep(1)  # 1초 동안 동작을 멈춥니다.

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
