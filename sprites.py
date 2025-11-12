#sprites.py

import sys
import pygame as pg
from config import *
from os import path

def load_animation_frames(folder_path, scale=1.0):
    frames = []
    animation_name = path.basename(folder_path) 
    
    # Adicione este print para ver o que o código está procurando!
    print(f"Buscando frames na pasta: {folder_path}")
    
    for i in range(100):
        # Opção B: Assumindo nomes de arquivo como 'fire_0.png', 'idle_0.png', etc.
        frame_name = path.join(folder_path, f'{animation_name}_{i}.png')
        
        # DEBUG: Imprima o caminho do primeiro arquivo que ele tenta carregar
        if i == 0:
            print(f"Tentativa de arquivo 0: {frame_name}")
        
        if not path.exists(frame_name):
            # Se não encontrou o primeiro arquivo (i=0), a lista 'frames' estará vazia.
            if i == 0:
                 print(f"ERRO: Não encontrou NENHUM frame. Verifique o caminho e o nome do arquivo '{frame_name}'")
            break
        img = pg.image.load(frame_name).convert_alpha()
        if scale != 1.0:
            img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        img = pg.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT)) 
        
        frames.append(img)
    return frames

def scale_to_fit(surf, max_w, max_h, smooth=True):
    w, h = surf.get_size()
    scale = min(max_w / w, max_h / h)
    new_size = (int(w * scale), int(h * scale))
    return pg.transform.smoothscale(surf, new_size) if smooth else pg.transform.scale(surf, new_size)

class Player(pg.sprite.Sprite):
    def __init__(self, game, start_pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        # --- Animação ---
        self.animations = self.game.player_animations 
        self.current_animation = 'idle'
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100 # ms por frame (ajuste para mais rápido/lento)
        self.facing = 'right' # 'left' ou 'right'
        self.is_dying = False # Flag para animação de morte

        # Define a imagem inicial
        self.image = self.animations[self.current_animation][self.current_frame]
        
        self.rect = pg.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.topleft = start_pos # Posiciona o rect

        self.vel = pg.math.Vector2(0, 0)
        self.on_ground = False

    def animate(self):
        now = pg.time.get_ticks()

        if now - self.last_update > self.frame_rate:
            self.last_update = now

            # 🛑 Se já estamos no último frame de MORTE, TRAVAMOS AQUI
            if self.is_dying and self.current_frame == len(self.animations['die']) - 1:
                pass # Não avança
            else:
                # Para todas as outras animações, faz o loop normal
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

            # Obtém a nova imagem (restante do código...)
            self.image = self.animations[self.current_animation][self.current_frame]

            # Inverte a imagem se estiver indo para a esquerda
            if self.facing == 'left':
                # ✅ NOVO: Aplica a inversão diretamente na imagem recém-selecionada (que já está no tamanho correto)
                self.image = pg.transform.flip(self.image, True, False)

    def jump(self):
        # 🛑 MUDANÇA: Sair da função se estiver morrendo
        if self.is_dying:
            return
            
        if self.on_ground:
            self.vel.y = PLAYER_JUMP
            self.on_ground = False 
            self.game.jump_sound.play()
            self.current_animation = 'jump'

    def die(self):
        if not self.is_dying:
            self.is_dying = True
            self.current_animation = 'die'
            self.current_frame = 0 # Reinicia a animação de morte
            self.frame_rate = 150 # Pode ser mais lento para morte
            self.game.run_channel.stop() # Para o som de andar

    # sprites.py (Dentro da classe Player)

    def update(self):
        # 🛑 1. PRIORIADE MÁXIMA: ESTADO DE MORTE
        # Se estiver morrendo, anula movimento, zera velocidade e apenas anima.
        if self.is_dying:
            self.vel.x = 0
            self.vel.y = 0
            
            self.animate()
            return # Sai do update para pular a física e colisão
        
        # --- (Início da Física e Movimento Normal) ---
        
        # Gravidade
        self.vel.y += GRAVITY
        self.vel.y = min(self.vel.y, 10) 
    
        # Leitura de Input e Velocidade Horizontal
        self.vel.x = 0 
        keys = pg.key.get_pressed()
    
        # Determina o estado da animação de movimento e aplica velocidade
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_VEL
            self.facing = 'left'
            if self.on_ground and self.current_animation != 'run':
                self.current_animation = 'run'
                self.frame_rate = ANIM_RUN_RATE
        elif keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_VEL
            self.facing = 'right'
            if self.on_ground and self.current_animation != 'run':
                self.current_animation = 'run'
                self.frame_rate = ANIM_RUN_RATE
        else:
            if self.on_ground and self.current_animation != 'idle':
                self.current_animation = 'idle'
                self.frame_rate = ANIM_FRAME_RATE
    
        # Animação de Pulo/Queda (só se não estiver no chão E NÃO ESTIVER MORRENDO)
        # O 'jump' só é definido uma vez em self.jump(). Se estiver no ar, mantemos o estado.
        if not self.on_ground and self.current_animation != 'jump': 
            # Esta lógica só deve forçar a animação se a velocidade de queda for muito alta 
            # (no caso de queda) ou se o estado foi perdido, mas não se estiver morrendo.
            self.current_animation = 'jump'
    
        # Lógica de som de andar
        moving_horizontally = (self.vel.x != 0)
        if moving_horizontally and self.on_ground:
            if not self.game.run_channel.get_busy():
                self.game.run_channel.play(self.game.walk_sound, -1)
        else:
            self.game.run_channel.stop()

        # 🛑 2. APLICAÇÃO DE MOVIMENTO E COLISÃO
        
        self.rect.x += self.vel.x
        self.collide_with_platforms('horizontal') 
        
        self.rect.y += self.vel.y
        self.collide_with_platforms('vertical') 
        
        # 🛑 3. REAJUSTE DE RECT E ANIMAÇÃO
        
        old_bottom = self.rect.bottom 
        old_centerx = self.rect.centerx

        self.animate()
        
        self.rect = self.image.get_rect() 
        self.rect.bottom = old_bottom
        self.rect.centerx = old_centerx

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

            # 🛑 NOVO: Só mude a animação ao pousar se NÃO estiver morrendo
            if direction == 'vertical' and self.vel.y > 0:
                self.on_ground = True
                if not self.is_dying: 
                    if self.current_animation == 'jump': # Volta para idle/run ao pousar
                        self.current_animation = 'idle' 
                        self.current_frame = 0 # Reinicia a animação
    
    def die(self):
        # O estado de morte só é iniciado UMA VEZ
        if not self.is_dying:
            self.is_dying = True
            self.current_animation = 'die'
            self.current_frame = 0 # Reinicia a animação de morte
            self.frame_rate = 150 # Pode ser mais lento para morte
            self.game.run_channel.stop() # Para o som de andar

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED_HELL)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Goal(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Fire(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)

        self.animations = game.fire_animation 
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 150 # ms por frame (ajuste)

        # Define a imagem inicial e ajusta o rect
        self.image = pg.transform.scale(self.animations[self.current_frame], (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        now = pg.time.get_ticks()

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations)

            # Atualiza a imagem, mantendo o tamanho original
            self.image = pg.transform.scale(self.animations[self.current_frame], self.rect.size)

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