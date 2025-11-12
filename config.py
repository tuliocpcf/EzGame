#config.py

from os import path
import pygame as pg

#Utilizei como referencia o arquivo "config.py" do handout e ajuda de IA para criacão das fases

IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
TITLE = "EzGame"
SUBTITLE = "Pressione ENTER ou clique em JOGAR"
WIDTH = 1024  # Largura da tela
HEIGHT = 576  # Altura da tela
FPS = 60      

# Pontuação
BASE_SCORE = 5000 
SCORE_LOSS_RATE = 10  # Pontos perdidos a cada segundo (1 pontos / 0.1s = 10 pontos por segundo) 

# Player Config
PLAYER_WIDTH = 30   # Largura do Player
PLAYER_HEIGHT = 40  # Altura do Player
PLAYER_VEL = 5      # Velocidade de movimento
GRAVITY = 0.8       # Aceleração da gravidade
PLAYER_JUMP = -14   # Força do pulo 
SOUND_JUMP = path.join(SND_DIR, 'jump.flac') 
SOUND_WALK = path.join(SND_DIR, 'run.flac') 
ANIM_FRAME_RATE = 500       
ANIM_RUN_RATE = 70          
ANIM_JUMP_RATE = 150       

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
RED_HELL = (150, 0, 0) 
ORANGE_HELL = (255, 100, 0) 
BLACK_HELL = (30, 0, 0) 

# Mapas das Fases
# 'platforms': blocos de colisão normal (x, y, largura, altura)
# 'spikes': espinhos (x, y, largura, altura)
# 'start': posição inicial do player (x, y) 
# 'goal': objetivo (x, y, largura, altura)

LEVEL_1 = {
    # Moldura
    'platforms': [
        (0, HEIGHT - 20, WIDTH, 20),         
        (0, 0, WIDTH, 20),                   
        (0, 20, 20, HEIGHT - 40),            
        (WIDTH - 20, 20, 20, HEIGHT - 40),   
        
        # Plataformas de Movimentação
        (250, HEIGHT - 120, 150, 20),       
        (550, HEIGHT - 220, 150, 20),       
    ],

    'start': (60, HEIGHT - 60),
    'goal': (600, HEIGHT - 280, 30, 60)
}

LEVEL_2 = {
    # Moldura
    'platforms': [
        (0, HEIGHT - 20, WIDTH, 20),       
        (0, 0, WIDTH, 20),                   
        (0, 20, 20, HEIGHT - 40),            
        (WIDTH - 20, 20, 20, HEIGHT - 40),   
        
        # Plataformas
        (120, HEIGHT - 135, 200, 20),        
        (520, HEIGHT - 135, 200, 20),
        (20, HEIGHT - 385, 850, 20),
        (850, HEIGHT - 240, 50, 20),
        (954, HEIGHT - 300, 50, 20)    



    ],
    # Fogo: Fosso entre as plataformas
    'spikes': [
        (220, HEIGHT - 40, 20, 20), (240, HEIGHT - 40, 20, 20), (260, HEIGHT - 40, 20, 20),
        (280, HEIGHT - 40, 20, 20), (300, HEIGHT - 40, 20, 20), (320, HEIGHT - 40, 20, 20),
        
        (590, HEIGHT - 155, 20, 20), (610, HEIGHT - 155, 20, 20), (630, HEIGHT - 155, 20, 20),

        (984, HEIGHT - 320, 20, 20)
    ],
    'start': (60, HEIGHT - 60),
    'goal': (80, HEIGHT - 445, 30, 60)
}

LEVEL_3 = {
    # Paredes Estéticas Finas
    'platforms': [
        (0, HEIGHT - 20, WIDTH, 20),         
        (0, 0, WIDTH, 20),                   
        (0, 20, 20, HEIGHT - 40),            
        (WIDTH - 20, 20, 20, HEIGHT - 40),   
        
        # Degraus
        (100, HEIGHT - 110, 100, 20),         
        (250, HEIGHT - 200, 100, 20),        
        (400, HEIGHT - 290, 100, 20),        
        (550, HEIGHT - 380, 100, 20),        
        
        (700, HEIGHT - 470, 200, 20),                 
    ],
    # Fogo: No topo de cada degrau e no chão
    'spikes': [
        (140, HEIGHT - 130, 20, 20),         
        (160, HEIGHT - 130, 20, 20),
        
        (290, HEIGHT - 220, 20, 20),         
        (310, HEIGHT - 220, 20, 20),
        
        (440, HEIGHT - 310, 20, 20),         
        (460, HEIGHT - 310, 20, 20),

        (590, HEIGHT - 400, 20, 20),         
        (610, HEIGHT - 400, 20, 20),
        
        # Fogo no chão
        (700, HEIGHT - 40, 20, 20), (720, HEIGHT - 40, 20, 20), (740, HEIGHT - 40, 20, 20),
    ],
    'start': (60, HEIGHT - 60),
    'goal': (850, HEIGHT - 530, 30, 60)
}

