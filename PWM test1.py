import time
import pigpio

ppm_pin = 18  # PPM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)

def ppm_callback(gpio, level, tick):
    print("PPM 신호 감지:", level, "Tick:", tick)

pi = pigpio.pi()

if not pi.connected:
    print("GPIO 초기화 실패. 프로그램을 종료합니다.")
    exit()

# PPM 신호를 읽기 위한 GPIO 핀 설정
pi.set_mode(ppm_pin, pigpio.INPUT)
pi.set_pull_up_down(ppm_pin, pigpio.PUD_UP)

# PPM 신호 변화 감지 콜백 설정
pi.callback(ppm_pin, pigpio.EITHER_EDGE, ppm_callback)

try:
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    pi.stop()
    print("GPIO 정리 완료. 프로그램 종료.")
