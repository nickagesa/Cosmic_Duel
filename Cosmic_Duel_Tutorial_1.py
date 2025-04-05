'''Cosmic Duel Game tutorial start here:'''
# This code handles:
# 1. Importing necessary libraries and modules.
# 2. Initializing Pygame and setting up the game window.
# 3. Defining constants, variables and loading images and sounds.
# 4. Scrolling the background and drawing the game window.
# 5. It also includes player movements and BOT movement functions.
# 6. Implementing the main game loop to handle events, quit and movement.

# Import necessary libraries
import pygame # pygame library for game development
import os # os module for file path handling
import sys # sys for exiting the program


# Initialize pygame
pygame.init()  # all imported pygame modules
pygame.font.init()  # font module
pygame.mixer.init()  # mixer module for sound

# Game window 
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500  # Width and height
GAME_WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # set window size
pygame.display.set_caption("Cosmic Duel")  # set title window 

# Load Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
BACKGROUND = pygame.image.load(os.path.join('Assets', 'space_background.jpg'))

# Image dimensions
BG_WIDTH, BG_HEIGHT = 900, 500 # Background dimensions
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  

# Transform & Rotate Images
BACKGROUND = pygame.transform.scale(BACKGROUND, (BG_WIDTH, BG_HEIGHT))  # Scale background to fit screen
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# SPACE SPEPARATOR BORDER #
BORDER = pygame.Rect(SCREEN_WIDTH//2 - 5, 0, 2, SCREEN_HEIGHT) # rect object for border (x,y,width,height)

# Fonts
FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)
BUTTON_FONT = pygame.font.SysFont('comicsans', 40)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Frame Rate
clock = pygame.time.Clock()  # clock object to control frame rate
FPS = 60  # set frame rate

# Bullet settings
MAX_BULLET = 5
BULLET_SPEED = 7 
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Bullet_Fire.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Bullet_Hit.mp3'))
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

# OTHER SOUNDS #
BACKGROUND_SOUND = pygame.mixer.music.load(os.path.join('Assets', 'background_music.mp3'))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Victory_Sound_Effect.mp3'))
MOUSE_CLICK_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Mouse_click_sound_effect.mp3'))

# SET SOUNDS VOLUME #
pygame.mixer.music.set_volume(0.1) # Set background music to 10% of max volume
BULLET_FIRE_SOUND.set_volume(0.03) # Set bullet fire sound to 10% of max volume
BULLET_HIT_SOUND.set_volume(0.03)   # Set bullet hit sound to 10% of max volume
VICTORY_SOUND.set_volume(0.03)  # Set victory sound to 10% of max volume
MOUSE_CLICK_SOUND.set_volume(0.2)  # Set mouse click sound to 20% of max volume

# Speeds
BOT_VEL = 2  # BOT movement speed (lower for smoother movement)
VEL = 5  # Spaceship movement speed (lower for smoother movement)


# EVERYTHING IN THE GAME WINDOW #
def draw_window(bg_scroll,red, yellow):
    # BACKGROUND SCROLLING
    GAME_WIN.blit(BACKGROUND, (bg_scroll, 0)) # Draw the background image at the current scroll position (x,y)
    GAME_WIN.blit(BACKGROUND, (bg_scroll + BACKGROUND.get_width(), 0))  # Draw the background image again at the right side
    # This creates the scrolling effect by drawing the image twice, once at the current scroll position and once at the right side of the screen. 
    
    # DRAW SPACESHIPS
    GAME_WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # Draw yellow spaceship
    GAME_WIN.blit(RED_SPACESHIP, (red.x, red.y))  # Draw red spaceshipip

     # DRAW SEPARATOR BORDER
    pygame.draw.rect(GAME_WIN, BLUE, BORDER) # space separator border
    
    pygame.display.update()  # Update the display


