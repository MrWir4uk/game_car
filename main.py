from random import choice, randint
from typing import Any
from pygame import *
import sys

init()
font.init()
font1 = font.SysFont("Kristen ITC", 100)
font2 = font.SysFont("Impact", 50)
game_over_text = font1.render("GAME OVER", True, (150, 0, 0))
restart_text = font2.render('PRESS R TO RESTART ', True, (150,0,0))
start_text = font2.render('PRESS ANY KEY TO START  ', True, (150,0,0))



mixer.init()
mixer.music.load('sound.ogg')
#mixer.music.play()
mixer.music.set_volume(0.9)

enemy_speed = 4 




screen_info = display.Info() 
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
#WIDTH, HEIGHT = 1367,768

window = display.set_mode((WIDTH,HEIGHT),flags=FULLSCREEN)
#window = display.set_mode((WIDTH,HEIGHT))
FPS = 90
clock = time.Clock()


bg = image.load('background.png')
bg = transform.scale(bg,(WIDTH,HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

line1 = 350 * WIDTH / 1367
line2 = 550* WIDTH / 1367
line3 = 770* WIDTH / 1367
line4 = 970* WIDTH / 1367

lines_cords = [line1,line2,line3,line4]

player_img = image.load("car.png")
enemy_img = image.load("car_enemy.png")
coin_img = image.load("coin.png")
all_coins = sprite.Group()
all_sprites = sprite.Group()
all_enemy = sprite.Group()



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
        all_enemy.add(self)
      

    def update(self):
        self.rect.y += player.bg_speed + self.speed
        if self.rect.y > HEIGHT:
            self.kill()
                

class Coin(Sprite):
    def __init__(self, sprite_img, width, height):
        rand_x = lines_cords[randint(0,3)]
        super().__init__(sprite_img, width, height, rand_x, -200)
  
        self.speed = enemy_speed
        all_coins.add(self)
      

    def update(self):
        self.rect.y += player.bg_speed
        if self.rect.y > HEIGHT:
            self.kill()
       


class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.score = 0
        self.speed = 2
        self.speed_x = 10
        self.bg_speed = 5
        self.max_speed = 20
        self.car_line = 2
        self.rect.x = lines_cords[self.car_line]
        self.original = self.image
        self.angle = 0

    def update(self):
        global score_text
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
            if self.rect.x > lines_cords[self.car_line]:
                self.rect.x -= self.speed_x
                if self.rect.x < lines_cords[self.car_line] + 100:
                    if self.angle < 30:
                        self.angle += 5
            
            
            # self.rect.x = lines_cords[self.car_line] 
        elif key_pressed[K_d] and self.rect.right < WIDTH:
            if self.car_line < 3:
                self.car_line += 1
            if self.rect.x < lines_cords[self.car_line]:
                self.rect.x += self.speed_x
                if self.angle > -30:
                     self.angle -= 5
        else:
            self.angle = 0
            
        self.image = transform.rotate(self.original, self.angle)

        enemy_collide = sprite.spritecollide(self, all_enemy, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100



        coin_collide = sprite.spritecollide(self, all_coins, True, sprite.collide_mask)
        if len(coin_collide) > 0:
            self.score += 5
            score_text = font2.render(f"Score:{self.score}", True, (255, 255, 255))


            


player = Player(player_img, 100,150,lines_cords[1],600)
enemy = Enemy(enemy_img,100,150)

score_text = font2.render(f"Score:{player.score}", True, (255, 255, 255))

start_time = time.get_ticks()
timer = start_time
enemy_spawn_time = time.get_ticks()
coin_spawn_time = time.get_ticks()
spawn_interval = randint(500, 1500)
spawn_interval_coin = randint(500, 1500)
start = False
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if not start:
                start = True
            if e.key == K_ESCAPE:
                run = False
                sys.exit()
            
            if finish and e.key == K_r:
                finish = False
                for s in all_sprites:
                    s.kill()
                player = Player(player_img, 100, 150, 300, 300)




        
    window.blit(bg,(0,bg_y1))
    window.blit(bg,(0,bg_y2))

    if finish != True and start:
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
            spawn_interval = randint(500, 2500) 
            

        if  now - timer > 15000:
            enemy_speed += 1.5
            timer = time.get_ticks()
        
        if now - coin_spawn_time > spawn_interval_coin:
            coin = Coin(coin_img,100,100)
            coin_spawn_time = time.get_ticks()
            spawn_interval_coin = randint(500, 2500) 






        all_sprites.draw(window)
        window.blit(score_text,(30,30))
        if not finish:
            all_sprites.update()
    if not start:
        window.blit(start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2 - start_text.get_height()/2 + 200))

    if finish:
        window.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 - restart_text.get_height()/2 + 200))
        window.blit(game_over_text,(WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))

    display.update()
    clock.tick(FPS)
