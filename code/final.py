# Be the MONSTER! 20201127 Lee Chang-hyun

import pygame as pg
import random
import numpy as np
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1280
HEIGHT = 720
FPS = 60
check = 121

# score
out = 0
strike = 0
foul = 0
hit = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#hit point
hitpoint = 432

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Be the Monster_20201127이창현")
clock = pg.time.Clock()

# load all images-----------------------------------------------
ball_images = []
for i in range(1,4):
    filename = 'ball{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    ball_images.append(img)

bat_images = []
for i in range(1,4):
    filename = 'bat{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    bat_images.append(img)

font_name = pg.font.match_font('arial')

background = pg.image.load(path.join(img_dir, 'atbat.jpg'))
background = pg.transform.scale(background,(WIDTH,HEIGHT))
intro = pg.image.load(path.join(img_dir, 'intro.jpg'))
intro = pg.transform.scale(intro,(WIDTH,HEIGHT))
focus = pg.image.load(path.join(img_dir, 'focus.png'))
focus = pg.transform.scale(focus,(150,150))
# --------------------------------------------------------------

# load all sounds-----------------------------------------------
hit_s = pg.mixer.Sound(path.join(snd_dir, 'hit.mp3'))
pitch_s = pg.mixer.Sound(path.join(snd_dir, 'wind.mp3'))
foul_s = pg.mixer.Sound(path.join(snd_dir, 'foul.mp3'))
end_s = pg.mixer.Sound(path.join(snd_dir, 'end.mp3'))
pg.mixer.music.load(path.join(snd_dir, 'bgm.ogg'))
# --------------------------------------------------------------

