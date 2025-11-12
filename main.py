# main.py
import pygame as pg
from config import *
from sprites import *

class Game:
    # 1. MUDANÇA: O __init__ agora RECEBE a tela, em vez de criá-la
    def __init__(self, screen):
        self.screen = screen 
        pg.display.set_caption("EzGame")
        self.clock = pg.time.Clock()
        self.running = True
        # --- Gerenciamento de Nível ---
        self.current_level_index = 0
        self.game_over = False # Novo estado de jogo
        self.start_time = pg.time.get_ticks() # Tempo que o jogo começou (em milissegundos)
        self.final_time_ms = 0 # Tempo final, em milissegundos
        self.final_score = 0
        self.level_list = LEVEL_LIST  # <-- Onde 'level_list' é definido

        # Sons
        self.jump_sound = pg.mixer.Sound(SOUND_JUMP)
        self.walk_sound = pg.mixer.Sound(SOUND_WALK)
        self.run_channel = pg.mixer.Channel(1)

        # 1. Carregue as animações do Player e do Fire AQUI
        self.fire_animation = load_animation_frames(path.join(IMG_DIR, 'fire'), scale=1.0)
        self.player_animations = {
            'idle': load_animation_frames(path.join(IMG_DIR, 'player', 'idle'), scale=1.5), 
            'run': load_animation_frames(path.join(IMG_DIR, 'player', 'run'), scale=1.5),
            'jump': load_animation_frames(path.join(IMG_DIR, 'player', 'jump'), scale=1.5),
            'die': load_animation_frames(path.join(IMG_DIR, 'player', 'die'), scale=1.5),
            }
        
         # --- Grupos de Sprites ---
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.goal_group = pg.sprite.Group()
        self.danger_group = pg.sprite.Group() 

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
        
        # Carrega fogo
        if 'spikes' in level_data: 
            for fire_data in level_data['spikes']: 
                f = Fire(self, *fire_data) 
                self.all_sprites.add(f)
                self.danger_group.add(f)
        
        # Carrega o objetivo
        g = Goal(*level_data['goal'])
        self.all_sprites.add(g)
        self.goal_group.add(g)
        
        # Posiciona o jogador
        self.player.rect.topleft = level_data['start']
        self.player.vel = pg.math.Vector2(0, 0)
        self.all_sprites.add(self.player)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            # 🛑 MUDANÇA: Checa se o evento retornou 'quit'
            event_result = self.events() 
            if event_result == "quit":
                return "quit" # Sai do g.run() e passa "quit" para o loop principal

            if not self.game_over:
                self.update()
            self.draw()
            
        return "menu" # Retorna "menu" se saiu do loop porque o jogo acabou
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                return "quit" 
                
            # Lógica de input normal (pulo, etc.) só ocorre se o jogo não acabou
            if not self.game_over:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                        
            # 🛑 NOVO: LÓGICA DE CLIQUE PARA A TELA FINAL
            if self.game_over:
                self.handle_game_over_input(event) # Chama um novo método para o botão
        return "continue"
    
    def update(self):
        # 🛑 Checagem Unificada de Fim da Animação de Morte
        if self.player.is_dying and self.player.current_animation == 'die':
            # ✅ Reset acontece SOMENTE quando o último frame é atingido (e travado pelo Player.animate)
            if self.player.current_frame == len(self.player.animations['die']) - 1:
                self.load_level(self.level_list[self.current_level_index])
                self.player.is_dying = False
                self.player.current_animation = 'idle' 
                self.player.frame_rate = 100 
                return # Sai do update após o reset
            
        # O restante do código de update...
        self.all_sprites.update()

        # 🛑 Checar Colisão com Objetivo (Goal Hit)
        goal_hit = pg.sprite.spritecollide(self.player, self.goal_group, False)
        if goal_hit:
            if self.current_level_index < len(LEVEL_LIST) - 1:
                # Se ainda houver níveis, carrega o próximo
                self.current_level_index += 1
                self.load_level(LEVEL_LIST[self.current_level_index])
            else:
                # 🛑 O JOGADOR COMPLETOU TODOS OS NÍVEIS
                self.game_over = True
                self.end_game_calculation() # Novo método de pontuação

        # Checar "Morte" por Queda (Se o jogador cair fora da tela)
        if self.player.rect.top > HEIGHT:
            if not self.player.is_dying:
                self.player.die() # Inicia a animação de morte

        # Checar "Morte" por Perigo (Fogo/Spikes)
        danger_hit = pg.sprite.spritecollide(self.player, self.danger_group, False)
        if danger_hit:
            if not self.player.is_dying:
                self.player.die() # Inicia a animação de morte
        
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
        # self.screen.fill(self.background_color)
        self.screen.fill(BLACK_HELL) # Fundo preto/vermelho para o tema Inferno

        if self.game_over:
            self.draw_game_over_screen() # Chama o novo método de desenho
        else:
            self.all_sprites.draw(self.screen)
            
        pg.display.flip()

    def end_game_calculation(self):
        """Calcula o tempo total e a pontuação final do jogador."""
        
        # 1. Calcula o tempo total de jogo
        end_time = pg.time.get_ticks()
        self.final_time_ms = end_time - self.start_time
        
        # 2. Calcula os pontos perdidos
        # Pontos perdidos = (Tempo Total em segundos) * (Taxa de Perda por Segundo)
        # 1000 ms = 1 segundo
        time_in_seconds = self.final_time_ms / 1000
        
        # Como SCORE_LOSS_RATE = 10 pontos / 0.1s, isso é 100 pontos por segundo.
        # Se você definiu SCORE_LOSS_RATE = 10 no config.py, use 100 aqui para 1 ponto / 0.1s
        score_lost = time_in_seconds * 10
        
        # 3. Calcula a pontuação final
        self.final_score = max(BASE_SCORE - int(score_lost), 0) # Garante que a pontuação não seja negativa
        
        # 4. Formata o tempo para exibição
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
        self.formatted_time = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def draw_game_over_screen(self):
        """Desenha a tela de parabéns com a pontuação e o tempo."""
        
        # Configuração de Fonte
        title_font = pg.font.SysFont('arial', 72)
        score_font = pg.font.SysFont('arial', 48)

        # 1. Título
        title_text = title_font.render("PARABÉNS, VOCÊ ESCAPOU!", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # 2. Pontuação
        score_text = score_font.render(f"PONTUAÇÃO: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 100))
        self.screen.blit(score_text, score_rect)

        # 3. Tempo Total
        time_text = score_font.render(f"TEMPO: {self.formatted_time}", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 180))
        self.screen.blit(time_text, time_rect)

        # --- NOVO: Lógica do Botão ---
        
        button_width, button_height = 300, 60
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 3 + 280
        
        # Armazena a posição do botão para uso posterior
        self.restart_button_rect = pg.Rect(button_x, button_y, button_width, button_height)
        
        # Desenha o Botão (Quadrado)
        pg.draw.rect(self.screen, RED_HELL, self.restart_button_rect, border_radius=10)
        
        # Texto do Botão
        button_font = pg.font.SysFont('arial', 36)
        button_text = button_font.render("JOGAR NOVAMENTE", True, WHITE)
        button_text_rect = button_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def reset_game(self):
        """Reinicia o jogo para o estado inicial (Nível 1)."""
        self.current_level_index = 0
        self.game_over = False
        self.start_time = pg.time.get_ticks() # Zera o cronômetro
        self.final_time_ms = 0
        self.final_score = 0
        self.load_level(LEVEL_LIST[self.current_level_index])

    def handle_game_over_input(self, event):
        """Verifica cliques de mouse na tela final."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo do mouse
                mouse_pos = pg.mouse.get_pos()
                
                # Verifica se o clique está dentro da área do botão
                # Note: self.restart_button_rect deve ser definido em draw_game_over_screen()
                if hasattr(self, 'restart_button_rect') and self.restart_button_rect.collidepoint(mouse_pos):
                    self.reset_game()
    
#-----------------------------------------------------------------------------------------------------------------------#
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
            resultado = g.run() # 🛑 MUDANÇA: Armazenar o resultado de g.run()
            pg.mixer.music.set_volume(0.40)
            
            if resultado == "quit": # Se o botão X foi pressionado
                app_running = False # 🛑 FECHA O LOOP PRINCIPAL
            else:
                # quando o jogo terminar (win/escape próprio do jogo), volta ao menu
                state = "menu"

        # mantém 60 fps no loop do app
        clock.tick(60)

    pg.quit()
