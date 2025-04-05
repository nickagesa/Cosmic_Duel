'''Cosmic Duel Game tutorial 2'''
# This code handles Restart screen, start game screen and player selection screen:
# 1. Restart screen: allows players to restart the game or return to the main menu (start_screen). 
#    call restart() function in handle_game_over()
#    have a way to check if the game is restarting or not in main() function
#    (if not restarting, show start screen first)
#    pass game mode to restart() function to keep the game mode same as the previous game
#    (if game mode is one player, the BOT will be used in the restart game)
# 2. Start screen: allows players to start the game or go to the options menu. call function in main() before the game loop
# 3. Options menu: allows players to view the controls and return to the main menu (start_screen). call function in start_screen() function
# 4. Player selection screen: allows players to select if they want to play against BOT or another player. call function in start_screen() function
#    Return the selected mode and pass it to a variable called game_mode in main() function which will be used to determine the game mode
#    The game mode should only be called when tyhe game is starting and not when the game is restarting
#    Put game conditions in the following places in main() function: 
#    a.) Above, CREATING YELLOW BULLET & PLAYER 2 SHOOTING
#    b.) when you call the bot_movement() function, add a condition to check if the game mode is one player or two players
#    c.)when you call the player_2_movement() function, add a condition to check if the game mode is one player or two players
import pygame 
import os 
import sys
import random 

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
BLACK = (0, 0, 0)

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
BACKGROUND_MUSIC = pygame.mixer.music.load(os.path.join('Assets', 'background_music.mp3'))
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

# COLLISION EVENTS #
YELLOW_HIT = pygame.USEREVENT + 1 # Event for yellow spaceship hit +1 is just a unique number showing 1st event
RED_HIT = pygame.USEREVENT + 2 # Event for red spaceship hit +2 is just a unique number showing 2nd event

# EVERYTHING IN THE GAME WINDOW #
def draw_window(bg_scroll,red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    # BACKGROUND SCROLLING
    GAME_WIN.blit(BACKGROUND, (bg_scroll, 0))
    GAME_WIN.blit(BACKGROUND, (bg_scroll + BACKGROUND.get_width(), 0))   
    
    #****DRAW HEALTH TEXT****#
    # Create/write health text
    red_health_text = FONT.render(f"Health: {red_health}", True, WHITE)  # text, anti-aliased, color
    yellow_health_text = FONT.render(f"Health: {yellow_health}", True, WHITE) # text, anti-aliased, color
    '''Anti-aliasing is a technique used to smooth out jagged edges in images, text, and graphics.'''
    # Draw health text
    GAME_WIN.blit(red_health_text, (SCREEN_WIDTH - red_health_text.get_width() - 10, 10))
    GAME_WIN.blit(yellow_health_text, (10, 10))

    # DRAW SPACESHIPS
    GAME_WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # Draw yellow spaceship
    GAME_WIN.blit(RED_SPACESHIP, (red.x, red.y))  # Draw red spaceshipip

     # DRAW SEPARATOR BORDER
    pygame.draw.rect(GAME_WIN, BLUE, BORDER) # space separator border (Game window, color, border rect object)

    # DRAW MULTIPLE BULLETS #
    for bullet in yellow_bullets:  # loop through yellow bullets
        pygame.draw.rect(GAME_WIN, YELLOW, bullet)  # draw yellow bullets (game window, color, bullet rect object)
    for bullet in red_bullets:  # loop through red bullets
        pygame.draw.rect(GAME_WIN, RED, bullet)  # draw red bullets
    
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


######################### BOT IMPLEMENTATION ####################################
def bot_movement(yellow, vertical_direction, horizontal_direction):
    # BOT MOVEMENT LOGIC (PREDICTABLE NOT RANDOM) # appears like its moving randomly
    # vertical (up and down)
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

    # Horizontal (left and right)
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
   
##############################################################################################

# *********** DETERMINE MOVEMENT OF BULLET AND  COLLISION DETECTION ****************** #
def handle_bullets(yellow_bullets, red_bullets, red, yellow):
    # Move yellow bullets
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED  # Move yellow bullets to the right (increase x position)
        # remove bullets when they go off screen to save memory
        if bullet.x > SCREEN_WIDTH:  # If bullet goes off screen
            yellow_bullets.remove(bullet)

            #Detect collision with red spaceship
        elif red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) # post event to red ship has been hit
            yellow_bullets.remove(bullet)

    # Move red bullets
    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED  # Move red bullets to the left (decrease x position)
        # remove bullets when they go off screen to save memory
        if bullet.x < 0:  # If bullet goes off screen
            red_bullets.remove(bullet)

            #Detect collision with yellow spaceship
        elif yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # post event to yellow ship has been hit
            red_bullets.remove(bullet)
