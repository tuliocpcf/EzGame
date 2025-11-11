# main.py
import pygame as pg
from config import *
from sprites import *

class Game:
    # 1. MUDANÇA: O __init__ agora RECEBE a tela, em vez de criá-la
    def __init__(self, screen):
        # pg.init() não é mais necessário aqui, já foi chamado
        self.screen = screen # Recebe a tela
        pg.display.set_caption("EzGame")
        self.clock = pg.time.Clock()
        self.running = True
        
        # --- Gerenciamento de Nível ---
        self.current_level_index = 0
        self.level_list = LEVEL_LIST
        
        # --- Grupos de Sprites ---
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.goal_group = pg.sprite.Group()
        self.danger_group = pg.sprite.Group() 
        
        # Cria o jogador
        self.player = Player(self, (0, 0))
        
        # Carrega o primeiro nível
        self.load_level(self.level_list[self.current_level_index])

    def load_level(self, level_data):
        # Limpa os grupos
        self.all_sprites.empty()
        self.platforms.empty()
        self.goal_group.empty()
        self.danger_group.empty() 
        
        # Carrega as plataformas
        for plat in level_data['platforms']:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            
        # Carrega os Espinhos
        if 'spikes' in level_data:
            for spike_data in level_data['spikes']:
                s = Spike(*spike_data)
                self.all_sprites.add(s)
                self.danger_group.add(s)
        
        # Carrega o objetivo
        g = Goal(*level_data['goal'])
        self.all_sprites.add(g)
        self.goal_group.add(g)
        
        # Posiciona o jogador
        self.player.rect.topleft = level_data['start']
        self.player.vel = pg.math.Vector2(0, 0)
        self.all_sprites.add(self.player)

    def run(self):
        # O loop do jogo principal
        # Note que self.running é a flag da classe Game
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
        
        # Checar "Morte"
        if self.player.rect.top > HEIGHT:
            self.load_level(self.level_list[self.current_level_index])
        
        danger_hit = pg.sprite.spritecollide(self.player, self.danger_group, False)
        if danger_hit:
            self.load_level(self.level_list[self.current_level_index])
        
        # Checar "Vitória"
        goal_hit = pg.sprite.spritecollide(self.player, self.goal_group, False)
        if goal_hit:
            self.current_level_index += 1
            if self.current_level_index >= len(self.level_list):
                print("VOCÊ VENCEU!") 
                self.running = False # Encerra o loop do JOGO
            else:
                self.load_level(self.level_list[self.current_level_index])

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

# --- 2. MUDANÇA: Bloco principal agora gerencia as cenas ---
if __name__ == "__main__":
    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # Carrega e inicia a trilha UMA VEZ
    # Recomendo .ogg pela estabilidade no pygame
    pg.mixer.music.load("assets/snd/SoundTrack1.mp3")
    pg.mixer.music.set_volume(0.60)
    pg.mixer.music.play(-1)  # loop

    state = "menu"   # "menu" -> "instr" -> "game"
    app_running = True
    clock = pg.time.Clock()

    while app_running:
        if state == "menu":
            start_screen = StartScreen(screen)
            start_screen.run()  # loop da tela inicial
            pg.mixer.music.set_volume(0.60)

            if start_screen.start_game:
                # usuário clicou JOGAR -> vai para instruções
                start_screen.start_game = False
                state = "instr"
            else:
                # usuário fechou a janela na tela inicial
                app_running = False

        elif state == "instr":
            instrucoes_screen = InstructionScreen(screen)
            resultado = instrucoes_screen.run()
            pg.mixer.music.set_volume(0.50)

            if resultado == "next":
                state = "game"
            elif resultado == "back":
                state = "menu"

        elif state == "game":
            g = Game(screen)
            g.run()
            pg.mixer.music.set_volume(0.40)
            # quando o jogo terminar (win/escape próprio do jogo), volta ao menu
            state = "menu"

        # mantém 60 fps no loop do app
        clock.tick(60)

    pg.quit()
