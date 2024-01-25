import time
import pigpio

servo_pin = 24  # 서보모터의 신호선이 연결된 GPIO 핀
rc_channel = 18  # RC 조종기의 채널에 연결된 GPIO 핀

pi = pigpio.pi()

# 서보 모터로 사용할 GPIO 핀 설정
pi.set_servo_pulsewidth(servo_pin, 0)
time.sleep(1)  # 초기화를 위해 충분한 대기 시간

def set_servo_angle(angle):
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    pulse_width = (angle / 180.0) * (2500 - 500) + 500
    pi.set_servo_pulsewidth(servo_pin, int(pulse_width))
    time.sleep(0.01)  # 부드러운 이동을 위한 대기 시간

def rc_callback(channel, level, tick):
    pulse_duration = (tick / 1000000.0)  # 마이크로초를 초로 변환
    print("채널 {} PWM 값: {:.4f}".format(rc_channel, pulse_duration))  # 소수점 이하 4자리까지 출력

    if 0.0009 >= pulse_duration >= 0.0007:
        set_servo_angle(10)
    elif 0.0011 >= pulse_duration > 0.0009:
        set_servo_angle(170)
    else:
        set_servo_angle(90)

    current_angle = get_current_servo_angle()
    print("현재 서보모터 각도: {:.2f}도".format(current_angle))

def get_current_servo_angle():
    pulse_width = pi.get_servo_pulsewidth(servo_pin)
    angle = (pulse_width - 500) / (2500 - 500) * 180.0
    return angle

pi.set_mode(rc_channel, pigpio.INPUT)
pi.set_mode(servo_pin, pigpio.OUTPUT)

cb = pi.callback(rc_channel, pigpio.EITHER_EDGE, rc_callback)

try:
    while True:
        time.sleep(0.1)  # 주기적으로 RC PWM 값을 확인하는 주기를 늦추었습니다.

except KeyboardInterrupt:
    pass

finally:
    cb.cancel()
    pi.set_servo_pulsewidth(servo_pin, 0)  # 서보 모터의 PWM 신호를 중단합니다.
    pi.stop()
    print("GPIO 정리 완료. 프로그램 종료.")
