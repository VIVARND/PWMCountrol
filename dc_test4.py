import RPi.GPIO as GPIO
import time

# GPIO 설정 경고 비활성화
GPIO.setwarnings(False)

# GPIO 핀 설정
RC_PIN = 19  # 수신기의 신호선에 연결
DC_MOTOR_PIN = 13  # DC 모터의 신호선에 연결

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RC_PIN, GPIO.IN)  # 입력 모드로 설정
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)  # 출력 모드로 설정

# DC 모터 제어 함수
def control_dc_motor(pwm_value):
    if 1800 <= pwm_value <= 2100:
        dc_motor_pwm.ChangeDutyCycle(5)  # PWM의 duty cycle은 0~100 범위
        return True
    else:
        dc_motor_pwm.ChangeDutyCycle(0)  # 모터를 끔
        return False

# PWM 객체 생성
dc_motor_pwm = GPIO.PWM(DC_MOTOR_PIN, 100)  # PWM 주파수 100Hz
dc_motor_pwm.start(0)

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

        # DC 모터 제어
        motor_on = control_dc_motor(pwm_value)

        # 모터 상태 출력
        if motor_on:
            print("DC 모터: ON")
        else:
            print("DC 모터: OFF")

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    dc_motor_pwm.stop()
    GPIO.cleanup()
