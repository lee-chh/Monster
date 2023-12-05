# 20201127 Lee Chang-hyun

import pygame as pg
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1280
HEIGHT = 720
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Be the Monster_20201127이창현")
clock = pg.time.Clock()

ball_images = []
for i in range(1, 10):
    filename = 'ball{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    ball_images.append(img)

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "Be the MONSTER!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Master all sports and be the Monster!", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


class Ball(pg.sprite.Sprite):
    def __init__(self, all_balls):
        super().__init__(all_balls)

        # 랜덤한 이미지 설정
        original_image = random.choice(ball_images)

        # 초기 위치 설정
        self.rect = original_image.get_rect()
        self.rect.x = WIDTH * 4 / 5
        self.rect.y = HEIGHT * 1 / 5

        # 이미지 크기 조정
        scaled_width = 40  # 조절하고자 하는 폭
        scaled_height = 40  # 조절하고자 하는 높이
        self.image = pg.transform.scale(original_image, (scaled_width, scaled_height))

        # 초기 속도 및 가속도 설정
        self.speed_x = -3
        self.speed_y = 0
        self.gravity = 0.5
        self.x_acc = -1

        # 1초 간격으로 생성을 위한 타이머 설정
        self.appearance_timer = pg.time.get_ticks()
        self.appearance_interval = 1000  # 1 second

    def update(self):
        # 속도와 가속도의 영향을 받아 이동
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 가속도 적용
        self.speed_y += self.gravity
        self.speed_x += self.x_acc

        if self.rect.y > HEIGHT:
            self.kill()


# 스페이스바를 눌렀을 때의 플래그
space_pressed = False

# Ball 객체 생성
all_balls = pg.sprite.Group()

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False

    # 1초 간격으로 새로운 Ball 객체 생성
    now = pg.time.get_ticks()
    if all_balls and now - all_balls.sprites()[-1].appearance_timer > all_balls.sprites()[-1].appearance_interval:
        Ball(all_balls)
    elif not all_balls:
        Ball(all_balls)

    # Ball 객체 업데이트
    all_balls.update()

    # 그리기
    screen.fill(BLACK)
    all_balls.draw(screen)

    draw_text(screen, "run", 18, WIDTH / 2, HEIGHT / 2)

    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
