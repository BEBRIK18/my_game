from random import *
from time import time as t

from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, length, higth):
        super().__init__()
        self.player_image = player_image
        self.image = transform.scale(image.load(player_image), (length, higth))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 450:
            self.rect.y += self.speed

class Shrak(GameSprite):
    def update(self):
        self.rect.x -= self.speed

    def throwing_shrek(self):
        if self.rect.x <= 0:
            self.rect.x = 650
            self.rect.y = randint(50, 450)
            self.speed = randint(2, 5)
    def throwing_shrek_from_scala(self):
        self.rect.x = 650
        self.rect.y = randint(50, 450)
        self.speed = randint(2, 5)

class Shield(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            self.rect.x = 1500
            self.rect.y = randint(30, 470)
            self.speed = randint(2, 4)



window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('shrak_home.jpg'), (700, 500))


shraks = sprite.Group()

player = Player('scala.png', 30, 220, 4, 50, 50)

shrak1 = Shrak('shrak.png', 650, 70, 1, 80, 80)
shrak2 = Shrak('shrak.png', 650, 170, 2, 75, 75)
shrak3 = Shrak('shrak.png', 650, 250, 3, 70, 70)
shrak4 = Shrak('shrak.png', 650, 360, 4, 65, 65)
shrak5 = Shrak('shrak.png', 650, 450, 5, 60, 60)

shield = Shield('shield.png', 700, 300, 2, 50, 50)

shraks.add(shrak1)
shraks.add(shrak2)
shraks.add(shrak3)
shraks.add(shrak4)
shraks.add(shrak5)

font.init()
font = font.Font(None, 30)

mixer.init()
mixer.music.load('shrak_song.mp3')
dead_zvuk = mixer.Sound('shrek_roar.ogg')
mixer.music.play(-1)

FPS = 60
clock = time.Clock()
game = True
finish = False
protection = False

while game:
    key_pressed = key.get_pressed()

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        shraks.draw(window)
        shraks.update()
        for sprite_object in shraks:
            sprite_object.throwing_shrek()
        shield.update()


    grc = sprite.spritecollide(player, shraks, False)
    grc2 = sprite.collide_rect(player, shield)

    if grc2 :
        protection = True
        
    if grc and protection == True:
        for sprite_object in shraks:
            grc3 = sprite.collide_rect(player, sprite_object)
            if grc3:
                print(1)
                print(protection)
                sprite_object.throwing_shrek_from_scala()
                grc = False
        protection = False
        

    if grc and protection != True:
        print(protection)
        finish = True
        lose = font.render('шрек тебя съел', True, (255, 0, 0))
        window.blit(lose, (300, 200))
        mixer.music.stop()
        dead_zvuk.play()

    for e in event.get():
        if e.type == QUIT:
            game = False

    player.reset()
    shield.reset()
    clock.tick(FPS)

    display.update()