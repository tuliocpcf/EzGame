from os import path
import pygame as pg

#Utilizei como referencia o arquivo "config.py" do handout e ajuda de IA para criacão das fases

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
TITLE = "EzGame"
SUBTITLE = "Pressione ENTER ou clique em JOGAR"
WIDTH = 1024  # Largura da tela
HEIGHT = 576  # Altura da tela
FPS = 60      # Frames por segundo

# Config player
PLAYER_WIDTH = 30   # Largura do Player
PLAYER_HEIGHT = 40  # Altura do Player
PLAYER_VEL = 5      # Velocidade de movimento
GRAVITY = 0.8       # Aceleração da gravidade
PLAYER_JUMP = -15   # Força do pulo (negativo porque Y aumenta para baixo)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

# Mapas das Fases
# 'platforms': blocos de colisão normal (x, y, largura, altura)
# 'spikes': espinhos (x, y, largura, altura)
# 'start': posição inicial do player (x, y) 
# 'goal': objetivo (x, y, largura, altura)

LEVEL_1 = {
    'platforms': [
        (0, HEIGHT - 40, WIDTH, 40),        # Chão
        (200, HEIGHT - 120, 150, 20),       # Plataforma 1
        (450, HEIGHT - 250, 100, 20),       # Plataforma 2
        (700, HEIGHT - 350, 80, 20) # Plataforma do objetivo
    ],
    'spikes': [
        (500, HEIGHT - 270, 20, 20) # Em cima da plataforma 2
    ],
    'start': (50, HEIGHT - 100),
    'goal': (720, HEIGHT - 380, 40, 30)
}

LEVEL_2 = {
    'platforms': [
        (0, HEIGHT - 40, WIDTH, 40),              # Chão
        (100, HEIGHT - 150, 100, 20),             # Parede baixa
        (WIDTH / 2 - 20, HEIGHT - 150, 40, 120),  # Parede central
        (WIDTH - 200, HEIGHT - 150, 100, 20)
    ],
    'spikes': [
        (WIDTH / 2 - 100, HEIGHT - 60, 200, 20),

    ],
    'start': (50, HEIGHT - 100),
    'goal': (WIDTH - 150, HEIGHT - 180, 40, 30)
}

LEVEL_3 = {
    'platforms': [
        # Um "poço" no meio
        (0, HEIGHT - 40, WIDTH / 3, 40),
        (WIDTH - (WIDTH / 3), HEIGHT - 40, WIDTH / 3, 40),
        # Plataformas flutuantes
        (100, HEIGHT - 150, 100, 20),
        (300, HEIGHT - 250, 100, 20),
        (500, HEIGHT - 350, 100, 20)
    ],
    'spikes': [
        (WIDTH / 3, HEIGHT - 20, WIDTH / 3, 20) 
    ],
    'start': (50, HEIGHT - 100),
    'goal': (530, HEIGHT - 380, 40, 30)
}

# Lista de níveis em ordem
LEVEL_LIST = [LEVEL_1, LEVEL_2, LEVEL_3]