# MOVEMENT FUNCTIONS #
def player_1_movement(keys, red):
    # Player 1 movement
        if keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # move left
            red.x -= VEL # decrease x position
        if keys[pygame.K_RIGHT] and red.x + VEL + red.width < SCREEN_WIDTH: # move right
            red.x += VEL # increase x position
        if keys[pygame.K_UP] and red.y - VEL > 0:   # move up
            red.y -= VEL # decrease y position
        if keys[pygame.K_DOWN] and red.y + VEL + red.height < SCREEN_HEIGHT - 10:   # move down
            red.y += VEL # increase y position
'''
def player_2_movement(keys, yellow):
    # Player 2 movement
        if keys[pygame.K_a] and yellow.x - VEL > 0: # move left
            yellow.x -= VEL # decrease x position
        if keys[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # move right
            yellow.x += VEL # increase x position
        if keys[pygame.K_w] and yellow.y - VEL > 0: # move up
            yellow.y -= VEL # decrease y position
        if keys[pygame.K_s] and yellow.y + VEL + yellow.height < SCREEN_HEIGHT - 10: # move down
            yellow.y += VEL # increase y position
'''
#'''
def bot_movement(yellow, vertical_direction, horizontal_direction):
    # BOT MOVEMENT LOGIC (PREDICTABLE NOT RANDOM) # appears like its moving randomly
    # BOT movement vertical (up and down)
    if vertical_direction == "down":
        if yellow.y + BOT_VEL + yellow.height < SCREEN_HEIGHT - 10:
            yellow.y += BOT_VEL # increase y position
        else:
            vertical_direction = "up"
    else:
        if yellow.y - BOT_VEL > 0:
            yellow.y -= BOT_VEL # decrease y position
        else:
            vertical_direction = "down"

    # BOT movement Horizontal (left and right)
    if horizontal_direction == "right":
        if yellow.x + BOT_VEL + yellow.width < SCREEN_WIDTH // 2 - 10:  # Stay on the left side
            yellow.x += BOT_VEL # increase x position
        else:
            horizontal_direction = "left"
    else:
        if yellow.x - BOT_VEL > 0:
            yellow.x -= BOT_VEL # decrease x position
        else:
            horizontal_direction = "right"

    return vertical_direction, horizontal_direction
#'''

# MAIN FUNCTION #
def main(): 
    # BACKGROUND SCROLLING VARIABLES #
    bg_speed = 0.5  # Speed of background scrolling
    bg_scroll = 0  # Background initial scroll position

    # DRAW SPACESHIP RECTANGLES (They wrap around the spaceship images) #
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # position of red spaceship 700,200,55,40 (x,y,width,height)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # position of yellow spaceship 100,200,55,40 (x,y,width,height)

    # BOT MOVEMENT VARIABLES #
    vertical_direction = "down"  # BOT starts moving downward
    horizontal_direction = "right"  # BOT starts moving right

    # GAME LOOP #
    game_running = True 
    while game_running: 
        # FPS Control
        clock.tick(FPS)
       
        # EVENT HANDLING#
        for event in pygame.event.get():  # loop through all events
            # QUIT
            if event.type == pygame.QUIT: 
                game_running = False 
                pygame.quit()  # exit the game
                sys.exit()  # exit the program
        
        # GET KEY PRESSES #
        keys = pygame.key.get_pressed() # important used for movement, quiting, shooting, etc.
        
        # QUIT GAME UPON ESCAPE KEY PRESS #
        if keys[pygame.K_ESCAPE]:  # if escape key is pressed
            game_running = False

        # CALL FUNTIONS TO MOVE PLAYERS #
        player_1_movement(keys, red)
        vertical_direction, horizontal_direction = bot_movement(yellow, vertical_direction, horizontal_direction)
        #player_2_movement(keys, yellow)

        # SCROLLING BACKGROUND # 
        bg_scroll -= bg_speed  # Decrease the scroll value to move the image left

        # Reset scroll when the entire image moves off-screen
        if abs(bg_scroll) >= BG_WIDTH:
            bg_scroll = 0  

        draw_window(bg_scroll, red, yellow)  # Call draw function 

    
if __name__ == "__main__": 
    main()  # call main function to start game
