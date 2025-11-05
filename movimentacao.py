import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 1280
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Easy Game')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img\individual_sheets\male_hero_template-combo_1_end.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.gravity = 2

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedy += self.gravity

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

clock = pygame.time.Clock()
FPS = 30
game = True
jogador = Player()
all_sprites = pygame.sprite.Group()

all_sprites.add(jogador)
while game:
    clock.tick(FPS) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jogador.speedx = -5
            
            if event.key == pygame.K_RIGHT:
                jogador.speedx = 5
            if event.key == pygame.K_SPACE:
                jogador.speedy = -10
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jogador.speedx = 0

            if event.key == pygame.K_SPACE:
                jogador.speedy = -10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    jogador.speedy = 0
            #pula quando tiver chão apenas
            #if event.key == pygame.K_SPACE and jogador.rect.bottom >= HEIGHT:
            #jogador.speedy = -15


    # Atualiza
    all_sprites.update()

    # Desenha
    # window.blit(background, (0, 0))
    window.fill((255, 255, 255))
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()

