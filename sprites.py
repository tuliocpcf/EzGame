import sys
import pygame as pg
from config import *

def scale_to_fit(surf, max_w, max_h, smooth=True):
    w, h = surf.get_size()
    scale = min(max_w / w, max_h / h)
    new_size = (int(w * scale), int(h * scale))
    return pg.transform.smoothscale(surf, new_size) if smooth else pg.transform.scale(surf, new_size)

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

class Spike(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.Surface((w, h))
        self.image.fill(GREY) 
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True

        self.start_game = False

        # Fontes
        self.title_font = pg.font.Font("assets/fonts/Race Sport.ttf", 100)
        self.subtitle_font = pg.font.Font("assets/fonts/Race Sport.ttf", 24)

        # Fundo
        self.bg_image = pg.image.load("assets/img/Tela de Fundo Jogo.png").convert()
        self.bg_image = pg.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        # Botões
        btn_norm = pg.image.load("assets/img/Botao.png").convert_alpha()
        btn_hover = pg.image.load("assets/img/Botao_Clicado.png").convert_alpha()

        MAX_W, MAX_H = 920, 425
        self.start_btn_image = scale_to_fit(btn_norm, MAX_W, MAX_H)
        self.start_btn_image_hover = scale_to_fit(btn_hover, MAX_W, MAX_H)

        # Área clicável ajustada ao tamanho do botão
        self.start_btn_rect = self.start_btn_image.get_rect()  
        self.start_btn_rect.center = (WIDTH // 2, HEIGHT // 2 + 120)

        self.start_btn_mask = pg.mask.from_surface(self.start_btn_image)  

        self._is_hover = False

    # >>> NEW: helper para saber se o mouse está sobre a parte "opaca" do botão
    def _point_on_button(self, pos):
        if not self.start_btn_rect.collidepoint(pos):
            return False
        rel_x = pos[0] - self.start_btn_rect.left
        rel_y = pos[1] - self.start_btn_rect.top
        # Proteção extra caso coordenadas fiquem na borda
        if rel_x < 0 or rel_y < 0:
            return False
        if rel_x >= self.start_btn_mask.get_size()[0] or rel_y >= self.start_btn_mask.get_size()[1]:
            return False
        return self.start_btn_mask.get_at((rel_x, rel_y)) != 0

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                    self.start_game = True # <-- 4. MUDAR AQUI
                    self.running = False   # <-- 4. MUDAR AQUI

            elif event.type == pg.MOUSEMOTION:
                self._is_hover = self._point_on_button(event.pos)

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self._point_on_button(event.pos):
                    self.start_game = True # <-- 4. MUDAR AQUI
                    self.running = False   # <-- 4. MUDAR AQUI

    def draw(self):
        # Fundo
        self.screen.blit(self.bg_image, (0, 0))

        # Título
        title_surf = self.title_font.render(TITLE, True, (BLACK))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.screen.blit(title_surf, title_rect)

        # Subtítulo
        subtitle_surf = self.subtitle_font.render(SUBTITLE, True, (BLACK))
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Botão Pressionado
        image_to_draw = self.start_btn_image_hover if self._is_hover else self.start_btn_image
        self.screen.blit(image_to_draw, self.start_btn_rect.topleft)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pg.display.flip()
            self.clock.tick(60) 

class InstructionScreen:
    def __init__(self, screen, next_signal="next"):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.next_signal = next_signal

        # === Background fixo ===
        self.bg_image = pg.image.load("assets/img/Instructions.png").convert()
        self.bg_image = pg.transform.smoothscale(self.bg_image, (WIDTH, HEIGHT))

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        return "back"
                    if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                        self.running = False
                        return self.next_signal

            # === Desenho da tela ===
            self.screen.blit(self.bg_image, (0, 0))

            pg.display.flip()