def draw_text(surf, text, size, x, y, color=WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
#

def show_go_screen():
    global game_over, check, out, strike, foul, hit
    screen.fill(BLACK)
    screen.blit(intro,(0,0))
    # draw_text(screen, "Be the MONSTER!", 64, WIDTH / 2, HEIGHT / 4)
    # draw_text(screen, "Master all sports and be the Monster!", 22,
    #           WIDTH / 2, HEIGHT / 2)
    # draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                # 초기화
                game_over = True
                check = 121
                out = 0
                strike = 0
                foul = 0
                hit = 0
                waiting = False
#

class Ball(pg.sprite.Sprite):
    def __init__(self, all_balls):
        super().__init__(all_balls)

        # 랜덤한 이미지 설정
        self.original_image = random.choice(ball_images)

        # 초기 위치 설정
        self.rect = self.original_image.get_rect()
        self.rect.x = WIDTH /2
        self.rect.y = HEIGHT * 0.35

        # 이미지 크기 조정
        scaled_width = 5  # 조절하고자 하는 폭
        scaled_height = 5  # 조절하고자 하는 높이
        self.image = pg.transform.scale(self.original_image, (scaled_width, scaled_height))

        # 초기 속도 및 가속도 설정
        self.speed_x = 5
        self.speed_y = 0
        self.gravity = 0.5
        self.acc_x = -0.5

        self.update_score = update_score
        

    def update(self):
        # 속도와 가속도의 영향을 받아 이동
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # 가속도 적용
        self.speed_y += self.gravity
        self.speed_x += self.acc_x

        # 3D 효과를 위한 이미지 크기 조절
        distance = max(self.rect.y - HEIGHT * 0.35, 30)  # 최소 거리를 1로 설정

        self.image = pg.transform.scale(self.original_image, (distance / 4, distance / 4))

        # 오른쪽 파울
        if self.rect.x > WIDTH :
            self.kill()

        # 정타
        if self.rect.x < 500 and self.rect.y < 150:
            self.kill()

        # 왼쪽 파울
        if self.rect.x < 0 :
            self.kill()

        # 스트라이크
        if distance > 350:
            self.kill()
            self.update_score('strike')

        # Ball과 Bat 간의 충돌 감지
        hits = pg.sprite.spritecollide(self, all_bats, False)
        if hits:
            for bat in hits:
                ball_index = ball_images.index(self.original_image)
                bat_index = bat.image_index  # 변경된 부분: bat.image_index를 사용
                if ball_index == bat_index and not any(bat.collision_occurred for bat in all_bats):
                    # Ball의 x 좌표가 (WIDTH/2 - 100)에서 (WIDTH/2 + 100) 사이에 있는지 확인
                    if hitpoint - 30 < self.rect.y < hitpoint + 30:
                        # 충돌이면서 x 좌표가 조건에 맞다면 Hit
                        if not any(bat.collision_occurred for bat in all_bats):
                            self.update_score('hit')
                            hit_s.play()
                            self.speed_y = -20
                            self.speed_x = 10
                            for bat in all_bats:
                                bat.collision_occurred = True
                    else:
                        if not any(bat.collision_occurred for bat in all_bats):
                            # 충돌이지만 x 좌표가 조건에 맞지 않다면 Foul
                            if self.rect.y >= hitpoint + 30 and self.rect.y <= hitpoint + 45:
                                self.update_score('foul')
                                foul_s.play()
                                self.speed_y = -15
                                self.speed_x = 30
                            elif self.rect.y <= hitpoint - 30 and self.rect.y >= hitpoint - 45:
                                self.update_score('foul')
                                foul_s.play()
                                self.speed_y = -10
                                self.speed_x = -30
                                self.acc_x = -0.5
                            for bat in all_bats:
                                bat.collision_occurred = True
#

class Bat(pg.sprite.Sprite):
    def __init__(self, all_bats, bat_images, i, scaled_width, scaled_height, order):
        super().__init__(all_bats)

        # 이미지 크기 조정
        original_image = pg.transform.scale(bat_images[i], (scaled_width, scaled_height))
        self.original_image = original_image.copy()
        self.image = original_image
        self.check = 1

        self.scaled_width = scaled_width
        self.scaled_height = scaled_height
        self.i = i

        self.bot_x = WIDTH / 4
        self.bot_y = -100

        self.order = i
        self.image_index = i  # 이미지의 인덱스를 저장


        # 초기 위치 설정
        self.rect = self.image.get_rect()
        # self.rect.x = WIDTH / 2
        # self.rect.y = HEIGHT / 2

        # 회전 각도와 중심점 설정
        self.angle = 360
        self.original_angle = 360  # 초기 각도 저장
        self.rotation_center = (self.bot_x, self.bot_y)


        # Space 키가 눌려있었는지 여부를 저장하는 변수
        self.space_key_pressed = False

        self.collision_occurred = False  # 처음 충돌한 경우에만 True로 설정


    def update(self):
        # Space 키가 눌리면 배트 순서 변경
        keys = pg.key.get_pressed()
        if keys[pg.K_3] :
            # Space 키가 눌린 순간에만 실행
            if self.order == 1:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 2:
                self.check = 1
                self.rect.x = self.bot_x
                self.rect.y = self.bot_y
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 0:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가
        elif keys[pg.K_2] :
            # Space 키가 눌린 순간에만 실행
            if self.order == 0:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 1:
                self.check = 1
                self.rect.x = self.bot_x
                self.rect.y = self.bot_y
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 2:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가
        elif keys[pg.K_1] :
            # Space 키가 눌린 순간에만 실행
            if self.order == 1:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 0:
                self.check = 1
                self.rect.x = self.bot_x
                self.rect.y = self.bot_y
                self.collision_occurred = False  # 초기화 추가
            elif self.order == 2:
                self.check = 0
                self.rect.x = -5000
                self.rect.y = -5000
                self.collision_occurred = False  # 초기화 추가

        # Space 키의 상태 업데이트
        self.space_key_pressed = keys[pg.K_SPACE]

        # Enter 키가 눌리면 가장 아래에 있는 배트만 회전
        if keys[pg.K_RETURN] and self.check == 1:
            if self.angle < 480:
                self.angle += 35  # 회전 각도 증가
                rotated_image = pg.transform.rotate(self.original_image, self.angle)
                self.image = rotated_image
                self.rect = rotated_image.get_rect(center=self.rotation_center)
                self.rect.x += self.scaled_width/2
                self.rect.y += self.scaled_height/2 
        else:
            if self.check == 1 :
                # 키를 떼면 초기 각도로 돌아가도록 설정
                rotated_image = pg.transform.rotate(self.original_image, self.original_angle)
                self.image = rotated_image
                self.rect = rotated_image.get_rect(center=self.rotation_center)
                self.rect.x += self.scaled_width/2
                self.rect.y += self.scaled_height/2 
                self.angle = self.original_angle  # 초기 각도로 복원
            self.collision_occurred = False
#

def update_score(score_type):
    global out, strike, foul, hit
    if score_type == 'out':
        out += 1
        
    
    elif score_type == 'strike':
        if strike > 1:
            out+=1
            strike = 0
        else :
            strike += 1
    elif score_type == 'foul':
        foul += 1
        if strike < 2 :
            if strike > 1:
                out+=1
                strike = 0
            else :
                strike += 1
        elif strike ==2 :
            print()

    elif score_type == 'hit':
        hit += 1
#

# Ball 객체 생성
all_balls = pg.sprite.Group()
# Equipment 객체 생성
all_bats = pg.sprite.Group()

# Bat 객체를 미리 생성
bat0 = Bat(all_bats, bat_images, 0, 40, 800, 0)
bat1 = Bat(all_bats, bat_images, 1, 130, 800, 1)
bat2 = Bat(all_bats, bat_images, 2, 168, 800, 2)

pg.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True

while running:

    if out == 10 : 
        end_s.play()
        game_over = True
        
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

    

    # 2초 간격으로 새로운 Ball 객체 생성
    now = pg.time.get_ticks()
    if  check > 90 :
        new_ball = Ball(all_balls)
        check = 0
        pitch_s.play()

    # Ball 객체 업데이트
    for ball in all_balls:
        ball.update()

    # Bat 객체 업데이트a
    for bat in all_bats:
        bat.update()

    # 그리기
    screen.fill(BLACK)
    screen.blit(background,(0,0))
    all_balls.draw(screen)
    all_bats.draw(screen)

    screen.blit(focus,(640-75,hitpoint-75))

    # 전광판 출력 
    draw_text(screen, "Out    : ",30,150,25, RED)
    draw_text(screen, "Strike : ",30,150,65, YELLOW)
    draw_text(screen, "Foul   : " + str(foul),30,150,105, WHITE)
    draw_text(screen, "Hit     : " + str(hit),30,150,145, GREEN)
    
    for i in range(out) :
        pg.draw.circle(screen,RED,(200+i*25-125*(int(i/5)),25*(int(i/5)+1)+4),10)
    for i in range(strike) : 
        pg.draw.circle(screen,YELLOW,(200+i*50,85),15)

    check += 1

    # *after* drawing everything, flip the display
    pg.display.flip()
    
pg.quit()
