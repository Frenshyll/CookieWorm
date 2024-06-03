import pygame
import random
import string
from pygame import mixer

# Initialize Pygame
pygame.init()

# List of valid words
VALID_WORDS = ['CAT', 'DOG', 'HOUSE', 'CAR', 'TREE', 'BALL', 'COOKIES', 'YUMMY', 'FLAVOR', 'MOUSE', 'DUCK', 'LOVE', 'GAME', 'LOSS', 'WIN', 'OKAY', 'WAFER', 'WATER', 'PROJECT', 'DATA', 'DOT', 'LOT', 'LIST', 'OBEY', 'ADD', 'HAT', 'HOT', 'KNOT', 'RUN', 'NIGHT', 'STORY', 'GET', 'GOT', 'POT', 'PAT', 'OPEN', 'POP', 'GOOD', 'GOAL', 'LUCK', 'LOAD', 'HUG', 'LOG', 'PET', 'PATH', 'SIN', 'DESK', 'BIG', 'SKIP', 'HANDS', 'VASE', 'STORE']

# Function to check if the word is valid
def is_valid_word(word):
    return word.upper() in VALID_WORDS

# Constants
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1005
BACKGROUND_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (173, 216, 230)  # Light blue highlight color
FONT_COLOR = (0, 0, 0)
CROSSED_OUT_COLOR = (255, 0, 0)  # Red color for crossed out words
FONT_SIZE = 30
GRID_SIZE = 10
CELL_SIZE = 90
GRID_OFFSET_X = 150  # New offset for the grid
GRID_OFFSET_Y = 50
WORD_BOX_POSITION = (SCREEN_WIDTH - 800, GRID_OFFSET_Y)
WORD_BOX_SIZE = (300, 910)

# Image paths
BACKGROUND_IMAGE_PATH = "bg.png"  # Path to the background image
IMAGE_PATHS = [
    "image_1.png",
    "image_2.png",
    "image_3.png",
    "image_5.png",
    "image_4.png"
]

# Load the background music
mixer.music.load("bgm file.mp3")
mixer.music.play(-1)

# Load sound effects for buttons
button_sound = mixer.Sound("click-button-140881 (1).mp3")
score_sound = mixer.Sound("correct-6033.mp3")
invalid_sound = mixer.Sound("wrong-buzzer-6268.mp3")

# Function to play button sound effect
def play_button_sound():
    button_sound.play()

# Function to play score sound effect
def play_score_sound():
    score_sound.play()

# Function to play invalid word sound effect
def play_invalid_sound():
    invalid_sound.play()

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookieworm")

# Font setup
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 50)
message_font = pygame.font.Font(None, 60)