LEVEL_4 = {
    # Moldura
    'platforms': [
        (0, HEIGHT - 20, WIDTH, 20),         
        (0, 0, WIDTH, 20),                   
        (0, 20, 20, HEIGHT - 40),            
        (WIDTH - 20, 20, 20, HEIGHT - 40),   
        
        (20, HEIGHT - 456, 100, 20),
        (220, HEIGHT - 556, 20, 356),
        (220, HEIGHT - 200, 634, 20),
        (904, HEIGHT - 120, 50, 20),
        

    ],
    # Fogo: Sequência de obstáculos baixos no chão principal
    'spikes': [

        (120, HEIGHT - 250, 20, 20), (140, HEIGHT - 250, 20, 20), (160, HEIGHT - 250, 20, 20), (180, HEIGHT - 250, 20, 20), (200, HEIGHT - 250, 20, 20),  
        (20, HEIGHT - 40, 20, 20), (40, HEIGHT - 40, 20, 20), (60, HEIGHT - 40, 20, 20), (80, HEIGHT - 40, 20, 20), (100, HEIGHT - 40, 20, 20),
        (220, HEIGHT - 40, 20, 20), (220, HEIGHT - 60, 20, 20), (220, HEIGHT - 80, 20, 20), (220, HEIGHT - 100, 20, 20), (220, HEIGHT - 120, 20, 20),
        (320, HEIGHT - 40, 20, 20), (320, HEIGHT - 60, 20, 20), (320, HEIGHT - 80, 20, 20), (320, HEIGHT - 100, 20, 20),
        (400, HEIGHT - 180, 20, 20), (400, HEIGHT - 160, 20, 20), (400, HEIGHT - 140, 20, 20), (400, HEIGHT - 120, 20, 20), (400, HEIGHT - 100, 20, 20),
        (500, HEIGHT - 40, 20, 20), (520, HEIGHT - 40, 20, 20), (540, HEIGHT - 40, 20, 20), (560, HEIGHT - 40, 20, 20), (580, HEIGHT - 40, 20, 20), (600, HEIGHT - 40, 20, 20), (600, HEIGHT - 40, 20, 20),
        (864, HEIGHT - 40, 20, 20), (884, HEIGHT - 40, 20, 20), (904, HEIGHT - 40, 20, 20), (924, HEIGHT - 40, 20, 20), (944, HEIGHT - 40, 20, 20), (964, HEIGHT - 40, 20, 20), (984, HEIGHT - 40, 20, 20),
    ],
    'start': (60, HEIGHT - 496),
    'goal': (300, HEIGHT - 260, 30, 60)
}

LEVEL_5 = {
    # Moldura
    'platforms': [
        (0, HEIGHT - 20, WIDTH, 20),         
        (0, 0, WIDTH, 20),                   
        (0, 20, 20, HEIGHT - 40),            
        (WIDTH - 20, 20, 20, HEIGHT - 40),   
        
        # Plataforma Inicial
        (20, HEIGHT - 100, 100, 20),
        
        # Plataformas Estreitas e Distantes
        (250, HEIGHT - 200, 60, 20),
        (450, HEIGHT - 290, 60, 20),
        (650, HEIGHT - 380, 60, 20),
        
        # Plataforma do Objetivo
        (850, HEIGHT - 470, 100, 20),
    ],
    # Fogo: Cobrindo o chão abaixo e em cima das plataformas
    'spikes': [
        # Fogo em cima dos degraus
        (270, HEIGHT - 220, 20, 20),
        (470, HEIGHT - 310, 20, 20),
        (670, HEIGHT - 400, 20, 20),
        
        # Fosso Grande
        (20, HEIGHT - 40, 20, 20), (40, HEIGHT - 40, 20, 20), (60, HEIGHT - 40, 20, 20), (80, HEIGHT - 40, 20, 20), (100, HEIGHT - 40, 20, 20), (120, HEIGHT - 40, 20, 20), (140, HEIGHT - 40, 20, 20), (160, HEIGHT - 40, 20, 20), (180, HEIGHT - 40, 20, 20), (200, HEIGHT - 40, 20, 20), (220, HEIGHT - 40, 20, 20), (240, HEIGHT - 40, 20, 20), (260, HEIGHT - 40, 20, 20), (280, HEIGHT - 40, 20, 20), (300, HEIGHT - 40, 20, 20), (320, HEIGHT - 40, 20, 20), (340, HEIGHT - 40, 20, 20), (360, HEIGHT - 40, 20, 20), (380, HEIGHT - 40, 20, 20), (400, HEIGHT - 40, 20, 20), (420, HEIGHT - 40, 20, 20), (440, HEIGHT - 40, 20, 20), (460, HEIGHT - 40, 20, 20), (480, HEIGHT - 40, 20, 20), (500, HEIGHT - 40, 20, 20), (520, HEIGHT - 40, 20, 20), (540, HEIGHT - 40, 20, 20), (560, HEIGHT - 40, 20, 20), (580, HEIGHT - 40, 20, 20), (600, HEIGHT - 40, 20, 20), (620, HEIGHT - 40, 20, 20), (640, HEIGHT - 40, 20, 20), (660, HEIGHT - 40, 20, 20), (680, HEIGHT - 40, 20, 20), (700, HEIGHT - 40, 20, 20), (720, HEIGHT - 40, 20, 20), (740, HEIGHT - 40, 20, 20), (760, HEIGHT - 40, 20, 20), (780, HEIGHT - 40, 20, 20), (800, HEIGHT - 40, 20, 20), (820, HEIGHT - 40, 20, 20), (840, HEIGHT - 40, 20, 20), (860, HEIGHT - 40, 20, 20), (880, HEIGHT - 40, 20, 20), (900, HEIGHT - 40, 20, 20), (920, HEIGHT - 40, 20, 20), (940, HEIGHT - 40, 20, 20), (960, HEIGHT - 40, 20, 20), (980, HEIGHT - 40, 20, 20)

    ],
    'start': (60, HEIGHT - 140),
    'goal': (900, HEIGHT - 530, 30, 60)
}



# Lista de níveis em ordem
LEVEL_LIST = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]