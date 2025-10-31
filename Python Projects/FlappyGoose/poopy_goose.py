import pygame
import sys
import random

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💩 Poopy Goose: Trick or Treat Edition 🎃")

# --- Colors ---
PURPLE = (40, 10, 60)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
BLACK = (0, 0, 0)
RED = (255, 80, 80)

# --- Game Variables ---
gravity = 0.5
velocity = 0
game_active = True
score = 0

# Goose rect
goose = pygame.Rect(100, HEIGHT // 2, 40, 30)

# Ground
ground_height = 100
ground_y = HEIGHT - ground_height

# Poop projectiles
poops = []

# NPCs
npcs = []
npc_spawn_timer = 0

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Goose Sprite Setup ---
sprite_sheet = pygame.image.load("gooseImg.png").convert_alpha()

# Adjust these numbers to match your sprite’s width and height
FRAME_WIDTH = 202    # ← change if needed; divide total sheet width by 3
FRAME_HEIGHT = sprite_sheet.get_height()

frames = []
for i in range(3):  # 3 frames
    frame = sprite_sheet.subsurface((i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (80, 60))  # upscale for visibility
    frames.append(frame)

current_frame = 0
frame_delay = 7
frame_timer = 0




# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                velocity = -8  # poop thrust upward
                # create falling poop projectile
                poop_rect = pygame.Rect(goose.x + 10, goose.y + 25, 10, 10)
                #Poop emoji
                poop_rect = pygame.Rect(goose.x + 10, goose.y + 25, 10, 10)
                poops.append([poop_rect, -4])  # [rect, upward velocity]
            if event.key == pygame.K_SPACE and not game_active:
                # Restart
                goose.center = (100, HEIGHT // 2)
                velocity = 0
                score = 0
                npcs.clear()
                poops.clear()
                game_active = True

    if game_active:
        # --- Physics ---
        velocity += gravity
        goose.y += velocity*(0.70)

        # --- Check for ground collision ---
        if goose.bottom >= ground_y or goose.top <= 0:
            game_active = False

        # --- Background ---
        screen.fill(PURPLE)
        pygame.draw.circle(screen, ORANGE, (320, 100), 40)

        # --- NPC Spawning ---
        npc_spawn_timer += 1
        if npc_spawn_timer > 90:  # spawn every ~1.5 seconds
            npc_x = random.choice([WIDTH + 20, -40])
            direction = -1 if npc_x > WIDTH else 1
            npcs.append([pygame.Rect(npc_x, ground_y - 30, 20, 30), direction])
            npc_spawn_timer = 0

        # --- Update NPCs ---
        for npc in npcs:
            npc[0].x += npc[1] * 2
        npcs = [n for n in npcs if -50 < n[0].x < WIDTH + 50]

        # --- Update Poops ---
        for p in poops:
            rect, vy = p
            vy += 0.4  # gravity on poop
            rect.y += vy
            p[1] = vy

        # --- Collision detection (poop vs NPC) ---
        for p in poops[:]:
            for npc in npcs[:]:
                if p[0].colliderect(npc[0]):
                    poops.remove(p)
                    npcs.remove(npc)
                    score += 1
                    break

        # --- Draw ---
        # Poops
        # for rect, _ in poops:
        #     pygame.draw.circle(screen, GREEN, rect.center, 5)
        # Poops (💩 emojis instead of green circles)
        # 💩 Emoji Poop Projectiles
        poop_font = pygame.font.SysFont("Segoe UI Emoji", 10)

        for rect, _ in poops:
            poop_surface = poop_font.render("💩", True, (255, 255, 255))
            poop_rect = poop_surface.get_rect(center=rect.center)
            screen.blit(poop_surface, poop_rect)

        # Goose
        # --- Animate Goose ---
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(frames)

        rotated_goose = pygame.transform.rotate(frames[current_frame], -velocity * 2)
        screen.blit(rotated_goose, goose)


        # NPCs
        for npc in npcs:
            pygame.draw.rect(screen, RED, npc[0])

        # Ground
        pygame.draw.rect(screen, BLACK, (0, ground_y, WIDTH, ground_height))

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # --- Game Over ---
        over_text = font.render("💀 Game Over 💩", True, ORANGE)
        rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, rect)
        tip = font.render("Press SPACE", True, WHITE)
        tip_rect = tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(tip, tip_rect)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(score_text, score_rect)

    pygame.display.update()
    clock.tick(60)
