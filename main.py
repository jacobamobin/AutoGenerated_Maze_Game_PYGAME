import replit
import time
import random
import pygame
from tkinter import *
from tkinter import messagebox

pygame.init()

replit.clear()

#Jacob Mobin
# April 4th 2022
#Maze game with autogenerating terrain

######################## NOTES TO TEACHER #####################
#The lasers have a cooldown, then they shoot one vertically and one horizantially, this sequence and the amount of time it takes might be influenced by replits lag, and might be a little bit faster when run locally, the laser should blink on either sides of the screen once quickly before clearing all blocks in that row

#i could not fix the Blit incorrect position error, the game still fully works, it just cant be reastarted without running the code again after a death

#If the game runs and the timer is low or the tutorial killed the time just reastart the game, for some reason replit is saving the amount of time and keeping it in bettween runs of the code


######################## GLOBAL VAIRABLES #####################
sq_sz = 25
#size of pixels
#IMAGE LOADING
imageD = pygame.image.load('FacingDown.png')  #Player
imageA = pygame.image.load('FacingLeft.png')  #2nd idle
imageB = pygame.image.load('FacingRight.png')  #main idle
imageC = pygame.image.load('FacingUpward.png')  #player facing up
imageE = pygame.image.load('Bomb.png')  #enemy one
imageF = pygame.image.load('Bomb2.png')  #enemy one opposite direction (UNUSED)
coinFrame1 = pygame.image.load('CoinFrame1.png')  #FRAMES 1-5 OF COIN ITEM
coinFrame2 = pygame.image.load('coinFrame2.png')  #WORKED, BUT LAGGED REPLIT TO MUCH WITH THE COIN ANIMATIONS
coinFrame3 = pygame.image.load('coinFrame3.png')
coinFrame4 = pygame.image.load('coinFrame4.png')
coinFrame5 = pygame.image.load('coinFrame5.png')  #USED COIN IMAGE
WallTexture = pygame.image.load('walltexture.png')
Laser = pygame.image.load('LaserEdge.png')  #Just in case

#colors
WallColor = (7, 80, 217)  #SETS COLORS FOR DIFFERENT ASSETS
AirColor = (247, 247, 247)
CoinColor = (247, 240, 15)
PlayerColor = (100, 15, 247)
EnemyColor = (255, 13, 21)
PortalColor = (255, 13, 219)
LaserColor = (255, 25, 5)

#VARIABLES
nA = 0
tutorial = 0
startTime = time.time()
lasercooldown = 1
GameState = 1
#Not using T/F becuase this game has more then "Alive" & "Dead" states
playerRow = 0  #PLAYER LOCATION IN ROOM
playerColumn = 0  #PLAYER LOCATION IN ROOM
playerRowB = 0  #PLAYER LOCATION IN CHECKERROOM
playerColumnB = 0  #PLAYER LOCATION IN CHECKERROOM
score = 0  #SCORE
lives = 3  #LIVES
level = 1  #LEVEL
CharachterState = 1
#The animation state of the player
LastDirection = 1
#Choses idle direction of the player
DamageFrame = False  #if the player should have invincibily frames
animLast = 10
#The last direction the player was looking
EnemyTick = 1
#This would (In a perfect not laggy replit world, show the direction the enemys are facing, 1 for right 2 for left)
CoinTick = 1
#This would (In a perfect not laggy replit world, show an animation for the coins, 1 for frame one 2 for 2 ect)
laserpowered = 0
lasercooldown = 0  #LASER CONTROLS FOR HORIZANTIAL AND VERTICAL LASERS
laserpoweredB = 0
lasercooldownB = 0
xtime = 120

#init windowed display
(width, height) = (sq_sz * 29, sq_sz * 30)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Jacobs Game')

room = [[
    "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
    "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"
],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ],
        [
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
            "X", "X", "X", "X"
        ]]
checkerroom = []

############################ METHOD DEFINING  ########################
#would write the room code
def printroom():
    for i in range(len(room)):
        for j in range(len(room[i])):
            print(room[i][j], end=" ")
        print()


