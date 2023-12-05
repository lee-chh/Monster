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

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Be the Monster_20201127이창현")
clock = pg.time.Clock()

ball_images = []
for i in range(1,10):
    filename = 'ball{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert()
    
    ball_images.append(img)

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.frame = 0
        self.image = explosion_anim[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # self.frame = (self.frame+1) % self.
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

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
    def __init__(self):

        # 랜덤한 이미지 설정
        self.image = random.choice(ball_images)
        self.rect = self.image.get_rect()

        # 초기 위치 설정
        self.rect.center = (random.randint(50, WIDTH - 50), 50)

        # 초기 속도 및 가속도 설정
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.uniform(-5, 5)
        self.gravity = 0.5

        # 1초 간격으로 생성을 위한 타이머 설정
        self.appearance_timer = pg.time.get_ticks()
        self.appearance_interval = 1000  # 1 second


    def update(self):
        now = pg.time.get_ticks()
        if now - self.appearance_timer > self.appearance_interval:
            self.appearance_timer = now
            new_ball = Ball(self.all_balls, self.all_equipment)
            new_ball.speed_x = random.choice([-5, 5])
            new_ball.speed_y = random.uniform(-5, 5)
            new_ball.rect.center = (random.randint(50, WIDTH-50), 50)
            self.all_balls.add(new_ball)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += self.gravity

        if self.rect.bottom > HEIGHT:
            self.kill()

class Circle(pg.sprite.Sprite): 
    def __init__(self, all_circles):
        super().__init__(all_circles)

        # 초기 위치 설정
        self.rect = pg.Rect(1000,200, 20, 20)
        self.rect.center = (1000,200)

        # 초기 속도 및 가속도 설정
        self.speed_x = 20
        self.speed_y = 0
        self.gravity = 0.5

        # 랜덤한 이미지 설정
        original_image = random.choice(ball_images)
        
        # 이미지 크기 조정
        scaled_width = 20  # 조절하고자 하는 폭
        scaled_height = 20  # 조절하고자 하는 높이
        self.image = pg.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()

    def update(self):
        # 속도와 가속도의 영향을 받아 이동
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 가속도 적용
        self.speed_y += self.gravity

        # 특정 조건에 도달하면 제거
        if self.rect.y > HEIGHT:
            print("Circle removed!")
            self.kill() 

# 스페이스바를 눌렀을 때의 플래그
space_pressed = False

# Game loop
game_over = True
running = True

# Circle 객체 생성
all_circles = pg.sprite.Group()

# Ball 그룹을 생성
all_balls = pg.sprite.Group()

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

    # 스페이스바를 누르면 새로운 Circle 객체 생성
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        print("Creating a new circle!")
        Circle(all_circles)
    # Circle 객체 업데이트
    all_circles.update()

    # 그리기
    screen.fill(BLACK)
    all_circles.draw(screen)

    # # Ball 객체 업데이트
    # all_balls.update()

    # # 그리기
    # screen.fill(BLACK)
    # all_balls.draw(screen)

    draw_text(screen, "run", 18, WIDTH / 2, HEIGHT / 2)

    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()