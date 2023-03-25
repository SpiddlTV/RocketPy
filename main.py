import random

import pygame, sys
import time

pygame.init()
screen = pygame.display.set_mode((576,1024))
FPS = 120
FramePerSecond = pygame.time.Clock()


middle_x = int(screen.get_width() / 2)
middle_y = int(screen.get_height() / 2)

## Hintergrund ##
hintergrund = pygame.image.load("lib/assets/background-night.png").convert()  # Lädt das Background-Image aus den assets
hintergrund = pygame.transform.scale(hintergrund, (screen.get_width(), screen.get_height())) # Skaliert das Bild und passt es der Größe an

## Basis ##
basis = pygame.image.load("lib/assets/base.png").convert()
basis = pygame.transform.scale(basis, (screen.get_width(), basis.get_height()))
basis_x = 0

## Sprite ##

sprite = pygame.image.load("lib/assets/bluebird-midflap.png").convert()
sprite = pygame.transform.scale2x(sprite)
sprite_x = middle_x - int(middle_x / 2) # Setzt die Position auf der X-Achse des Sprites
sprite_y = middle_y # Setzt die Position auf der Y-Achse des Sprites
sprite_rect = sprite.get_rect(center=(sprite_x, sprite_y)) # Gibt dem Sprite eine Hitbox
sprite_move = 1

## Hindernisse ##

obstacle = pygame.image.load("lib/assets/pipe-green.png").convert()
obstacle = pygame.transform.scale2x(obstacle)
obstacle_Choices = [700, 800, 900]
obstacles = []

SPAWNOBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWNOBSTACLE, 1000) # Jede Sekunde führt PyGame das Userevent aus

def spawn_obstacle():
    obstacle_height = random.choice(obstacle_Choices)
    obstacle_rect_normal = obstacle.get_rect(center=(700, obstacle_height))
    obstacle_rect_flip = obstacle.get_rect(center=(700, obstacle_height - 1000))
    return obstacle_rect_normal, obstacle_rect_flip

def draw_obstacle(obstacles):
    for obstacle_i in obstacles:
        if obstacle_i.bottom >= 2048:
            screen.blit(obstacles, obstacle_i)
        else:
            new_obstacle = pygame.transform.flip(obstacle, False, True)
            screen.blit(new_obstacle, obstacle_i)

def move_obstacle(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 3
## While-Schleife ##
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Prüft ob die taste gleich der Leertaste ist
                sprite_move = 0 # Schaltet die Gravitation aus
                sprite_move -= 10 # Lässt den Sprite nach oben Springen
        if event.type == SPAWNOBSTACLE:
            obstacles.extend(spawn_obstacle())

    ## Zeichnungen ##

    screen.blit(hintergrund, (0,0)) # Zeichnet den Hintergrund in den Screen
    screen.blit(basis, (basis_x,900)) # Zeichnet die Basis
    screen.blit(basis, (basis_x + screen.get_width(), 900))  # Zeichnet die Basis ein zweites mal für den Bewegungseffekt
    screen.blit(sprite, sprite_rect)

    sprite_rect.centery += sprite_move

    sprite_move += 0.25 # Graviation

    draw_obstacle(obstacles)
    move_obstacle(obstacles)

    basis_x -= 1 # Bewegt die basis
    ## Unendlicher Boden ##
    if abs(basis_x) == screen.get_width():  # Vergleicht die Basis_X Variabel mit der Breite des Bildschirms, wenn es außerhalb des Bildschirms ist, wird alles zurückgesetzt und die Animation "startet neu"
        basis_x = 0 # Setzt die Variabel zurück



    FramePerSecond.tick(FPS)
    pygame.display.update()