#***********************************************************************************************#

############################## OPTIONS MENU #######################################################
def options_menu():
    # Create a rectangle object for the back button
    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 130, 200, 50)

    while True:
        # Background image (we will fill the screen with the background image)
        GAME_WIN.blit(BACKGROUND, (0, 0))

        # Create / Write Title text
        title_text = WINNER_FONT.render("Game Controls", True, WHITE)
        # Draw title text
        GAME_WIN.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//11))

        # Put controls text in a dictionary
        controls_text = {
            "Player 1 (Red)": {
                "Move": ["UP", "DOWN", "RIGHT", "LEFT"],
                "Shoot": "Right Ctrl"
            },
            "Player 2 (Yellow)": {
                "Move": ["W", "A", "S", "D"],
                "Shoot": "Left Ctrl"
            },
            
        }

        # Starting position for controls text
        y_offset = SCREEN_HEIGHT // 4  

        # Display player & controls text properly
        for player, actions in controls_text.items():
            # create player text
            player_text = FONT.render(player, True, WHITE) # text, anti-aliased, color
            # Draw player text
            GAME_WIN.blit(player_text, (SCREEN_WIDTH//2 - player_text.get_width()//2, y_offset))
            y_offset += 40  # Space below title

            # Controls text 
            for action, keys in actions.items():
                # create controls text
                action_text = FONT.render(f"{action}: {keys}", True, WHITE) # text, anti-aliased, color
                # Draw controls text
                GAME_WIN.blit(action_text, (SCREEN_WIDTH//2 - action_text.get_width()//2, y_offset))
                y_offset += 30  # Space between lines
            
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Highlight back button when hovered
        button_color = (255, 100, 100) if back_button.collidepoint((mouse_x, mouse_y)) else RED
        ## Draw back button rectangle object
        pygame.draw.rect(GAME_WIN, button_color, back_button)

        # Create button text
        back_text = BUTTON_FONT.render("Back", True, BLACK) # text, anti-aliased, color
        # Draw button text inside button rectangle
        GAME_WIN.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2, 
                             back_button.y + (back_button.height - back_text.get_height()) // 2))

        # Event handling for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse button is pressed
                # Check if the back button is clicked
                if back_button.collidepoint(event.pos):
                    MOUSE_CLICK_SOUND.play() # play sound effect
                    return  # Return to the start screen

        # Update display                
        pygame.display.update()
#####################################################################################

######################### START SCREEN ##############################################
def start_screen():
    # Create a rectangle objects for the start button and options button
    start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30, 200, 60) # (x,y,width,height)
    options_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 60)  

    # Background music settings (optional)
    pygame.mixer.music.play(-1) # -1 means loop the music indefinitely
    '''The background music will play during the start screen and then start playing again when the game starts.
    '''

    waiting = True # Flag to control the loop
    # Main loop for the start screen
    while waiting:
        # Background image (we will fill the screen with the background image)
        GAME_WIN.blit(BACKGROUND, (0, 0)) # image, (x,y) position
        
        # Create/ Write Title text
        title_text = WINNER_FONT.render("Cosmic Duel", True, WHITE)
        # Draw title text
        GAME_WIN.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos() # to handle mouse events

        # Highlight buttons when hovered
        start_color = (255, 100, 100) if start_button.collidepoint((mouse_x, mouse_y)) else RED
        options_color = (100, 100, 255) if options_button.collidepoint((mouse_x, mouse_y)) else (0, 150, 255)
        
        # Draw button rectangle objects
        pygame.draw.rect(GAME_WIN, start_color, start_button) 
        pygame.draw.rect(GAME_WIN, options_color, options_button)

        # Create button text 
        start_text = BUTTON_FONT.render("Start", True, BLACK) # text, anti-aliased, color
        options_text = BUTTON_FONT.render("Options", True, BLACK)

        # Draw button text inside button rectangles
        GAME_WIN.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, 
                               start_button.y + (start_button.height - start_text.get_height()) // 2))
        
        GAME_WIN.blit(options_text, (options_button.x + (options_button.width - options_text.get_width()) // 2, 
                                options_button.y + (options_button.height - options_text.get_height()) // 2))

        # CHECK FOR MOUSE CLICK EVENTS #
        for event in pygame.event.get():
            # Check if user wants to quit the game at the start screen (if you don't add this the game will freeze when you click the x button)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # exit the game 
            # Check if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse button is pressed
                # Check if the start button is clicked
                if start_button.collidepoint(event.pos): 
                    MOUSE_CLICK_SOUND.play() # play sound effect
                    return  # Start the game    
                                            
                    # return takes us to the main function because we are in a loop in the main function
                if options_button.collidepoint(event.pos):
                    MOUSE_CLICK_SOUND.play() # play sound effect
                    options_menu()  # Show the controls menu
                    
        # Update display
        pygame.display.update()
#######################################################################################

######################### PLAYERS SELECTION SCREEN ##############################################
def select_game_mode():
    
    # Create a rectangle objects for the one player button, two player button and back button
    one_player_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 80, 300, 60)
    two_player_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 20, 300, 60)
    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 130, 200, 50)

    selected_mode = None # Initialize selected mode to None

    while selected_mode is None: # Loop until a mode is selected
        GAME_WIN.blit(BACKGROUND, (0, 0)) # Fill the screen with the background image
        
        # Create / Write Title text
        title_text = WINNER_FONT.render("Select Game Mode", True, WHITE)
        # Draw title text
        GAME_WIN.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//8))
       
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Highlight buttons when hovered
        one_player_color = (0, 200, 0) if one_player_button.collidepoint((mouse_x, mouse_y)) else (0, 255, 0)
        two_player_color = (0, 100, 255) if two_player_button.collidepoint((mouse_x, mouse_y)) else (0, 150, 255)
        back_color = (255, 100, 100) if back_button.collidepoint((mouse_x, mouse_y)) else RED

        # Draw buttons rect
        pygame.draw.rect(GAME_WIN, one_player_color, one_player_button)
        pygame.draw.rect(GAME_WIN, two_player_color, two_player_button)
        pygame.draw.rect(GAME_WIN, back_color, back_button)

        # Button text
        one_player_text = BUTTON_FONT.render("One Player", True, BLACK)
        two_player_text = BUTTON_FONT.render("Two Players", True, BLACK)
        back_text = BUTTON_FONT.render("Back", True, BLACK)

        # Draw button text
        GAME_WIN.blit(one_player_text, (one_player_button.x + (one_player_button.width - one_player_text.get_width()) // 2,
                                   one_player_button.y + (one_player_button.height - one_player_text.get_height()) // 2))

        GAME_WIN.blit(two_player_text, (two_player_button.x + (two_player_button.width - two_player_text.get_width()) // 2,
                                   two_player_button.y + (two_player_button.height - two_player_text.get_height()) // 2))

        GAME_WIN.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2, 
                             back_button.y + (back_button.height - back_text.get_height()) // 2))
        
        # Event handling for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if user wants to quit the game at the select screen 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse button is pressed
                # Check if the one player button is clicked
                if one_player_button.collidepoint(event.pos):
                    selected_mode = "one_player"
                    MOUSE_CLICK_SOUND.play() # play sound effect

                # Check if the two player button is clicked
                if two_player_button.collidepoint(event.pos):
                    selected_mode = "two_players"
                    MOUSE_CLICK_SOUND.play() # play sound effect

                # Check if the back button is clicked
                if back_button.collidepoint(event.pos):
                    MOUSE_CLICK_SOUND.play() # play sound effect
                    start_screen() # Return to the start screen
                    
        
        # Update display
        pygame.display.update()

    return selected_mode # Return the selected mode ("one_player" or "two_players")
#######################################################################################

######################### RESTART SCREEN ##############################################
def restart_screen(game_mode):
    # Create a rectangle objects for the restart button and main menu button
    restart_button = pygame.Rect(SCREEN_WIDTH//2 - 105, SCREEN_HEIGHT//2 + 50, 220, 60) # (x,y,width,height)
    main_menu = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 120, 215, 70) # (x,y,width,height)
    
    button_selection = True
    while button_selection:
        mouse_x, mouse_y = pygame.mouse.get_pos() # get mouse position

        # Highlight buttons when hovered
        restart_color = (0, 100, 255) if restart_button.collidepoint((mouse_x, mouse_y)) else (0, 150, 255) # set color when mouse over button & when not over button
        main_menu_color = (255, 100, 100) if main_menu.collidepoint((mouse_x, mouse_y)) else RED
        '''How it works: set a color for the button when mouse is over it and another color when mouse is not over it
           collidepoint() checks if the mouse is over the button and returns True or False'''

        # Draw button rectangle objects
        pygame.draw.rect(GAME_WIN, restart_color, restart_button) # game window, color, button rect object
        pygame.draw.rect(GAME_WIN, main_menu_color, main_menu)
        
        # Write text on buttons
        restart_text = BUTTON_FONT.render("Restart", True, BLACK) # text, anti-aliased, color
        main_menu_text = BUTTON_FONT.render("Main Menu", True, BLACK)

        # Draw button text on the buttons rectangles
        GAME_WIN.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2, 
                                restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
        # (x,y) position of text on button rectangle
        # Center the text on the button rectangle
        
        GAME_WIN.blit(main_menu_text, (main_menu.x + (main_menu.width - main_menu_text.get_width()) // 2,
                                 main_menu.y + (main_menu.height - main_menu_text.get_height()) // 2))
         # (x,y) position of text on button rectangle
        # Center the text on the button rectangle

        # Update display
        pygame.display.update()

        # CHECK FOR MOUSE CLICK EVENTS #
        for event in pygame.event.get():
            # Check if user wants to quit the game at the restart screen (if you don't add this the game will freeze when you click the x button)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # exit the game
            # Check if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse button is pressed
                # Check if mouse is over restart button and perform actions
                if restart_button.collidepoint(event.pos):
                    MOUSE_CLICK_SOUND.play()
                    button_selection = False  # Restart game without going back to start menu
                    main(restart=True, game_mode=game_mode)  # Call main function to restart the game
                    # pass game mode to main function to keep the game mode same as the previous game
                # Check if mouse is over main menu button and perform actions    
                if main_menu.collidepoint(event.pos):
                    MOUSE_CLICK_SOUND.play()
                    button_selection = False
                    start_screen()  # Return to the main menu
###############################################################################################################

#### GAME OVER & STOP MUSIC ####
def handle_game_over(winner,game_mode):
    # Handle Game over Music #
    pygame.mixer.music.stop() # stop background music
    VICTORY_SOUND.play() # play victory sound effect

    # write winner text
    draw_text = WINNER_FONT.render(winner, True, WHITE)  # winner text, anti-aliased, color
    # Draw winner text
    GAME_WIN.blit(draw_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, SCREEN_HEIGHT//2 - draw_text.get_height()//2)) # text, (x,y) position
    
    pygame.display.update()  # Update the display
    #pygame.time.delay(5000)  # Delay for 5 seconds before restarting else the game will restart immediately

    # Call the restart screen instead of pausing for 5 seconds
    restart_screen(game_mode)

# MAIN GAME FUNCTION #
def main(restart=False, game_mode=None): 

    # CHECK IF GAME IS RESTARTING OR NOT
    if not restart:  # Only show start screen if NOT restarting the game
        start_screen() # Call the start screen function
        # select game mode if not restarting the game
        game_mode = select_game_mode() # Call the select game mode function (game_mode will be either "one_player" or "two_players")

    # If game_mode is still None (first launch), ask for selection else use the passed game_mode to restart the game
    if game_mode is None:
        game_mode = select_game_mode()
    
    # BACKGROUND SCROLLING VARIABLES #
    bg_speed = 0.5  # Speed of background scrolling
    bg_scroll = 0  # Background initial scroll position

    # DRAW SPACESHIP RECTANGLES (They wrap around the spaceship images) #
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # position of red spaceship 700,200,55,40 (x,y,width,height)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # position of yellow spaceship 100,200,55,40 (x,y,width,height)

    # BOT MOVEMENT VARIABLES #
    vertical_direction = "down"  # BOT starts moving downward
    horizontal_direction = "right"  # BOT starts moving right
    
    # LISTS TO STORE BULLETS #
    yellow_bullets = []  # list of yellow bullets
    red_bullets = []  # list of red bullets
    
    # INITIALIZE MUSIC #
    pygame.mixer.music.play(-1) # play background music in loop indefinitely

    # HEALTH VARIABLES #
    red_health = 100 # player starts with 100 health
    yellow_health = 100

    # GAME LOOP #
    game_running = True 
    while game_running: 
        # FPS Control
        clock.tick(FPS)

        # EVENT HANDLING #
        for event in pygame.event.get():  # loop through all events
            # QUIT
            if event.type == pygame.QUIT: 
                game_running = False 
                pygame.quit()  # exit the game
                sys.exit()  # exit the program

            # CAPTURE CTRL KEY PRESSES TO SHOOT BULLETS  & CREATE RECTANGLES FOR BULLETS #   
            if event.type == pygame.KEYDOWN:
                
                # CREATING RED BULLET & PLAYER 1 SHOOTING
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET: #if RCTRL key is pressed & number of bullets is less than max_bullet
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT) # create red bullet
                    red_bullets.append(bullet) # append bullet to red_bullets list
                    BULLET_FIRE_SOUND.play() # play sound effect
                    # you can only fire 5 bullets at a time if statement got that covered
                    # remove len(red_bullets) < MAX_BULLET if you want to fire unlimited bullets
                
                if game_mode == "two_players": # If game mode is two players
                    # CREATING YELLOW BULLET & PLAYER 2 SHOOTING
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET: #if LCTRL key is pressed & number of bullets is less than max_bullet
                        bullet = pygame.Rect(yellow.x + yellow. width, yellow.y + yellow.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                        yellow_bullets.append(bullet) # append bullet to yellow_bullets list
                        BULLET_FIRE_SOUND.play() # play sound effect
                        # you can only fire 5 bullets at a time if statement got that covered
                        # remove len(yellow_bullets) < MAX_BULLET if you want to fire unlimited bullets
                    
            # CAPTURE BULLET COLLISION EVENTS #
            if event.type == YELLOW_HIT: # receive event when yellow spaceship is hit
                yellow_health -= 10 # reduce health of yellow spaceship
                BULLET_HIT_SOUND.play() # play hit sound effect
                
            if event.type == RED_HIT: # receive event when red spaceship is hit
                red_health -= 10 # reduce health of red spaceship
                BULLET_HIT_SOUND.play() # play hit sound effect

        if game_mode == "one_player": # If game mode is one player
            #### CREATING YELLOW BULLETS & BOT SHOOTING RANDOMLY ########## 
            if random.randint(0, 100) < MAX_BULLET: # Randomly shoot
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                yellow_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
            
                
        # GET KEY PRESSES #
        keys = pygame.key.get_pressed() # important: used for movement, quiting, shooting, etc.
        
        # QUIT GAME UPON ESCAPE KEY PRESS
        if keys[pygame.K_ESCAPE]:  # if escape key is pressed
            game_running = False
        
        # DETERMINE WINNER #
        winner = ""    # Initialize winner text with empty string    
        if yellow_health <= 0:
            winner = "Red wins!"
        if red_health <= 0:
            winner = "Yellow wins!"
            
        # Display winner text and restart button
        if winner: # if winner is not empty
            handle_game_over(winner,game_mode) # call function to display winner
            main() # restart the game ,main resets all variables to default values
            # NOTICE: if you don't call main the game will launch again without resetting the variables and the game will be unplayable

        # CALL FUNTIONS TO MOVE PLAYERS #
        player_1_movement(keys, red)
        if game_mode == "one_player":
            vertical_direction, horizontal_direction = bot_movement(yellow, vertical_direction, horizontal_direction)
        elif game_mode == "two_players":
            player_2_movement(keys, yellow)

          # SCROLLING BACKGROUND # 
        bg_scroll -= bg_speed  # Decrease the scroll value to move the image left

        # Reset scroll when the entire image moves off-screen
        if abs(bg_scroll) >= BG_WIDTH:
            bg_scroll = 0  

        # SHOOTING #
        handle_bullets(yellow_bullets, red_bullets, red, yellow) # Move bullets and check for collisions
        draw_window(bg_scroll,red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)  # Call draw function 

    
if __name__ == "__main__": 
    main()  # call main function to start game
