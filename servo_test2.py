import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
ppm_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(ppm_pin, GPIO.IN)

# PPM 신호를 읽기 위한 변수 초기화
ppm_start_time = 0
ppm_last_time = 0
ppm_widths = []

def ppm_callback(channel):
    global ppm_start_time, ppm_last_time, ppm_widths
    pulse_width = time.time() - ppm_last_time
    ppm_last_time = time.time()

    if pulse_width > 0.0002:  # PPM 신호에서의 긴 펄스를 감지
        ppm_start_time = ppm_last_time
        ppm_widths = []

    ppm_widths.append(pulse_width)

# GPIO 핀에 콜백 함수 연결
GPIO.add_event_detect(ppm_pin, GPIO.BOTH, callback=ppm_callback)

try:
    while True:
        if ppm_widths:
            # PPM 신호에서의 각 채널의 펄스 폭 출력 (2자리 수로 변환)
            ppm_widths_in_ms = [int(width * 1000) for width in ppm_widths]
            print("PPM Channel Widths:", ppm_widths_in_ms)
            ppm_widths = []  # PPM 신호를 읽고 나면 리스트 초기화

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    GPIO.cleanup()
