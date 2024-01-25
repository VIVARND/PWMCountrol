import RPi.GPIO as GPIO
import serial
import struct
import time

# GPIO 핀 설정
pwm_pin = 18  # PWM 입력 핀
servo_pin = 24  # 서보 모터 신호 핀

# 서보 모터 각도에 따른 PWM 신호 범위
angle_to_pwm_range = {
    10: (0.0009, 0.0011),  # 수정된 부분
    170: (0.0017, 0.0019),
}

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # GPIO 경고 비활성화
GPIO.setup(pwm_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM 객체 생성
pwm = GPIO.PWM(pwm_pin, 50)  # 50Hz 주파수 설정

# 서보 모터를 특정 각도로 회전하는 함수
def set_servo_angle(angle):
    pwm_range = angle_to_pwm_range.get(angle, (0.0009, 0.0011))  # 수정된 부분
    pwm_value = sum(pwm_range) / 2  # PWM 값의 중간값 사용
    pwm.ChangeDutyCycle(pwm_value)
    print(f"서보 모터 각도: {angle}도, PWM 값: {pwm_value}")

# PWM 신호 읽기
def read_pwm(serial_port):
    while True:
        data = serial_port.read(2)
        if len(data) == 2:
            channel, pwm_value = struct.unpack('<BB', data)
            pwm_value_normalized = pwm_value / 255.0  # PWM 값을 0.0에서 1.0으로 정규화

            if 0.0009 <= pwm_value_normalized <= 0.0011:  # 수정된 부분
                set_servo_angle(10)
            elif 0.0019 >= pwm_value_normalized > 0.0017:
                set_servo_angle(170)
            else:
                set_servo_angle(90)

            print(f"채널 {channel} PWM 값: {pwm_value_normalized}")
            # 여기에 필요한 로직 추가

if __name__ == "__main__":
    port = "/dev/ttyUSB0"  # 실제 사용하는 환경에 맞게 설정
    baud_rate = 9600

    try:
        ser = serial.Serial(port, baud_rate, timeout=0.1)
        print(f"시리얼 포트 {port}에 연결되었습니다.")
        time.sleep(1)  # 초기화를 위해 충분한 대기 시간

        # PWM 시작
        pwm.start()

        # PWM 읽기 시작
        read_pwm(ser)
    except serial.SerialException as e:
        print(f"시리얼 포트 연결 중 오류가 발생했습니다: {e}")
    finally:
        # 정리 작업
        pwm.stop()
        GPIO.cleanup()
        ser.close()
        print("시리얼 포트가 닫혔습니다.")