#drawing the acctually game
def draw_window():
    global CharachterState
    global LastDirection
    global animLast
    global CoinTick
    global EnemyTick
    global lives
    global lasercooldown
    global nA
    global laserpowered
    global lasercooldown
    global laserpoweredB
    global lasercooldownB
    for row in range(len(room)):  #REPLACES LIST WITH IMAGES AND RECTS ON SCREEN
      for column in range(len(room[row])):
        rectangle = pygame.Rect(column * sq_sz, row * sq_sz, sq_sz, sq_sz)
        pygame.draw.rect(screen, AirColor, rectangle)
    for row in range(
            len(room)):  #REPLACES LIST WITH IMAGES AND RECTS ON SCREEN
        for column in range(len(room[row])):
            rectangle = pygame.Rect(column * sq_sz, row * sq_sz, sq_sz, sq_sz)
            if room[row][column] == "■":
                pygame.draw.rect(screen, WallColor, rectangle)
                screen.blit(WallTexture, (column * sq_sz, row * sq_sz))
            elif room[row][column] == "|":
                pygame.draw.rect(screen, PortalColor, rectangle)
            elif room[row][column] == "⎊":
                if EnemyTick == 1:
                    screen.blit(imageE, (column * sq_sz, row * sq_sz))
            elif room[row][column] == "$":
                if CoinTick == 1:
                    CoinTick += 1
                    screen.blit(coinFrame1, (column * sq_sz, row * sq_sz))
                elif CoinTick == 2:
                    CoinTick += 1
                    screen.blit(coinFrame2, (column * sq_sz, row * sq_sz))
                elif CoinTick == 3:
                    CoinTick += 1
                    screen.blit(coinFrame3, (column * sq_sz, row * sq_sz))
                elif CoinTick == 4:
                    CoinTick += 1
                    screen.blit(coinFrame4, (column * sq_sz, row * sq_sz))
                elif CoinTick == 5:
                    CoinTick = 1
                    screen.blit(coinFrame5, (column * sq_sz, row * sq_sz))
            elif room[row][column] == "P":
              pygame.draw.rect(screen, PlayerColor, rectangle)
              #ANIMATIONS
              if CharachterState == 1:  #RIGHT
                screen.blit(imageA, (column * sq_sz, row * sq_sz))
              elif CharachterState == 2:  #LEFT
                screen.blit(imageB, (column * sq_sz, row * sq_sz))
              elif CharachterState == 3:  #UP
                screen.blit(imageC, (column * sq_sz, row * sq_sz))
                if animLast == 1:
                  animLast = 10
                if animLast > 1:
                  animLast -= 1
                if animLast == 2:
                  if LastDirection == 1:
                    CharachterState = 1
                  if LastDirection == 2:
                    CharachterState = 2
              if CharachterState == 4:  #DOWN
                screen.blit(imageD, (column * sq_sz, row * sq_sz))
                if animLast == 1:
                  animLast = 10
                if animLast > 1:
                  animLast -= 1
                if animLast == 2:
                  if LastDirection == 1:
                    CharachterState = 1
                  if LastDirection == 2:
                    CharachterState = 2
                if room[row][column] == " ":  
                  pygame.draw.rect(screen, AirColor, rectangle)
    
            #HORIZANTIAL LASER AIR - LASER BLOCK
            if room[row][column] == "L": 
              if column == 0:
                set = 0

                while set != 29:   #REPLACES AIR COIN AND ENEMY WITH LASER
                  if room[nA][set] != "|" and room[nA][set] != "P":
                    room[nA][set] = "L"
                  if room[set][nA] == "P":
                    lives -= 1
                  rectangleB = pygame.Rect(nA * sq_sz, set * sq_sz, sq_sz, sq_sz)  #ADDS RED LASER
                  pygame.draw.rect(screen, LaserColor, rectangleB) 
                  set+=1
                time.sleep(0.1) #SO YOU CAN SEE LASER BETTER
              if room[row][column] == "L":         
                set = 0
                while set != 29:   #REPLACES LASER WITH AIR AFTER
                  if room[nA][set] == "L":
                    room[nA][set] = " "
                  set+=1
                  
            #VERTICAL LASER AIR - LASER BLOCK
            if room[row][column] == "L": 
              if row == 0:
                set = 0

                while set != 29:   #REPLACES AIR COIN AND ENEMY WITH LASER
                  if room[set][nA] != "|" and room[set][nA] != "P":
                    room[set][nA] = "L"
                  if room[set][nA] == "P":
                    lives -= 1
                  rectangleC = pygame.Rect(nA * sq_sz, set * sq_sz, sq_sz, sq_sz)  #ADDS RED LASER
                  pygame.draw.rect(screen, LaserColor, rectangleC) 
                  time.sleep(0.1) #SO YOU CAN SEE LASER BETTER
                  set+=1
                
              if room[row][column] == "L":             
                set = 0
                while set != 30:   #REPLACES LASER WITH AIR AFTER
                  if room[set][nA] == "L":
                    room[set][nA] = " "
                  set+=1
      
    #LASER ENEMY BASE CODE< DECIDING ELEVATION
    laserchance = random.randint(1, 5)  #LASER HEIGHT
    if laserchance == 1:
      laserpowered = 1
    if lasercooldown <= 0 and laserpowered == 1:
        nA = random.randint(0 , 29)
        room[nA][0] = "L"
        room[nA][29] = "L"
        LaserLeft = pygame.Rect(28 * sq_sz, nA * sq_sz, sq_sz, sq_sz)
        pygame.draw.rect(screen, LaserColor, LaserLeft)  
        LaserRight = pygame.Rect(0 * sq_sz, nA * sq_sz, sq_sz, sq_sz)
        pygame.draw.rect(screen, LaserColor, LaserRight) 
        lasercooldown = 30
        laserpowered = 0 
    laserchanceB = random.randint(1, 5)  #LASER HEIGHT
    if laserchanceB == 1:
      laserpoweredB = 1
    if lasercooldownB <= 0 and laserpoweredB == 1:
        nA = random.randint(0 , 29)
        room[0][nA] = "L"
        room[29][nA] = "L"
        LaserLeft = pygame.Rect(nA * sq_sz, 0 * sq_sz, sq_sz, sq_sz) #ADDS EDGE LASER INDICATORS
        pygame.draw.rect(screen, LaserColor, LaserLeft)  
        LaserRight = pygame.Rect(nA * sq_sz, 29 * sq_sz, sq_sz, sq_sz)
        pygame.draw.rect(screen, LaserColor, LaserRight)  
        lasercooldownB = 30
        laserpoweredB = 0 
    lasercooldown -= 1
    lasercooldownB -= 1

  
                
                    
                
        #gameDisplay.blit(bg, (0, 0))


