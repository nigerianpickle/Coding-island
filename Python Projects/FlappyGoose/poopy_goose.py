import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 900, 600
GROUND_HEIGHT = 100
FPS = 60

# Colors
PURPLE = (40, 10, 60)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💩 Poopy Goose: Trick or Treat Edition 🎃")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Game Variables ---
gravity = 0.5
velocity = 0
game_active = True
score = 0
ground_y = HEIGHT - GROUND_HEIGHT

# --- Player (Goose) Setup ---
goose = pygame.Rect(100, HEIGHT // 2, 40, 30)
goose_sheet = pygame.image.load("gooseImg.png").convert_alpha()

FRAME_WIDTH = 202
FRAME_HEIGHT = goose_sheet.get_height()
goose_frames = [
    pygame.transform.scale(
        goose_sheet.subsurface((i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)),
        (80, 60)
    )
    for i in range(3)
]
current_frame = 0
frame_timer = 0
frame_delay = 20

# --- Background Setup ---
# bg = pygame.image.load("bg_river.png").convert()
# bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
# bg_x = 0
# bg_speed = 2

background_files = [
    "bg_river.png",
    "bg_plain2.png",
    "bg_river.png",
    "bg_castle.png",
    "bg_plain.png",
    "bg_river.png",
    "bg_plain2.png",
    "bg_plain2.png",
    "bg_lighthouse.png",
]

backgrounds = [pygame.transform.scale(pygame.image.load(path).convert(), (WIDTH, HEIGHT))
               for path in background_files]

current_bg_index = 0
next_bg_index = 1
bg_x = 0
bg_speed = 2

current_bg_index = 0
bg = backgrounds[current_bg_index]
bg_x = 0
bg_speed = 2
last_bg_switch_time = 0  # in milliseconds
bg_switch_interval = 20000  # 20 seconds


# --- NPC (Students) Setup ---
student_sheet = pygame.image.load("walking_student.png").convert_alpha()
STUDENT_FRAME_WIDTH = 90
STUDENT_FRAME_HEIGHT = student_sheet.get_height()

student_frames = [
    pygame.transform.scale(
        student_sheet.subsurface(
            (i * STUDENT_FRAME_WIDTH, 0, STUDENT_FRAME_WIDTH, STUDENT_FRAME_HEIGHT)
        ),
        (60, 80)
    )
    for i in range(4)
]

# --- Ghost Setup ---
ghost_img = pygame.image.load("ghost.png").convert_alpha()
ghost_img = pygame.transform.scale(ghost_img, (60, 50))

# --- Dynamic Entities ---
poops = []
npcs = []
ghosts = []

npc_spawn_timer = 0
ghost_spawn_timer = 0

# --- Fonts ---
poop_font = pygame.font.SysFont("Segoe UI Emoji", 20)

# ===============================================================
#                            FUNCTIONS
# ===============================================================

def spawn_npc():
    """Spawn a walking student NPC."""
    from_right = random.choice([True, False])
    npc_x = WIDTH + 60 if from_right else -60
    direction = -1 if from_right else 1

    npcs.append({
        "rect": pygame.Rect(npc_x, ground_y - 80, 60, 80),
        "dir": direction,
        "frame": random.randint(0, len(student_frames) - 1),
        "timer": 0,
        "speed": random.uniform(1.0, 2.5)
    })


def update_npcs():
    """Move and animate NPCs."""
    for npc in npcs:
        npc["rect"].x += npc["dir"] * npc["speed"]
        npc["timer"] += 1
        if npc["timer"] >= 8:
            npc["timer"] = 0
            npc["frame"] = (npc["frame"] + 1) % len(student_frames)
    # Remove off-screen NPCs
    npcs[:] = [n for n in npcs if -80 < n["rect"].x < WIDTH + 80]


def draw_npcs():
    for npc in npcs:
        frame_img = student_frames[npc["frame"]]
        if npc["dir"] == -1:
            frame_img = pygame.transform.flip(frame_img, True, False)
        screen.blit(frame_img, npc["rect"])


def spawn_ghost():
    """Spawn a ghost that floats across the screen."""
    ghost_y = random.randint(80, ground_y - 200)
    ghosts.append({
        "rect": pygame.Rect(WIDTH + 40, ghost_y, 60, 50),
        "speed": random.uniform(2.5, 4.5),
        "vy": random.choice([-1, 1]) * random.uniform(0.2, 0.6)
    })


def update_ghosts():
    """Update ghost positions and vertical floating."""
    for ghost in ghosts:
        ghost["rect"].x -= ghost["speed"]
        ghost["rect"].y += ghost["vy"]
        if ghost["rect"].top <= 50 or ghost["rect"].bottom >= ground_y - 120:
            ghost["vy"] *= -1
    ghosts[:] = [g for g in ghosts if g["rect"].right > 0]


def draw_ghosts():
    for ghost in ghosts:
        ghost_surface = ghost_img.copy()
        ghost_surface.set_alpha(180)
        screen.blit(ghost_surface, ghost["rect"])


def update_poops():
    """Apply gravity and move poop projectiles."""
    for p in poops:
        rect, vy = p
        vy += 0.4
        rect.y += vy
        p[1] = vy


def draw_poops():
    """Draw 💩 emoji projectiles."""
    for rect, _ in poops:
        poop_surface = poop_font.render("💩", True, WHITE)
        poop_rect = poop_surface.get_rect(center=rect.center)
        screen.blit(poop_surface, poop_rect)


def reset_game():
    """Restart after game over."""
    global velocity, score, npcs, poops, ghosts, game_active, bg_speed
    goose.center = (100, HEIGHT // 2)
    velocity = 0
    score = 0
    npcs.clear()
    poops.clear()
    ghosts.clear()
    bg_speed = 2
    game_active = True


# ===============================================================
#                         MAIN GAME LOOP
# ===============================================================

while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    velocity = -8
                    poop_rect = pygame.Rect(goose.x + 10, goose.y + 25, 10, 10)
                    poops.append([poop_rect, -4])
                else:
                    reset_game()

    # --- Game Logic ---
    if game_active:
        # Physics
        velocity += gravity
        goose.y += velocity * 0.6

        # Collisions with bounds
        if goose.bottom >= ground_y or goose.top <= 0:
            game_active = False

        # Collisions with ghosts
        for ghost in ghosts:
            if goose.colliderect(ghost["rect"]):
                game_active = False

        # Background scrolling
        # --- Scrolling Background with automatic transitions ---
        bg_x -= bg_speed

        # Draw current background
        screen.blit(backgrounds[current_bg_index], (bg_x, 0))

        # Draw the next background right after it
        screen.blit(backgrounds[next_bg_index], (bg_x + WIDTH, 0))

        # When current background fully moves off-screen...
        if bg_x <= -WIDTH:
            # Move to next background
            bg_x = 0
            current_bg_index = next_bg_index
            next_bg_index = (next_bg_index + 1) % len(backgrounds)


        # NPCs
        npc_spawn_timer += 1
        if npc_spawn_timer > 90:
            spawn_npc()
            npc_spawn_timer = 0
        update_npcs()

        # Ghosts
        ghost_spawn_timer += 1
        if ghost_spawn_timer > random.randint(80, 160):
            spawn_ghost()
            ghost_spawn_timer = 0
        update_ghosts()

        # Poops
        update_poops()

        # Poop vs NPC collision
        for p in poops[:]:
            for npc in npcs[:]:
                if p[0].colliderect(npc["rect"]):
                    poops.remove(p)
                    npcs.remove(npc)
                    score += 1
                    
                    break

        # Draw elements (no purple fill!)
        draw_npcs()
        draw_ghosts()
        draw_poops()

        # Animate Goose
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(goose_frames)
        rotated_goose = pygame.transform.rotate(goose_frames[current_frame], -velocity * 2)
        screen.blit(rotated_goose, goose)

        # Ground
        pygame.draw.rect(screen, BLACK, (0, ground_y, WIDTH, GROUND_HEIGHT))

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Speed increases with score
        bg_speed = 2 + (score * 0.1)

    else:
        # --- Game Over Screen ---
        screen.blit(bg, (0, 0))  # show the last background frame
        over_text = font.render("💀 Game Over 💩", True, ORANGE)
        screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        tip_text = font.render("Press SPACE to restart", True, WHITE)
        screen.blit(tip_text, tip_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))

    pygame.display.update()
    clock.tick(FPS)
