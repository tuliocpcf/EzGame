# main.py
import pygame as pg
from config import *
from sprites import *

# Utilizamos o auxilio de IA generativa para a construcao de certos aspectos do codigo do jogo!

class Game:
    def __init__(self, screen):
        self.screen = screen 
        pg.display.set_caption("EzGame")
        self.clock = pg.time.Clock()
        self.running = True

        # Configuracoes dos Níveis
        self.current_level_index = 0
        self.game_over = False 
        self.start_time = pg.time.get_ticks() 
        self.final_time_ms = 0 
        self.final_score = 0
        self.level_list = LEVEL_LIST  

        # Sons
        self.jump_sound = pg.mixer.Sound(SOUND_JUMP)
        self.walk_sound = pg.mixer.Sound(SOUND_WALK)
        self.run_channel = pg.mixer.Channel(1)

        # Animações do Player e do Fogo 
        self.fire_animation = load_animation_frames(path.join(IMG_DIR, 'fire'), scale=1.0)
        self.player_animations = {
            'idle': load_animation_frames(path.join(IMG_DIR, 'player', 'idle'), scale=1.5), 
            'run': load_animation_frames(path.join(IMG_DIR, 'player', 'run'), scale=1.5),
            'jump': load_animation_frames(path.join(IMG_DIR, 'player', 'jump'), scale=1.5),
            'die': load_animation_frames(path.join(IMG_DIR, 'player', 'die'), scale=1.5),
            }
        
         # Sprites
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.goal_group = pg.sprite.Group()
        self.danger_group = pg.sprite.Group() 

        self.player = Player(self, (0, 0))
        # Primeiro nível
        self.load_level(self.level_list[self.current_level_index])

    def load_level(self, level_data):
        # Limpa os sprites
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
            # Verifica se retornou "quit"
            event_result = self.events() 
            if event_result == "quit":
                return "quit" 

            if not self.game_over:
                self.update()
            self.draw()
            
        return "menu" 
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                return "quit"
            
            # Lógica de input normal (pulo, etc.) ocorre se o jogo não acabou
            if not self.game_over:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.playing = False 
                        return "menu"        
                        
                    if event.key == pg.K_SPACE or event.key == pg.K_UP:
                        self.player.jump()
                        
            # Botão Jogar Novamente
            if self.game_over:
                self.handle_game_over_input(event)
                
        return "continue"
    
    def update(self):
        # Verifica fim da Animação de Morte
        if self.player.is_dying and self.player.current_animation == 'die':
            if self.player.current_frame == len(self.player.animations['die']) - 1:
                self.load_level(self.level_list[self.current_level_index])
                self.player.is_dying = False
                self.player.current_animation = 'idle' 
                self.player.frame_rate = 100 
                return 
            
        self.all_sprites.update()

        # Verifica se o personagem chegou no objetivo
        goal_hit = pg.sprite.spritecollide(self.player, self.goal_group, False)
        if goal_hit:
            if self.current_level_index < len(LEVEL_LIST) - 1:
                # Se ainda houver níveis, carrega o próximo
                self.current_level_index += 1
                self.load_level(LEVEL_LIST[self.current_level_index])
            else:
                # Se completou todos os niveis
                self.game_over = True
                self.end_game_calculation() 

        # Verificar morte no "Void"
        if self.player.rect.top > HEIGHT:
            if not self.player.is_dying:
                self.player.die() # animação de morte

        # Verificar morte por elementos do mapa
        danger_hit = pg.sprite.spritecollide(self.player, self.danger_group, False)
        if danger_hit:
            if not self.player.is_dying:
                self.player.die() # animação de morte
        
        # Verifica "Vitória"
        goal_hit = pg.sprite.spritecollide(self.player, self.goal_group, False)
        if goal_hit:
            self.current_level_index += 1
            if self.current_level_index >= len(self.level_list):
                print("VOCÊ VENCEU!") 
                self.running = False # Encerra o loop do JOGO
            else:
                self.load_level(self.level_list[self.current_level_index])

    def draw(self):
        self.screen.fill(BLACK_HELL)

        if self.game_over:
            self.draw_game_over_screen()
        else:
            self.all_sprites.draw(self.screen)
            self.draw_time() 
            
        pg.display.flip()

    # Calculadora de tempo total e pontuacao final
    def end_game_calculation(self):
        
        # Calcula o tempo total de jogo
        end_time = pg.time.get_ticks()
        self.final_time_ms = end_time - self.start_time
        
        # Calcula os pontos perdidos
        # Pontos perdidos = (Tempo Total em segundos) * (Taxa de Perda por Segundo)
        time_in_seconds = self.final_time_ms / 1000
        
        score_lost = time_in_seconds * 10
        
        # Calcula a pontuação final
        self.final_score = max(BASE_SCORE - int(score_lost), 0) # Garante que a pontuação não seja negativa
        
        # Formata o tempo para mostrar
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
        self.formatted_time = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    # Tela de Parabens
    def draw_game_over_screen(self):
        
        # Configuração de Fonte
        title_font = pg.font.SysFont('arial', 72)
        score_font = pg.font.SysFont('arial', 48)

        # Título
        title_text = title_font.render("PARABÉNS, VOCÊ ESCAPOU!", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Pontuação
        score_text = score_font.render(f"PONTUAÇÃO: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 100))
        self.screen.blit(score_text, score_rect)

        # Tempo Total
        time_text = score_font.render(f"TEMPO: {self.formatted_time}", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 180))
        self.screen.blit(time_text, time_rect)

        # Lógica do Botão
        button_width, button_height = 300, 60
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 3 + 280
        
        # Armazena a posição do botão para uso posterior
        self.restart_button_rect = pg.Rect(button_x, button_y, button_width, button_height)
        
        # Desenha o Botão
        pg.draw.rect(self.screen, RED_HELL, self.restart_button_rect, border_radius=10)
        
        # Texto do Botão
        button_font = pg.font.SysFont('arial', 36)
        button_text = button_font.render("JOGAR NOVAMENTE", True, WHITE)
        button_text_rect = button_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        # Reinicia o Jogo
    def reset_game(self):
        self.current_level_index = 0
        self.game_over = False
        self.start_time = pg.time.get_ticks() # Zera o cronômetro
        self.final_time_ms = 0
        self.final_score = 0
        self.load_level(LEVEL_LIST[self.current_level_index])

        # Verifica cliques do Mouse
    def handle_game_over_input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo do mouse
                mouse_pos = pg.mouse.get_pos()
                
                if hasattr(self, 'restart_button_rect') and self.restart_button_rect.collidepoint(mouse_pos):
                    self.reset_game()

    def draw_time(self):
        
        # Calcula o tempo decorrido desde o início do jogo 
        time_elapsed_ms = pg.time.get_ticks() - self.start_time
        
        # Converte e Formata o tempo
        time_in_seconds = time_elapsed_ms / 1000
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        # Mostra os centésimos de segundo 
        hundredths = int((time_in_seconds * 10) % 10) 
        
        formatted_time = f"TEMPO: {minutes:02d}:{seconds:02d}.{hundredths:01d}"
        
        # Renderiza o texto
        font = pg.font.SysFont('arial', 32, bold=True)
        # Use INFERNO_LARANJA para destacar o cronômetro 
        text_surface = font.render(formatted_time, True, ORANGE_HELL)
        
        # Posiciona no canto superior direito 
        text_rect = text_surface.get_rect(topright=(WIDTH - 50, 50))
        self.screen.blit(text_surface, text_rect)
    
if __name__ == "__main__":
    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)    

    # Inicia trilha sonora
    pg.mixer.music.load("assets/snd/SoundTrack1.mp3")
    pg.mixer.music.set_volume(0.60)
    pg.mixer.music.play(-1) 

    state = "menu"   
    app_running = True
    clock = pg.time.Clock()

    while app_running:
        if state == "menu":
            start_screen = StartScreen(screen)
            start_screen.run()  # loop da tela inicial
            pg.mixer.music.set_volume(0.60)

            if start_screen.start_game:
                start_screen.start_game = False
                state = "instr"
            else:
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
            resultado = g.run() 
            pg.mixer.music.set_volume(0.40)
            
            if resultado == "quit": 
                app_running = False 
            else:
                # quando o jogo terminar win/esc no próprio do jogo, volta ao menu
                state = "menu"

        clock.tick(60)

    pg.quit()
