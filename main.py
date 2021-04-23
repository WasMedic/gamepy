import pygame
from pygame import mixer
import random
import math

pygame.init()

# this opens the window and sets resolution
screen = pygame.display.set_mode((1280,720))

#title 
pygame.display.set_caption("Aids Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
playerSprite = pygame.image.load("player.png")
playerX = 576
playerY = 650
playerX_change = 0
playerY_change = 0

#alien
alienSprite = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alienSprite.append(pygame.image.load("enemy.png")) 
    alienX.append(random.randint(0, 1216)) 
    alienY.append(random.randint(0, 400)) 
    alienX_change.append(0.3) 
    alienY_change.append(40)
#bullet
# Ready - has not been fired
# fire - bullet has been fire
bulletSprite = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 650
bulletY_change = 0.6
bullet_state = "ready"


background = pygame.image.load("background.png")
clock = pygame.time.Clock()
fps = clock.tick(60)

#score
score_value = 0
font = pygame.font.Font('retro.ttf', 32)
textX = 10
textY = 10

#gameover text
over_font =  pygame.font.Font('retro.ttf', 64)

#sound
mixer.music.load("music.mp3")
mixer.music.play(-1)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameover_text():
    over_text = font.render("GAMEOVER! You Scored " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (300, 300))
    mixer.music.pause

def player(x, y):
    screen.blit(playerSprite, (x,y))

def alien(x, y, i):
    screen.blit(alienSprite[i], (x,y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletSprite, (x + 16, y + 10))

def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


    

#this the game 
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #inputs
            if event.key == pygame.K_a: 
                # moving left
               playerX_change = -0.4
            if event.key == pygame.K_d:
                # moving right
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                 # firing bullet
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

        
    # the movement and border
    playerX += playerX_change * fps
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1216:
        playerX = 1216

    #ALIENS
    for i in range(num_of_aliens):

        #gameover text
        if alienY[i] >= 560:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            gameover_text()
            break
        
        alienX[i] += alienX_change[i] * fps
        
        if alienX[i] >= 1216:
            alienX_change[i] = -0.3
            alienY[i] += alienY_change[i]
        elif alienX[i] <= 0:
            alienX_change[i] = 0.3
            alienY[i] += alienY_change[i]
    
    #collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY) 
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 1216)
            alienY[i] = random.randint(0, 100)
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
        
        alien(alienX[i], alienY[i], i)
        
    
# bullet movement
    if bulletY <= 0:
        bulletY = 650
        bullet_state = "ready"


    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change * fps



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

