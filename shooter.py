from pygame import *
from random import *
from time import time as timer
w = 1200
h = 800
class GameSprite(sprite.Sprite):
    def __init__(self,x,y,weight,height,player_speed,player_image):
        super().__init__()
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (weight,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def move(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 550:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 700:
            self.rect.y += self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 995:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 105:
            self.rect.x -= self.speed
    
    def fire(self):
        bullet = Bullet(self.rect.centerx,self.rect.top,10,15,15,'bullet1.png')
        bullets.add(bullet)
font.init()
font = font.Font(None,50)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 800:
            self.rect.y = 0
            random_x = randint(150,950)
            self.rect.x = random_x
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.rect.y = 0
            random_x = randint(100,1000)
            self.rect.x = random_x

win_text = font.render('YOU WIN!', True, (255,255,255))
lose_text = font.render('YOU LOSE!', True, (255,255,255))
reload_text = font.render('WAIT,RELOAD', True, (255,255,255))
finish = False
clock = time.Clock()
window = display.set_mode((w,h))
display.set_caption('Космо-Шутер')
background = transform.scale(image.load('background2.png'), (w,h))
mixer.init()
mixer.music.load('game_sounds.ogg')
mixer.music.play()
shoot = mixer.Sound('game_sounds_shooting_shoot2.mp3')
lose = mixer.Sound('game_sounds_gameover.mp3')
win = mixer.Sound('game_sounds_win.mp3')
game = True
health = 3
num_fire = 0
rel_time = False 
player = Player(550,650,100,100,5,'player.png')
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy(randint(150,950), -50, 100, 100,randint(1,3), 'enemy1_2.png')
    monsters.add(monster)
for k in range(3):
    asteroid = Asteroid(randint(100,1000), -50, 80,80,randint(1,4), 'meteor_2.png')
    asteroids.add(asteroid)
score = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    shoot.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 10 and rel_time == False:
                    rel_time = True
                    start = timer()


    if finish != True:
        
        window.blit(background, (0,0))
        text1 = font.render('Пропущено:'+ str(lost), 1, (139, 0, 139))
        text2 = font.render('Счёт:' + str(score), 1, (139,0,139))
        window.blit(text1, (50,50))
        window.blit(text2, (50,10))
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        if sprite.spritecollide(player,monsters, True) or sprite.spritecollide(player,asteroids, True):
            health -= 1
        for h in sprites_list:
            score += 1
            monster = Enemy(randint(150,950), -50, 100, 100,1, 'enemy1_2.png')
            monsters.add(monster)
        if rel_time == True:
            end = timer()
            if end - start < 3:
                window.blit(reload_text,(470,600)) 
            else:
                num_fire = 0
                rel_time = False
        player.reset()
        player.move()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        if score >= 10:
            window.blit(win_text, (500,400))
            win.play()
            mixer.music.set_volume(0)
            finish = True
        elif lost >= 5 or health == 0:
            window.blit(lose_text, (500,400))
            lose.play()
            mixer.music.set_volume(0)
            finish = True
        if health == 3:
            health_color = (0,255,9)
        if health == 2:
            health_color = (255,255,0)
        if health == 1:
            health_color = (255,0,0)
        if health == 0:
            health_color = (0,0,0)
        text3 = font.render(str(health), 1, health_color)
        window.blit(text3, (1100, 50))
        clock.tick(90)
        display.update()
