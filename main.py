import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create Game Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brwal")

#set fps
clock = pygame.time.Clock()
FPS = 60

#deine colors
RED = (255, 0, 0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)

#define game variables 
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player score
round_over = False
R_over_cooldown = 2000

#Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE= 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music
#pygame.mixer.music.load("assets")

bg_image = pygame.image.load("assets/images/Background/background.jpg").convert_alpha()

#to load sprite sheet
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/icons/victory.png").convert_alpha()

#Define no of sprite animation each chracter has
WARRIOR_SPRITE_ANIMATION = [10, 8, 1, 7, 7, 3, 7]
WIZARD_SPRITE_ANIMATION = [8, 8, 1,8, 8, 3, 7]

#define Font
count_font = pygame.font.Font("assets/font/Turok.ttf", 80)
score_font = pygame.font.Font("assets/font/Turok.ttf", 80)

#define function for text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Function for Draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#function for heatlh bar
def draw_health_bar(health, x , y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34) )
    pygame.draw.rect(screen, RED, (x, y, 400, 30) )
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30) )
    


#fighter instance for both player    
fighter_1 = Fighter(1, 200, 310,False, WARRIOR_DATA, warrior_sheet, WARRIOR_SPRITE_ANIMATION)
fighter_2 = Fighter(2, 700, 310,True, WIZARD_DATA, wizard_sheet, WIZARD_SPRITE_ANIMATION)

run = True
while run:

    clock.tick(FPS)

    #Draw Background
    draw_bg()

    #Show Player Health
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    #countdown update
    if intro_count <= 0:
        #move fighter
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)
    
    

    #update fighters
    fighter_1.update()
    fighter_2.update()
    
    #Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            R_over_time = pygame.time.get_ticks()
            
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            R_over_time= pygame.time.get_ticks()
    else:
        #display victory image
        screen.blit(victory_img, (360, 150))    
        if pygame.time.get_ticks() - R_over_time > R_over_cooldown :
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310,False, WARRIOR_DATA, warrior_sheet, WARRIOR_SPRITE_ANIMATION)
            fighter_2 = Fighter(2, 700, 310,True, WIZARD_DATA, wizard_sheet, WIZARD_SPRITE_ANIMATION)



    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False  
    

    #update display 
    pygame.display.update()


#exit game
pygame.quit()
