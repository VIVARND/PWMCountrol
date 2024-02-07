import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
MOTOR_PIN = 27  # 내장형 DC 모터를 제어하기 위한 GPIO 핀
RC_PIN = 22   # 수신기의 PWM 신호를 받기 위한 GPIO 핀

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
GPIO.setup(RC_PIN, GPIO.IN)  # 수신기의 PWM 신호를 입력으로 설정

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
        
        # 현재 PWM 값과 상태 출력
        print(f"현재 PWM 값: {pwm_value:04d}")
        
        # 범위에 따라 DC 모터 상태 제어
        if 900 <= pwm_value <= 1200:
            print("DC 모터 ON")
            GPIO.output(MOTOR_PIN, GPIO.HIGH)  # 모터 ON
        else:
            print("DC 모터 OFF")
            GPIO.output(MOTOR_PIN, GPIO.LOW)   # 모터 OFF

        time.sleep(0.1)  # 갱신 주기에 따라 조절

except KeyboardInterrupt:
    GPIO.cleanup()
