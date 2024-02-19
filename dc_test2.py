import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# PWM 입력 신호를 받을 GPIO 핀 설정 (라즈베리 파이에 연결된 GPIO 핀 번호로 수정)
RC_PIN = 27
# DC 모터 제어 핀 설정 (라즈베리 파이에 연결된 GPIO 핀 번호로 수정)
DC_MOTOR_PIN = 22

# GPIO 핀을 입력 모드로 설정
GPIO.setup(RC_PIN, GPIO.IN)

# DC 모터를 작동시키기 위한 PWM 범위 설정
PWM_MIN = 1000
PWM_MAX = 2100



# GPIO 핀을 출력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

# PWM 객체 생성
dc_motor_pwm = GPIO.PWM(DC_MOTOR_PIN, 50)  # PWM 주파수 50Hz
dc_motor_pwm.start(0)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        # PWM 값 읽어오기
        channel_pulse_start = time.time()
        GPIO.wait_for_edge(RC_PIN, GPIO.RISING)
        pulse_start = time.time()

        GPIO.wait_for_edge(RC_PIN, GPIO.FALLING)
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        pwm_value = round(pulse_duration * 1000000)

        # PWM 값 출력
        print(f"현재 PWM 값: {pwm_value:04d}")

        # PWM 값이 일정 범위 내에 있는지 확인
        if PWM_MIN <= pwm_value <= PWM_MAX:
            # PWM 값을 모터 속도로 변환 (여기에서는 예시로 직접 매핑)
            speed = map_value(pwm_value, PWM_MIN, PWM_MAX, 0, 100)
            dc_motor_pwm.ChangeDutyCycle(speed)
            print(f"DC 모터 속도: {speed}%")
        else:
            # PWM 값이 범위를 벗어나면 모터 정지
            dc_motor_pwm.ChangeDutyCycle(0)
            print("DC 모터 정지")

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    # GPIO 정리
    dc_motor_pwm.stop()
    GPIO.cleanup()
