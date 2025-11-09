# step1_window.py
import pygame, sys

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Step 1: Window")
clock = pygame.time.Clock()

PURPLE = (40, 10, 60)

running = True
while running:
    # 1) Handle events (quit button, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2) Update world (nothing yet)

    # 3) Draw
    screen.fill(PURPLE)

    # 4) Flip buffers + cap FPS
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