class GameImage:
    def __init__(self, image_paths):
        self.images = [pygame.image.load(path) for path in image_paths]
        self.index = 0

    def update_index(self, score):
        # Update index based on score
        if score >= 60:
            self.index = 4  # Changed to 4 because there are 5 images (index 0 to 4)
        elif score >= 45:
            self.index = 3
        elif score >= 30:
            self.index = 2
        elif score >= 15:
            self.index = 1
        else:
            self.index = 0

    def draw(self, surface):
        image = self.images[self.index]
        image_rect = image.get_rect(center=(SCREEN_WIDTH - GRID_OFFSET_X - 2 * 50, SCREEN_HEIGHT // 2))
        surface.blit(image, image_rect)

# Function to render text on the screen
def draw_text(surface, text, position, color=FONT_COLOR):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Function to render the list of valid words on the screen
def draw_valid_words(surface, words, found_words, box_position, box_size):
    pygame.draw.rect(surface, FONT_COLOR, (*box_position, *box_size), 2)
    max_words_per_line = (len(words) + 25) // 26  # Maximum words per line, ensuring no more than 26 lines
    num_lines = min(len(words), 26)  # Maximum 26 lines
    for line in range(num_lines):
        for i in range(max_words_per_line):
            index = line * max_words_per_line + i
            if index < len(words):
                word = words[index]
                if word in found_words:
                    # Draw crossed out word
                    text_surface = font.render(word, True, CROSSED_OUT_COLOR)
                    text_rect = text_surface.get_rect(topleft=(box_position[0] + 10 + (i * 150), box_position[1] + 10 + line * (FONT_SIZE + 5)))
                    surface.blit(text_surface, text_rect.topleft)
                    # Draw line through the word
                    pygame.draw.line(surface, CROSSED_OUT_COLOR, text_rect.topleft, text_rect.bottomright, 2)
                    pygame.draw.line(surface, CROSSED_OUT_COLOR, (text_rect.left, text_rect.centery), (text_rect.right, text_rect.centery), 2)
                else:
                    draw_text(surface, word, (box_position[0] + 10 + (i * 150), box_position[1] + 10 + line * (FONT_SIZE + 5)))

# Function to generate a random grid of letters
def generate_grid(size):
    grid = []
    for _ in range(size):
        row = [random.choice(string.ascii_uppercase) for _ in range(size)]
        grid.append(row)
    return grid

# Function to replace selected cells with new random letters
def replace_selected_cells(grid, selected_cells):
    for (y, x) in selected_cells:
        grid[y][x] = random.choice(string.ascii_uppercase)

# Function to draw the grid with highlights for selected cells
def draw_grid(surface, grid, selected_cells):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (y, x) in selected_cells:
                pygame.draw.rect(surface, HIGHLIGHT_COLOR, rect)
            pygame.draw.rect(surface, FONT_COLOR, rect, 2)
            draw_text(surface, cell, (rect.x + 30, rect.y + 30))

# Function to draw a button
def draw_button(surface, text, position, size, color=(0, 0, 0), hover_color=(100, 100, 100)):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(position, size)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(surface, hover_color, button_rect, border_radius=10)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(surface, color, button_rect, border_radius=10)

    button_text = button_font.render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    surface.blit(button_text, text_rect)

    return False

# Function to draw a modal message box with design
def draw_message_box(surface, message, position, size, color=(0, 0, 0), bg_color=(255, 255, 255), border_color=(0, 255, 0), decoration_color=(255, 215, 0)):
    box_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, bg_color, box_rect)
    pygame.draw.rect(surface, border_color, box_rect, 5)

   
    text_surface = message_font.render(message, True, color)
    text_rect = text_surface.get_rect(center=box_rect.center)
    surface.blit(text_surface, text_rect)

# Main Menu Loop
def main_menu(background_image_path):
    background_image = pygame.image.load(background_image_path)
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background_image, (0, 0))

        # Draw play button
        if draw_button(screen, "Play", (170, SCREEN_HEIGHT // 2 - 100), (300, 100), color=(0, 128, 0), hover_color=(0, 255, 0)):
            play_button_sound()  # Play button sound effect
            menu_running = False
            game_loop("bg5.png")  # Pass game background image path

        # Draw quit button
        if draw_button(screen, "Quit", (170, SCREEN_HEIGHT // 2 + 20), (300, 100), color=(255, 0, 0), hover_color=(255, 100, 100)):
            play_button_sound()  # Play button sound effect
            pygame.quit()
            quit()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Game Loop
def game_loop(background_image_path):
    background_image = pygame.image.load(background_image_path)
    game_image = GameImage(IMAGE_PATHS)
    clock = pygame.time.Clock()
    running = True
    score = 0
    current_word = ""
    selected_cells = []
    found_words = set()
    grid = generate_grid(GRID_SIZE)
    congratulations_displayed = False  # To track if the congratulation message has been displayed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse click events to select letters from the grid
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                grid_y = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    cell = (grid_y, grid_x)
                    if cell not in selected_cells:
                        selected_cells.append(cell)
                        current_word += grid[grid_y][grid_x]

            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and selected_cells:
                    last_cell = selected_cells.pop()
                    current_word = current_word[:-1]
                elif event.key == pygame.K_RETURN:
                    if is_valid_word(current_word):
                        score += 5
                        game_image.update_index(score)
                        replace_selected_cells(grid, selected_cells)
                        found_words.add(current_word.upper())
                        current_word = ""
                        selected_cells = []
                        play_score_sound()  # Play score sound effect
                    else:
                        play_invalid_sound()  # Play invalid word sound effect

                # Add back button functionality
                elif event.key == pygame.K_ESCAPE:
                    main_menu("bg.png")  # Return to the main menu

        screen.blit(background_image, (0, 0))

        # Draw the grid
        draw_grid(screen, grid, selected_cells)
        game_image.draw(screen)

        # Update the position of the text for score and word
        draw_text(screen, f"Score: {score}", (GRID_OFFSET_X - 140, GRID_OFFSET_Y))
        draw_text(screen, f"Word: {current_word}", (GRID_OFFSET_X - 140, GRID_OFFSET_Y + FONT_SIZE + 10))

        # Draw the list of valid words on the right side of the screen
        draw_valid_words(screen, VALID_WORDS, found_words, WORD_BOX_POSITION, WORD_BOX_SIZE)

        # Check if the player has reached the highest score and display the congratulations message
        if score >= 65 and not congratulations_displayed:
            draw_message_box(screen, "Congratulations! You reached the highest score!",
                             (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 100), (1000, 200))
            pygame.display.flip()
            pygame.time.wait(5000)  # Display the message for 3 seconds
            congratulations_displayed = True

        # Draw back button
        if draw_button(screen, "Back", (SCREEN_WIDTH - 150, 20), (120, 50), color=(255, 0, 0), hover_color=(255, 100, 100)):
            main_menu("bg.png")  # Return to the main menu
            running = False

        # Check if the last image has been displayed and end the game
        if game_image.index == len(game_image.images) - 1:
            draw_message_box(screen, "Congratulations! You've completed the game!",
                             (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 100), (1000, 200))
            pygame.display.flip()
            pygame.time.wait(5000)  # Display the message for 3 seconds
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_menu("bg.png")  # Use main menu background image
