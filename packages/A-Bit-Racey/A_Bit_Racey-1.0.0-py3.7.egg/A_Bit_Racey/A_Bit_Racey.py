def A_Bit_Racey():
    import pygame
    import time
    import random
    pygame.init()
    crash_sound = pygame.mixer.Sound('/home/pi/mu_code/PyGame/A_Bit_Racey/explosion.wav')
    pygame.mixer.music.load('/home/pi/mu_code/PyGame/A_Bit_Racey/UpbeatFunk.wav')
    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('A Bit Racey')
    black = (0,0,0)
    white = (255,255,255)
    red = (200, 0, 0)
    green = (0,200,0)
    bright_red = (255,0,0)
    bright_green = (0,255,0)
    block_color = (73,83,255)
    car_width = 72
    pause = True
    know = False

    clock = pygame.time.Clock()
    carImg = pygame.image.load('/home/pi/mu_code/PyGame/A_Bit_Racey/racecar.png')
    pygame.display.set_icon(carImg)

    def things_dodged(count):
        font = pygame.font.SysFont('comicsansms', 25)
        text = font.render('Dodged: '+str(count), True, black)
        gameDisplay.blit(text, (0,0))

    def things(thingx,thingy,thingw,thingh,color):
        pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

    def car(x,y):
        gameDisplay.blit(carImg,(x,y))

    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    def crash():
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(crash_sound)
        while 1 == 1 :
            largeText = pygame.font.SysFont('comicsansms',115)
            TextSurf, TextRect = text_objects('You Crashed', largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(TextSurf, TextRect)

            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                button('Play Again',150,450,100,50,green,bright_green,'game_loop')
                button('Quit', 550,450,100,50,red,bright_red,'quit')

                pygame.display.update()
                clock.tick(15)

    def button(msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
            if click[0] ==1 and action != None:
                if action == 'play':
                    game_loop()
                elif action == 'quit':
                    pygame.quit
                    quit()
                elif action == 'unpause':
                    unpause()
                elif action == 'game_loop':
                    game_loop()
                elif action == 'i':
                    i()
                elif action == 'game_intro':
                    game_intro()
        else:
            pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
        smallText = pygame.font.SysFont('comicsansms',20)
        textSurf, textRect = text_objects(msg,smallText)
        textRect.center = ((x+(w/2)),y +(h/2))
        gameDisplay.blit(textSurf,textRect)
    def unpause():
        global pause
        pygame.mixer.music.unpause()
        pause = False
    def paused():
        pygame.mixer.music.pause()
        largeText = pygame.font.SysFont('comicsansms',115)
        TextSurf, TextRect = text_objects('PAUSED', largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            button('Continue',150,450,100,50,green,bright_green,'unpause')
            button('Quit', 550,450,100,50,red,bright_red,'quit')

            pygame.display.update()
            clock.tick(15)


    def game_intro():
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            gameDisplay.fill(white)
            largeText = pygame.font.SysFont('comicsansms',115)
            smallText = pygame.font.SysFont('comicsansms',40)
            TextSurf, TextRect = text_objects('A Bit Racey', largeText)
            TextSurf2, TextRect2 = text_objects('Avoid hitting the sides or the blue rectangles', smallText)
            TextSurf3, TextRect3 = text_objects('Use the left and right arrow keys to steer', smallText)
            TextSurf4, TextRect4 = text_objects('Press "p" to pause', smallText)
            TextSurf5, TextRect5 = text_objects('Press "q" to quit', smallText)
            TextRect.center = (((display_width/2), (display_height/5)))
            TextRect2.center = (((display_width/2), (display_height/1.5)))
            TextRect3.center = (((display_width/2), (display_height/1.35)))
            TextRect4.center = (((display_width/2), (display_height/1.23)))
            TextRect5.center = (((display_width/2), (display_height/1.14)))
            gameDisplay.blit(TextSurf, TextRect)
            gameDisplay.blit(TextSurf2, TextRect2)
            gameDisplay.blit(TextSurf3, TextRect3)
            gameDisplay.blit(TextSurf4, TextRect4)
            gameDisplay.blit(TextSurf5, TextRect5)
            button('PLAY',120,300,100,50,green,bright_green,'play')
            button('QUIT',555,300,100,50,red,bright_red,'quit')
            pygame.display.update()
            clock.tick(15)


    def game_loop():
        pygame.mixer.music.play(-1)
        gameExit = False
        global pause
        x = (display_width*0.45)
        y = (display_height*0.8)
        x_change = 0
        thing_startx = random.randrange(0, display_width)
        thing_starty = -600
        thing_speed = 4
        thing_width = 100
        thing_height = 100
        dodged = 0

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    elif event.key == pygame.K_RIGHT:
                        x_change = 5
                    elif event.key == pygame.K_p:
                        pause = True
                        paused()
                    elif event.key == pygame.K_q:
                        pygame_quit()
                        quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

            x+= x_change
            gameDisplay.fill(white)
            things(thing_startx, thing_starty, thing_width, thing_height, block_color)
            thing_starty += thing_speed
            car(x,y)
            things_dodged(dodged)

            if x>display_width-car_width or x<0:
                crash()

            if thing_starty > display_height:
                thing_starty = 0 - thing_height
                thing_startx = random.randrange(0, display_width)
                dodged+= 1
                thing_speed += 0.3
                thing_width += (dodged*1.05)


            if y < thing_starty + thing_height:
                if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                    crash()
                    crash()


            pygame.display.update()
            clock.tick(60)

    game_intro()
    pygame.quit()
    quit()