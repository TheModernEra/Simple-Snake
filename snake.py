import pygame, random, time 

pygame.init() # initialize all the boring system graphics stuff we don't want to do

WIDTH = 640 # declare the WIDTH of the screen to 640
HEIGHT = 320 # declare the HEIGHT of the screen as 320

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set up the screen, WIDTH and HEIGHT used as a tuple
pygame.display.set_caption("Snake") # set the window's title as "Snake"

# declare a bunch of colors so we can use them later, numbers correspond to RGB codes
red = pygame.Color(255, 0, 0) 
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

clock = pygame.time.Clock() # clock lets time-based calculations be consistent on all computers regardless of speed

delta = 10 # used for randomness, movement speed and size of snake
snakePos = [100, 50] # head of the snake's x and y positition stored as a list
snakeBody = [[100, 50], [90, 50], [80, 50]] # nested list which stores all of the snake's body (including head). each item inside are x/y coordinates for each square of the snake's body
foodPos = [400, 50] # position of current food on screen as x/y coordinates
foodSpawn = True # boolean variable tracking if food is currently on screen, True if there is food on screen and False if not
direction = "RIGHT" # the current direction of the snake
changeto = "" # a holder variable for player input so we can verify that it's a valid move before applying it to the snake. you can't immediately swap from left to right in snake for example
score = 0 # player's current score

def gameOver(): # function to be run whenever we hit game over, puts up game over text and quits the game
    font = pygame.font.SysFont("Calibri", 72) # create font to be used for text
    text = font.render("Game Over", True, red) # create text to be displayed
    screen.blit(text, (150, HEIGHT/2)) # display text by sending to screen
    pygame.display.update() # update screen, you must update the display everytime something moves or appears
    time.sleep(2) # wait 2 seconds
    pygame.quit() # quit the game

def showScore(): # function to be run every frame that shows and updates the score display
    font = pygame.font.SysFont("Calibri", 32) # create font to be used for text
    text = font.render(f"Score: {score}", True, black) # create text to be displayed
    screen.blit(text, (80, 10)) # send text to the screen
    pygame.display.update() # update the display

running = True # boolean (True or False) variable that keeps track if the game is currently running

while running:  # while running is true, in other words run the following code on loop until the game stops running
    for event in pygame.event.get(): # search through all events currently activated in case there's one we want
        if event.type == pygame.QUIT: # if one of the active events is QUIT, turn running to false which will quit the game
            running = False
        elif event.type == pygame.KEYDOWN: # if one of the active events is KEYDOWN, a key is currently being pressed. now we search through the keys being pressed in case we need to do something
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # if the user presses RIGHT ARROW or D...
                changeto = "RIGHT" # change potential direction to RIGHT
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: # if the user presses LEFT ARROW or A...
                changeto = "LEFT" # change potential direction to LEFT
            if event.key == pygame.K_UP or event.key == pygame.K_w: # if the user presses UP ARROW or W...
                changeto = "UP" # change potential direction to UP
            if event.key == pygame.K_DOWN or event.key == pygame.K_s: # if the user presses DOWN ARROW or S...
                changeto = "DOWN" # change potential direction to DOWN

    # now we verify that the user has made a valid move
    if changeto == "RIGHT" and direction != "LEFT":
        direction = changeto
    if changeto == "LEFT" and direction != "RIGHT":
        direction = changeto
    if changeto == "UP" and direction != "DOWN":
        direction = changeto
    if changeto == "DOWN" and direction != "UP":
        direction = changeto

    # once movement has been checked, apply to snake itself
    if direction == "RIGHT":
        snakePos[0] += delta
    if direction == "LEFT":
        snakePos[0] -= delta
    if direction == "UP":
        snakePos[1] -= delta
    if direction == "DOWN":
        snakePos[1] += delta

    snakeBody.insert(0, list(snakePos)) # inserting the current location of the snake's head into the list in case we hit food
    if snakePos == foodPos:
        foodSpawn = False
        score += 1
    else:
        snakeBody.pop() # if we don't hit food, get rid of the extra square we just made

    # if food is off-screen, spawn it in a random position and turn foodSpawn to True, as food is now on-screen
    if foodSpawn == False:
        food_x = random.randrange(1, WIDTH // 10) * delta
        food_y = random.randrange(1, HEIGHT // 10) * delta
        foodPos = [food_x, food_y]
        foodSpawn = True

    screen.fill(white) # make bg white
    for square in snakeBody: # draw each square of the snake's body
        pygame.draw.rect(screen, green, pygame.Rect(square[0], square[1], delta, delta))
    pygame.draw.rect(screen, red, pygame.Rect(foodPos[0], foodPos[1], delta, delta)) # draw the food square

    # if the snake hits any of the screen borders, game over
    if snakePos[0] >= WIDTH or snakePos[0] < 0:
        gameOver()
    if snakePos[1] >= HEIGHT or snakePos[1] < 0:
        gameOver()

    # if snake's head hits a square in it's body, game over
    for square in snakeBody[1:]:
        if snakePos == square:
            gameOver()

    # do these every loop: update score, refresh entire screen so it shows the changes we made this loop, tick the clock 20 frames
    showScore()
    pygame.display.update()
    clock.tick(20)