import pygame
import requests
from io import BytesIO
import pandas as pd

# Load Pokémon data from CSV
pokemon_data = pd.read_csv("Pokemon Game\pokemon_data.csv")  # Replace with your CSV file
pokemon_list = pokemon_data["Name"].tolist()  # Extract Pokémon names into a list

# Pygame setup
pygame.init()

# Screen dimensions
X = 1280
Y = 720

# Set up display and font
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Pokemon Games")
clock = pygame.time.Clock()
running = True
font = pygame.font.Font('freesansbold.ttf', 32)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gray = (200, 200, 200)

# Current Pokémon index and user's team
current_pokemon_index = 0
user_team = []  # List to store user's selected Pokémon


# Fetch Pokémon image from PokeAPI
def fetch_pokemon_image(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            image_url = data["sprites"]["front_default"]
            image_response = requests.get(image_url)
            image_data = BytesIO(image_response.content)
            return pygame.image.load(image_data)
        else:
            print(f"Error: Could not fetch data for {pokemon_name}")
            return None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


# Draw button
def draw_button(text, x, y, width, height, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Highlight button if hovered
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, gray, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Render button text
    button_text = font.render(text, True, black)
    button_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, button_rect)


# Add Pokémon to team
def add_pokemon():
    global current_pokemon_index
    current_pokemon = pokemon_data.iloc[current_pokemon_index]["Name"]
    if current_pokemon not in user_team and len(user_team) < 3:
        user_team.append(current_pokemon)
    elif len(user_team) >= 3:
        print("Team is full!")


# Remove Pokémon from team
def remove_pokemon():
    global current_pokemon_index
    current_pokemon = pokemon_data.iloc[current_pokemon_index]["Name"]
    if current_pokemon in user_team:
        user_team.remove(current_pokemon)


# Render the title page and current Pokémon with stats
def create_title_page(pokemon_index):
    # Fill the screen with a background color
    screen.fill(white)

    # Get Pokémon data
    current_pokemon = pokemon_data.iloc[pokemon_index]
    pokemon_name = current_pokemon["Name"]
    pokemon_hp = current_pokemon["HP"]
    pokemon_attack = current_pokemon["Attack"]
    pokemon_defense = current_pokemon["Defense"]

    # Render the title text
    title_text = font.render('Choose Your Pokemon', True, black)
    title_rect = title_text.get_rect(center=(X // 2, Y // 8))
    screen.blit(title_text, title_rect)

    # Render Pokémon name
    name_text = font.render(f"Name: {pokemon_name}", True, black)
    name_rect = name_text.get_rect(topleft=(50, 200))
    screen.blit(name_text, name_rect)

    # Render Pokémon stats
    hp_text = font.render(f"HP: {pokemon_hp}", True, black)
    hp_rect = hp_text.get_rect(topleft=(50, 250))
    screen.blit(hp_text, hp_rect)

    attack_text = font.render(f"Attack: {pokemon_attack}", True, black)
    attack_rect = attack_text.get_rect(topleft=(50, 300))
    screen.blit(attack_text, attack_rect)

    defense_text = font.render(f"Defense: {pokemon_defense}", True, black)
    defense_rect = defense_text.get_rect(topleft=(50, 350))
    screen.blit(defense_text, defense_rect)

    # Fetch and display Pokémon image
    pokemon_image = fetch_pokemon_image(pokemon_name)
    if pokemon_image:
        pokemon_image = pygame.transform.scale(pokemon_image, (200, 200))
        screen.blit(pokemon_image, (X // 2 - 100, Y // 2 - 100))

    # Display the user's Pokémon team
    team_text = font.render("Your Team:", True, black)
    screen.blit(team_text, (900, 50))
    for i, team_member in enumerate(user_team):
        team_member_text = font.render(f"{i + 1}. {team_member}", True, black)
        screen.blit(team_member_text, (900, 100 + i * 40))

    # Draw Add and Remove buttons
    draw_button("Add", 200, 600, 100, 50, green, add_pokemon)
    draw_button("Remove", 400, 600, 150, 50, red, remove_pokemon)


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle navigation with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Next Pokémon
                current_pokemon_index += 1
                if current_pokemon_index >= len(pokemon_list):
                    current_pokemon_index = 0
            elif event.key == pygame.K_LEFT:  # Previous Pokémon
                current_pokemon_index -= 1
                if current_pokemon_index < 0:
                    current_pokemon_index = len(pokemon_list) - 1

    # Render the title page with the current Pokémon and stats
    create_title_page(current_pokemon_index)

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit FPS to 60
    clock.tick(60)

pygame.quit()