#location defining  #DISPLAYS THE WINDO


def locate_player():
    global playerRow
    global playerColumn
    for row in range(len(room)):
        for column in range(len(room[row])):
            if room[row][column] == "P":
                playerRow = row
                playerColumn = column

#perform move controls 2D ONLY  #EXTRA LOCATOR FOR CHECKER ROOM UNUSED #UNUSED BC REPLIT IS BAD
def perform_move(direction):
    global CharachterState
    global LastDirection
    #move controls, sets block
    room[playerRow][playerColumn] = " "
    if direction == "right":
        room[playerRow][playerColumn + 1] = "P"
        CharachterState = 1  #RIGHT, FACINGRIGHT
        LastDirection = 1  #LAST DIR
    if direction == "left":
        room[playerRow][playerColumn - 1] = "P"
        CharachterState = 2  #LEFT, FACINGLEFT
        LastDirection = 2  #LAST DIR
    if direction == "up":
        room[playerRow - 1][playerColumn] = "P"
        CharachterState = 3  #UP, FACINGUPWARD
    if direction == "down":
        room[playerRow + 1][playerColumn] = "P"
        CharachterState = 4  #DOWN, FACINGDOWN
    return "B"


#GET OBJECT IN WAT   #THIS PERFORMS THE MOVE BY SETTING P
def get_object(direction):
    #GETS OBJECT
    if direction == "right" and playerColumn != 29:
        return room[playerRow][playerColumn + 1]
    if direction == "left" and playerColumn != 0:
        return room[playerRow][playerColumn - 1]
    if direction == "up" and playerRow != 0:
        return room[playerRow - 1][playerColumn]
    if direction == "down" and playerRow != 29:
        return room[playerRow + 1][playerColumn]
    return "luke"


