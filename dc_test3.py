import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RC_PIN = 27
DC_MOTOR_PIN = 22

GPIO.setup(RC_PIN, GPIO.IN)
GPIO.setup(DC_MOTOR_PIN, GPIO.OUT)

dc_motor_pwm = GPIO.PWM(DC_MOTOR_PIN, 50)
dc_motor_pwm.start(0)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        channel_pulse_start = time.time()
        GPIO.wait_for_edge(RC_PIN, GPIO.RISING)
        pulse_start = time.time()

        GPIO.wait_for_edge(RC_PIN, GPIO.FALLING)
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        pwm_value = round(pulse_duration * 1000000)

        if 1800 <= pwm_value <= 2100:
            speed = map_value(pwm_value, 1800, 2100, 0, 100)
            dc_motor_pwm.ChangeDutyCycle(speed)
            print(f"DC 모터 속도: {speed:.0f}%")
        else:
            dc_motor_pwm.ChangeDutyCycle(0)
            print("DC 모터 정지")

        time.sleep(0.1)

except KeyboardInterrupt:
    dc_motor_pwm.stop()
    GPIO.cleanup()
