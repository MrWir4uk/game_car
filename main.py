from random import choice, randint
from typing import Any
from pygame import *
import sys

init()
font.init()
font1 = font.SysFont("Kristen ITC", 100)
font2 = font.SysFont("Impact", 50)
game_over_text = font1.render("GAME OVER", True, (150, 0, 0))
mixer.init()
mixer.music.load('sound.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)

enemy_speed = 4 

line1 = 350
line2 = 550
line3 = 770
line4 = 970

lines_cords = [350,550,770,970]

screen_info = display.Info() 
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

window = display.set_mode((WIDTH,HEIGHT),flags=FULLSCREEN)
FPS = 90
clock = time.Clock()


bg = image.load('background.png')
bg = transform.scale(bg,(WIDTH,HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT


player_img = image.load("car.png")
enemy_img = image.load("car_enemy.png")
all_sprites = sprite.Group()


class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Enemy(Sprite):
    def __init__(self, sprite_img, width, height):
        rand_x = lines_cords[randint(0,3)]
        super().__init__(sprite_img, width, height, rand_x, -200)
        self.damage = 100
        self.speed = enemy_speed
     


    def update(self):
        self.rect.y += player.bg_speed + self.speed
        if self.rect.y > HEIGHT:
            self.kill()



class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.score = 0
        self.speed = 2
        self.bg_speed = 5
        self.max_speed = 20
        self.car_line = 0
        self.rect.x = lines_cords[2]

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w] and self.rect.y > 200:
            self.rect.y -= self.speed
            self.bg_speed += 0.1
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            if self.bg_speed > 2:
                self.bg_speed -= 0.2

        if key_pressed[K_a] and self.rect.x > 0:
            if self.car_line > 0:
                self.car_line -= 1
            self.rect.x = lines_cords[self.car_line] 
        if key_pressed[K_d] and self.rect.right < WIDTH:
            if self.car_line < 3:
                self.car_line += 1
            self.rect.x = lines_cords[self.car_line] 
            


player = Player(player_img, 100,150,970,600)
enemy = Enemy(enemy_img,100,150)


start_time = time.get_ticks()
timer = start_time
enemy_spawn_time = time.get_ticks()
spawn_interval = randint(500, 3000)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            # if start_screen:
            #     start_screen = False
            if e.key == K_ESCAPE:
                run = False
                sys.exit()

        
    window.blit(bg,(0,bg_y1))
    window.blit(bg,(0,bg_y2))

    if finish != True:
        bg_y1+=player.bg_speed
        bg_y2+=player.bg_speed
        
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT

        if player.hp <= 0:
            finish = True
        
        now = time.get_ticks() #поточний час
        if now - enemy_spawn_time > spawn_interval: #Якщо від появи останнього ворога пройшло <1 секундни
            enemy1 = Enemy(enemy_img, 100,150)#створюємо нового ворога

            enemy_spawn_time = time.get_ticks() #оновлюємо час появи ворога
            spawn_interval = randint(500, 1500) 
        if  now - timer > 5000:
            enemy_speed += 30
            timer = time.get_ticks()
        
        
    
            

            # ollide_list = sprite.spritecollide(player, enemys, True, sprite.collide_mask)
            # if len(collide_list) > 0:
            #     finish = True



        all_sprites.draw(window)
        # window.blit(score_text,(30,30))
        if not finish:
            all_sprites.update()
        # if finish:
        #     window.blit(game_over_text, (300,500))
        #     window.blit(restart_text, (500,600))
    #game_over_text,WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2

    display.update()
    clock.tick(FPS)