#move defining   #THIS GETS THE OBJECT IN A CERTIAN DIRECTION
def move(direction):
    global score
    global GameState
    global lives
    global level
    global xtime
    locate_player()
    object = get_object(direction)
    if object == "$":
        score += 10
        perform_move(direction)
    if object == " ":
        perform_move(direction)
    if object == "⎊":
        score += 10
        lives -= 1
        if lives == 0:
            GameState = 0
            level = 1
        perform_move(direction)
    if object == "|":
        score += 10
        perform_move(direction)
        xtime = 60+time.time()
        GameState = 1
        level += 1


        #THIS HANDLES PLAYER MOVEMENT
def terrain():
    global xtime  
    #runs through every board spot
    xtime = 60+time.time()
    for i in range(len(room)):
        for j in range(len(room[i])):
            #randomises air and walls
            n = random.randint(1, 5)
            if n == 1:
                room[i][j] = "■"
            else:
                room[i][j] = " "
                #randomises coins
                n = random.randint(1, 10)
                if n == 1:
                    room[i][j] = "$"
                else:
                    room[i][j] = " "
                    #adds enemys
                    n = random.randint(1, 10)
                    if n == 1:
                        room[i][j] = "⎊"
                    else:
                        room[i][j] = " "
    #border FIX
    #replaces borders with blocks
    for i in range(len(room)):
        room[i][0] = "■"
    for i in range(len(room)):
        room[i][28] = "■"
    for j in range(len(room)):
        room[0][j] = "■"
    for j in range(len(room)):
        room[29][j] = "■"
    #WALL FIX
    #if there is BLOCK AIR BLOCK IN A ROW IT FILLS AIR WITH A BLOCK
    WallDepth = 0
    while WallDepth != 7:
        for i in range(len(room)):
            for j in range(len(room[i])):
                if room[i][j] == "■" and i < 28 and i > 3 and j > 3 and j < 28:
                    counter = 0
                    if room[i + 1][j] == " " or "⎊" or "$":
                        counter += 1
                        if room[i + 2][j] == "■":
                            counter += 1
                        if counter == 2:
                            room[i + 1][j] = "■"
                    counter = 0
                    if room[i - 1][j] == " " or "⎊" or "$":
                        counter += 1
                        if room[i - 2][j] == "■":
                            counter += 1
                        if counter == 2:
                            room[i - 1][j] = "■"
                    counter = 0
                    if room[i][j - 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i][j - 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i][j - 1] = "■"
                    counter = 0
                    if room[i][j - 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i][j - 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i][j - 1] = "■"
        for i in range(len(room)):
            for j in range(len(room[i])):
                #DIAGONALS
                # DOES THING ABOVE WITH WALLS BUT WITH DIAGONALS
                #Top right
                if room[i][j] == "■" and i < 28 and i > 3 and j > 3 and j < 28:
                    counter = 0
                    if room[i + 1][j + 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i + 2][j + 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i + 1][j + 1] = "■"
                # top LEFT
                    counter = 0
                    if room[i - 1][j - 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i - 2][j - 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i - 1][j - 1] = "■"
                #bottom right
                    counter = 0
                    if room[i - 1][j + 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i - 2][j + 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i - 1][j + 1] = "■"
                #bottom left
                    counter = 0
                    if room[i + 1][j - 1] == " " or "⎊" or "$":
                        counter += 1
                        if room[i + 2][j - 2] == "■":
                            counter += 1
                        if counter == 2:
                            room[i + 1][
                                j -
                                1] = "■"  #REPLACES BLOCK AIR BLOCK WITH BLOCK BLOCK BLOCK ON DIAGONAL ANGLES
        WallDepth += 1
    n = random.randint(1, 27)
    na = n
    n = random.randint(1, 27)
    nb = n
    room[na][nb] = "|"
    #spawn player in room
    room[15][15] = "P"
    room[16][15] = " "
    room[14][15] = " "
    room[15][14] = " "
    room[15][16] = " "
    room[17][15] = " "
    room[13][15] = " "
    room[15][13] = " "
    room[15][17] = " "



