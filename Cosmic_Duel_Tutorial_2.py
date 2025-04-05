'''Cosmic Duel Game tutorial 2'''
# This code handles Bullets and shooting mechanics, collision detection, health system, and game over screen:
# 1. Create bullet list for each player. (yellow_bullets and red_bullets)
# 2. Draw multiple bullets using a for loop in draw_window() function.
# 3. Create a bullet object using pygame.Rect() and append it to the respective bullet list main() function.
# 4. Create a function handle_bullets () to move the bullets and detect collision
#     Move bullets using bullet.x += BULLET_VEL for yellow and bullet.x -= BULLET_VEL for red.
#     Create global events for yellow and red hit using pygame.USEREVENT + 1 and pygame.USEREVENT + 2.
#     Detect collision using colliderect() method and post an event to indicate a hit.
#     Remove the bullet from the list after it hits the spaceship or goes off screen.
# 5. Create new Variables in main() for health (red_health & yellow_health)
# 6. Reduce health of the spaceship when hit by a bullet. 
# 7. initialize music and sound effects for shooting and hitting main().
# 8. Draw health text in the draw_window() function using FONT.render() and blit() method.
# 9. Determine the winner based on health and display the winner text.
# 10. Create a function handle_game_over() to display the winner and restart the game.
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
BOT_VEL = 2  # AI movement speed (lower for smoother movement)
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
#'''
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

#### GAME OVER & STOP MUSIC ####
def handle_game_over(winner):
    # Handle Game over Music #
    pygame.mixer.music.stop() # stop background music
    VICTORY_SOUND.play() # play victory sound effect

    # draw winner
    draw_text = WINNER_FONT.render(winner, True, WHITE)  # winner text, anti-aliased, color
    GAME_WIN.blit(draw_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, SCREEN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()  # Update the display
    pygame.time.delay(5000)  # Delay for 5 seconds before restarting else the game will restart immediately

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
    
    # LISTS TO STORE BULLETS #
    yellow_bullets = []  # list of yellow bullets
    red_bullets = []  # list of red bullets
    
    # INITIALIZE MUSIC #
    pygame.mixer.music.play(-1) # play background music in loop
    
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
                '''
                # CREATING YELLOW BULLET & PLAYER 2 SHOOTING
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET: #if LCTRL key is pressed & number of bullets is less than max_bullet
                    bullet = pygame.Rect(yellow.x + yellow. width, yellow.y + yellow.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet) # append bullet to yellow_bullets list
                    BULLET_FIRE_SOUND.play() # play sound effect
                    # you can only fire 5 bullets at a time if statement got that covered
                    # remove len(yellow_bullets) < MAX_BULLET if you want to fire unlimited bullets
                '''
            # CAPTURE BULLET COLLISION EVENTS #
            if event.type == YELLOW_HIT: # receive event when yellow spaceship is hit
                yellow_health -= 10 # reduce health of yellow spaceship
                BULLET_HIT_SOUND.play() # play hit sound effect
                
            if event.type == RED_HIT: # receive event when red spaceship is hit
                red_health -= 10 # reduce health of red spaceship
                BULLET_HIT_SOUND.play() # play hit sound effect
        #'''
        #### CREATING YELLOW BULLETS & BOT SHOOTING RANDOMLY ########## 
        if random.randint(0, 100) < MAX_BULLET: # Randomly shoot
            bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
            yellow_bullets.append(bullet)
            BULLET_FIRE_SOUND.play()
        #'''
                
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
            handle_game_over(winner) # call function to display winner
            main() # restart the game ,main resets all variables to default values
            # NOTICE: if you don't call main the game will launch again without resetting the variables and the game will be unplayable

        # CALL FUNTIONS TO MOVE PLAYERS #
        player_1_movement(keys, red)
        vertical_direction, horizontal_direction = bot_movement(yellow, vertical_direction, horizontal_direction)
        #player_2_movement(keys, yellow)

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
