# sprites.py
import pygame as pg
from config import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, start_pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        self.vel = pg.math.Vector2(0, 0)
        self.rect.topleft = start_pos
        
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vel.y = PLAYER_JUMP
            self.on_ground = False 

    def update(self):
        self.vel.y += GRAVITY
        if self.vel.y > 10: 
            self.vel.y = 10
            
        self.vel.x = 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_VEL
        if keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_VEL
            
        self.rect.x += self.vel.x
        self.collide_with_platforms('horizontal')
        
        self.on_ground = False
        self.rect.y += self.vel.y
        self.collide_with_platforms('vertical')

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def collide_with_platforms(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            if direction == 'horizontal':
                if self.vel.x > 0:
                    self.rect.right = hits[0].rect.left
                if self.vel.x < 0:
                    self.rect.left = hits[0].rect.right
                self.vel.x = 0
                    
            if direction == 'vertical':
                if self.vel.y > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.on_ground = True
                if self.vel.y < 0:
                    self.rect.top = hits[0].rect.bottom
                self.vel.y = 0

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Goal(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)