#runs basic code per frame
######################## GAME LOOP #####################

############################ START OF GAME LOOP  ########################
while GameState != 2:  #THIS CONSTANTLY RUNS THE GAME
    if tutorial == 0:
      Tk().wm_withdraw()
      messagebox.showinfo('Welcome To The Game','You are the purple amongus, and you move with the arrow keys. You must beat each randomly generated level in a short time frame or else you lose. Completing a level will add more time and reset you to 3 lives. Collect as many coins as you can along the way to increase score and avoid the Bombs as you will lose one of your lives, every few secconds a laser will blast through the screen from side to side so watch out, it will destroy all blocks in its path and take away a life. Get to the pink portal to complete the level!')
      fullTime = 30
      tutorial = 1
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MC', 30)
    if GameState == 1:
        terrain()
        lives = 3
        GameState = 0
        xtime += 60
    if lives == 0:
      timeText = myFont.render('OUT OF LIVES', False, (0,0,255))
      screen.blit(timeText,(10,height-sq_sz+10))
      GameState = 2
    #player controls
    events = pygame.event.get()
    move_ticker = 0
    #for event
    for event in events:  #GETTING PLAYER INPUTS
        keys = pygame.key.get_pressed()
        if move_ticker == 0:
            #Input Collection
            if keys[pygame.K_LEFT]:
                move_ticker = 10
                move("left")
            if keys[pygame.K_RIGHT]:
                move_ticker = 10
                move("right")
            if keys[pygame.K_UP]:
                move_ticker = 10
                move("up")
            if keys[pygame.K_DOWN]:
                move_ticker = 10
                move("down")
        #move ticker
        if move_ticker > 0:  #PLAYER TICKER (PLAYER DOSENT ZOOM)
            move_ticker -= 5
    #Handles laser boss
    draw_window()  #DISPLAYS ROOM IN GAME WINDOW
    #for i in range(len(room)):
        #for j in range(len(room[i])):
          #if room[i][j] == "L":
            #rectangle = pygame.Rect(j * sq_sz, i * sq_sz, sq_sz, sq_sz)
            #pygame.draw.rect(screen, LaserColor, rectangle)
    textSurface = myFont.render('Score: ' + str(score), False,
                                (0, 0, 255))
    screen.blit(textSurface, (10, 30 - sq_sz))
    textSurface = myFont.render('Lives: ' + str(lives), False,
                                (0, 0, 255))
    screen.blit(textSurface, (10, 50 - sq_sz))
    textSurface = myFont.render('Level: ' + str(level), False,
                                (0, 0, 255))
    screen.blit(textSurface, (10, 70 - sq_sz))
    fullTime = int((startTime+xtime)-time.time())
    showSec = fullTime%60
    timeText = myFont.render('time: '+ str(showSec).zfill(2), False, (0,0,255))
    screen.blit(timeText,(10,height-sq_sz+10))
    if showSec == 0:
      textSurface = myFont.render('OUT OF TIME', False, (0,0,255))
      screen.blit(textSurface,(10,height-sq_sz+10))
      GameState = 2
    #printroom()  #DISPLAYS ROOM IN CONSLE
    #replit.clear()
    #print("Score: " + str(score))
    #print("Lives: " + str(lives))
    pygame.display.update()

######################## END OF GAME #####################
print("Game Over")
textSurface = myFont.render('GAME OVER', False, (0,0,255))
screen.blit(textSurface, False, (10,10))
pygame.display.update()
time.sleep(2)
pygame.display.clear()
pygame.quit()

#testing
