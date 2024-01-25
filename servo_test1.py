import time
import pigpio

pwm_pin = 18  # PWM 신호를 읽을 GPIO 핀 (라즈베리파이 3B/3B+/4B의 경우 GPIO18)
servo_pin = 24  # 서보모터의 신호선이 연결된 GPIO 핀

pi = pigpio.pi()

# 서보 모터로 사용할 GPIO 핀 설정
pi.set_servo_pulsewidth(servo_pin, 0)
time.sleep(1)  # 초기화를 위해 충분한 대기 시간

def set_servo_angle(angle):
    current_angle = get_current_servo_angle()
    target_angle = angle
    step = 1 if target_angle > current_angle else -1
    
    for a in range(int(current_angle), int(target_angle), step):
        pulse_width = (a / 180.0) * (2.5 - 0.5) + 0.5
        duty_cycle = pulse_width * 100 / 20
        pi.set_servo_pulsewidth(servo_pin, int(duty_cycle * 1000))  # 마이크로초 단위로 변환
        time.sleep(0.01)  # 부드러운 이동을 위한 대기 시간

def pwm_callback(channel, level, tick):
    pulse_duration = (tick / 1000000.0)  # 마이크로초를 초로 변환
    if pulse_duration != 0.0:
        print("채널 10 PWM 값: {:.4f}".format(pulse_duration)[2:])  # 소수점 이하 3자리부터 4자리까지 출력

        if 0.0011 >= pulse_duration >= 0.0090:
            set_servo_angle(10)
        elif 0.0019 >= pulse_duration >= 0.0017:
            set_servo_angle(170)
        else:
            set_servo_angle(90)

        current_angle = get_current_servo_angle()
        print("현재 서보모터 각도: {:.2f}도".format(current_angle))

def get_current_servo_angle():
    duty_cycle = pi.get_servo_pulsewidth(servo_pin) / 1000.0  # 밀리초를 초로 변환
    pulse_width = (duty_cycle / 20.0) + 0.5
    angle = pulse_width * 180.0
    return angle

pi.set_mode(pwm_pin, pigpio.INPUT)
pi.set_mode(servo_pin, pigpio.OUTPUT)

cb = pi.callback(pwm_pin, pigpio.EITHER_EDGE, pwm_callback)

try:
    while True:
        time.sleep(0.1)  # 주기적으로 PWM 값을 확인하는 주기를 늦추었습니다.

except KeyboardInterrupt:
    pass

finally:
    cb.cancel()
    pi.set_servo_pulsewidth(servo_pin, 0)  # 서보 모터의 PWM 신호를 중단합니다.
    pi.stop()
    print("GPIO 정리 완료. 프로그램 종료.")
