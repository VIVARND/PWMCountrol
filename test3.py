import pygame
import pigpio

# RC 조종기 핀 설정
rc_pin = 14  # RC 조종기 신호 핀 번호

# GPIO 설정
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio. Make sure pigpiod is running.")
    exit()

# pygame 초기화
pygame.init()

# 화면 크기 및 설정
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PWM Signal Visualization")

# 시계열 데이터를 저장할 리스트
data = []

try:
    print("Reading and plotting PWM signals from RC controller...")

    while True:
        # PWM 값 읽기
        pulse_width = pi.get_servo_pulsewidth(rc_pin)

        if pulse_width > 0:
            # 리스트에 값을 추가
            data.append(pulse_width)

            # 화면 갱신
            screen.fill((255, 255, 255))  # 배경을 흰색으로 설정

            # 선 그리기
            pygame.draw.lines(screen, (0, 0, 255), False, [(i, height - value) for i, value in enumerate(data)], 2)

            # 화면 업데이트
            pygame.display.flip()

        # 이벤트 처리 (종료 버튼 클릭 시 종료)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        pygame.time.Clock().tick(30)  # 초당 30 프레임 제한

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 리소스 해제 및 pygame 종료
    pi.stop()
    pygame.quit()
    print("Program terminated.")
