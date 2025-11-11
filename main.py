# main.py
import pygame as pg
from config import *
from sprites import Player, Platform, Goal 

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("EzGame")
        self.clock = pg.time.Clock()
        self.running = True
        
        self.current_level_index = 0
        self.level_list = LEVEL_LIST
        
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.goal_group = pg.sprite.Group() 

        self.player = Player(self, (0, 0))
        
        self.load_level(self.level_list[self.current_level_index])

    def load_level(self, level_data):
        self.all_sprites.empty()
        self.platforms.empty()
        self.goal_group.empty()
        
        for plat in level_data['platforms']:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            
        g = Goal(*level_data['goal'])
        self.all_sprites.add(g)
        self.goal_group.add(g)
        
        self.player.rect.topleft = level_data['start']
        self.player.vel = pg.math.Vector2(0, 0) 
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()

    def update(self):
        self.all_sprites.update()
        
        if self.player.rect.top > HEIGHT:
            self.load_level(self.level_list[self.current_level_index])
        
        goal_hit = pg.sprite.spritecollide(self.player, self.goal_group, False)
        if goal_hit:
            self.current_level_index += 1
            
            if self.current_level_index >= len(self.level_list):
                # Adicionar tela de vitoria
                self.running = False 
            else:
                self.load_level(self.level_list[self.current_level_index])

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

# Bloco Principal
if __name__ == "__main__":
    g = Game()
    g.run()
    pg.quit()