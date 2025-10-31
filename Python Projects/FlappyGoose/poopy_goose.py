import pygame
import sys
import random

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 900, 600
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

# Ghosts
ghosts = []
ghost_spawn_timer = 0

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Goose Sprite Setup ---
sprite_sheet = pygame.image.load("gooseImg.png").convert_alpha()


# --- Student Sprite Setup ---
student_sheet = pygame.image.load("walking_student.png").convert_alpha()

# --- Ghost Sprite Setup ---
ghost_img = pygame.image.load("ghost.png").convert_alpha()
ghost_img = pygame.transform.scale(ghost_img, (60, 50))

STUDENT_FRAME_WIDTH = 90     # adjust to your sheet
STUDENT_FRAME_HEIGHT = student_sheet.get_height()
student_frames = []

for i in range(4):  # 4 walking frames
    frame = student_sheet.subsurface((i * STUDENT_FRAME_WIDTH, 0, STUDENT_FRAME_WIDTH, STUDENT_FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (60, 80))  # resize for visibility
    student_frames.append(frame)



# --- Background Setup ---
bg = pygame.image.load("bg_river.png").convert()  # your background image
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bg_x = 0           # current x position of background
bg_speed = 2       # how fast it scrolls

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
        goose.y += velocity*(0.6)

        # --- Check for ground collision ---
        if goose.bottom >= ground_y or goose.top <= 0:
            game_active = False

        # --- Check for ghost collision with goose ---
        for ghost in ghosts:
            if goose.colliderect(ghost["rect"]):
                game_active = False

        # --- Background ---
        # screen.fill(PURPLE)
        # pygame.draw.circle(screen, ORANGE, (320, 100), 40)


        # --- Scrolling Background ---
        bg_x -= bg_speed

        # Draw two copies side by side for looping
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + WIDTH, 0))

        # Reset scroll when first image goes off-screen
        if bg_x <= -WIDTH:
            bg_x = 0


        # --- NPC Spawning ---
        npc_spawn_timer += 1
        if npc_spawn_timer > 90:  # spawn every ~1.5 seconds
            from_right = random.choice([True, False])

            if from_right:
                npc_x = WIDTH + 60     # spawn just off the right edge
                direction = -1         # move left
            else:
                npc_x = -60            # spawn just off the left edge
                direction = 1          # move right

            npcs.append({
                "rect": pygame.Rect(npc_x, ground_y - 80, 60, 80),
                "dir": direction,
                "frame": random.randint(0, len(student_frames) - 1),
                "timer": 0,
                "speed": random.uniform(1.0, 2.5)  # varied walking speed
            })

            npc_spawn_timer = 0


        # --- Update NPCs ---
        for npc in npcs:
            npc["rect"].x += npc["dir"] * 1.5
            npc["timer"] += 1
            if npc["timer"] >= 8:  # slower = smoother walk
                npc["timer"] = 0
                npc["frame"] = (npc["frame"] + 1) % len(student_frames)

        # Remove off-screen NPCs
        npcs = [n for n in npcs if -80 < n["rect"].x < WIDTH + 80]

        # --- Draw NPCs ---
        for npc in npcs:
            frame_img = student_frames[npc["frame"]]
            if npc["dir"] == -1:
                frame_img = pygame.transform.flip(frame_img, True, False)
            screen.blit(frame_img, npc["rect"])

        # --- Ghost Spawning ---
        ghost_spawn_timer += 1
        if ghost_spawn_timer > random.randint(80, 160):  # random interval for chaos
            ghost_y = random.randint(80, ground_y - 200)  # spawn randomly in the air
            ghosts.append({
                "rect": pygame.Rect(WIDTH + 40, ghost_y, 60, 50),
                "speed": random.uniform(2.5, 4.5),  # move left
                "vy": random.choice([-1, 1]) * random.uniform(0.2, 0.6)  # floaty motion
            })
            ghost_spawn_timer = 0
        # --- Update Ghosts ---
        for ghost in ghosts:
            ghost["rect"].x -= ghost["speed"]
            ghost["rect"].y += ghost["vy"]

            # make ghosts bounce a little vertically
            if ghost["rect"].top <= 50 or ghost["rect"].bottom >= ground_y - 120:
                ghost["vy"] *= -1

        # remove off-screen ghosts
        ghosts = [g for g in ghosts if g["rect"].right > 0]
        # --- Draw Ghosts ---
        for ghost in ghosts:
            ghost_surface = ghost_img.copy()
            ghost_surface.set_alpha(180)  # ghost transparency (optional)
            screen.blit(ghost_surface, ghost["rect"])
        # --- Update Poops ---
        for p in poops:
            rect, vy = p
            vy += 0.4  # gravity on poop
            rect.y += vy
            p[1] = vy

        # --- Collision detection (poop vs NPC) ---
        for p in poops[:]:
            for npc in npcs[:]:
                if p[0].colliderect(npc["rect"]): 
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
        poop_font = pygame.font.SysFont("Segoe UI Emoji", 20)

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
        # for npc in npcs:
        #     pygame.draw.rect(screen, 0, npc["rect"]) 

        # Ground
        pygame.draw.rect(screen, BLACK, (0, ground_y, WIDTH, ground_height))

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        bg_speed = 2 + (score * 0.1)

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
