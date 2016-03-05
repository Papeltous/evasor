import pygame, random, sys, time
from pygame.locals import *

print('INSTRUCCIONES')
print()
print('En este juego tu eres el personaje blanco. Te has de mover con las flechas o con la teclas: A, S, D, W')
print()
print('En este juego has de ir esquivando las cosas verdes que van cayendo por la pantalla y te has de ir comiendo las cerezas.')
print()
print('Cada cereza que te comas te dara 100 puntos extra.')
print()
print('Cada cereza te ira ir mas lento y cada 5 cerezas los enemigos iran un poco mas rapidos')
print()
print('Hay tres niveles diferenes de dificultad')
print()
input()

nivel = 1

salida_baddie = 20
salida_cherry = 25
salida_pocion = 500
velocidad_maxima_baddie = 2
velocidad_minima_baddie = 1

WINDOWWIDTH = 1250
WINDOWHEIGHT = 750

TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)

FPS = 40

BADDIEMINSIZE = 20
BADDIEMAXSIZE = 40
BADDIEMINSPEED = velocidad_minima_baddie
BADDIEMAXSPEED = velocidad_maxima_baddie
ADDNEWBADDIERATE = salida_baddie

PLAYERSIZE = 40

LIVES = 3

to_reset_BADDIEMINSPEED = BADDIEMINSPEED
to_reset_BADDIEMAXSPEED = BADDIEMAXSPEED

CHERRYMINSIZE = 20
CHERRYMAXSIZE = 40
CHERRYMINSPEED = 1
CHERRYMAXSPEED = 4

POCIONMINSIZE = 20
POCIONMAXSIZE = 21
POCIONMINSPEED = 1
POCIONMAXSPEED = 5

PLAYERMOVERATE = float(5)
PLAYERMOVERATE_to_reset = PLAYERMOVERATE

una_vez = True

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

#----------
# BADDIES
#----------

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

#---------
# CHERRY
#---------

def playerHasHitCherry(playerRect, cherry):
    for c in cherry:
        if playerRect.colliderect(c['rect']):
            return c
    return False

def playerHasHitPocion(playerRect, pocionSize):
    for p in pocion:
        if playerRect.colliderect(p['rect']):
            return p
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Esquivacaras')
pygame.mouse.set_visible(False)


# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
player_Image = pygame.image.load('player.png')
player_actual = player_Image
playerRect =  player_Image.get_rect()

player_Image2 = pygame.image.load('player2.png')
player_Image3 = pygame.image.load('player3.png')



#player2_Image = pygame.image.load('player.png')
#player2_Rect = player2_Image.get_rect()

baddieImage = pygame.image.load('baddie.png')

cherryImage = pygame.image.load('cherry1.png')
cherryRect = cherryImage.get_rect()


pocionImage = pygame.image.load('pocion.png')

# show the "Start" screen
drawText('Evasivo y gloton.', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Aprieta una tecla para empezar.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # set up the start of the game
    baddies = []
    cherry = []
    pocion = []
    cherries = 0
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    reversecheat = slowcheat = False
    baddieAddCounter = 0
    cherryAddCounter = 0
    pocionAddCounter = 0
    paso_por_aqui = FPS
    contador = 0

    old_centerx = playerRect.centerx
    old_centery = playerRect.centery

    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        if nivel == 1:
            salida_baddie = 20
            salida_cherry = 25
            salida_pocion = 500
            velocidad_maxima_baddie = 2
            velocidad_minima_baddie = 1
            nivel2 = False
            nivel3 = False

        if nivel == 2 and nivel2 == False:
            salida_baddie = 15
            salida_cherry = 20
            salida_pocion = 750
            velocidad_maxima_baddie = 3
            velocidad_minima_baddie = 2
            nivel2 = True
            nivel3 = False
            

        if nivel == 3 and nivel3 == False:
            salida_baddie = 10
            salida_cherry = 20
            salida_pocion = 1000
            velocidad_maxima_baddie = 4
            velocidad_minima_baddie = 3
            nivel3 == True

        BADDIEMINSPEED = velocidad_minima_baddie
        BADDIEMAXSPEED = velocidad_maxima_baddie
        ADDNEWBADDIERATE = salida_baddie
        ADDNEWCHERRYRATE = salida_cherry
        ADDNEWPOCIONRATE = salida_pocion

        if playerRect.centerx != old_centerx or playerRect.centery != old_centery:
            contador += 1
            old_centery = playerRect.centery
            old_centerx = playerRect.centerx

        else:
            contador = 10

        if contador <= 5:
            player_actual = player_Image2
            
        elif contador <= 10:
            player_actual = player_Image

        elif contador <= 15:
            player_actual = player_Image3

        elif contador <= 20:
            player_actual = player_Image

        if contador >= 20:
            contador = 0        

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()


            if event.type == KEYDOWN:
                if event.key == ord('b'):
                    for b in baddies:
                        baddies.remove(b)
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                elif event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                elif event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                elif event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()


                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            #if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                #playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        
        if not reversecheat and not slowcheat:
            cherryAddCounter += 1
        if cherryAddCounter == ADDNEWCHERRYRATE:
            cherryAddCounter = 0
            cherrySize = random.randint(CHERRYMINSIZE, CHERRYMAXSIZE)
            newCherry = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - cherrySize), 0 - cherrySize, cherrySize, cherrySize),
                        'speed': random.randint(CHERRYMINSPEED, CHERRYMAXSPEED),
                        'surface': pygame.transform.scale(cherryImage, (cherrySize, cherrySize)),
                        } 
            
            cherry.append(newCherry)


        if not reversecheat and not slowcheat:
            pocionAddCounter += 1
        if pocionAddCounter == ADDNEWPOCIONRATE:
            pocionAddCounter = 0
            pocionSize = random.randint(POCIONMINSIZE, POCIONMAXSIZE)
            newpocion = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - pocionSize), 0 - pocionSize, pocionSize, pocionSize),
                        'speed': random.randint(POCIONMINSPEED, POCIONMAXSPEED),
                        'surface': pygame.transform.scale(pocionImage, (pocionSize, pocionSize)),
                        } 
            
            pocion.append(newpocion)


        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
                score = score - 100
            elif slowCheat:
                b['rect'].move_ip(0, 1)
                score = score - 100

        for c in cherry:
            if not reversecheat and not slowcheat:
                c['rect'].move_ip(0, c['speed'])
            elif reversecheat:
                c['rect'].move_ip(0, -5)
            elif slowcheat:
                c['rect'].move_ip(0, 1)

        for p in pocion:
            if not reversecheat and not slowcheat:
                p['rect'].move_ip(0, p['speed'])
            elif reversecheat:
                p['rect'].move_ip(0, -5)
            elif slowcheat:
                p['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
 
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        for c in cherry[:]:
            if c['rect'].top > WINDOWHEIGHT:
                cherry.remove(c)

        for p in pocion[:]:
            if p['rect'].top > WINDOWHEIGHT:
                pocion.remove(p)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Puntuación: %s' % (score), font, windowSurface, 10, 0)
        drawText('Record: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Cerezas: %s' % (cherries), font, windowSurface, 10, 80)
        drawText('Nivel: %s' % (nivel), font, windowSurface, 10, 120)

        # Draw the player's rectangle
        windowSurface.blit(player_actual, playerRect)

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        for c in cherry:
            windowSurface.blit(c['surface'], c['rect'])

        for p in pocion:
            windowSurface.blit(p['surface'], p['rect'])

        pygame.display.update()

        #points_extra = cherries * 100

        # Check if any of the baddies have hit the player.
        
        if playerHasHitBaddie(playerRect, baddies):
            BADDIEMINSPEED = to_reset_BADDIEMINSPEED
            BADDIEMAXSPEED = to_reset_BADDIEMAXSPEED
       
            if score > topScore:
                topScore = score # set new top score
            PLAYERMOVERATE = PLAYERMOVERATE_to_reset
            break

        if playerHasHitPocion(playerRect, pocion):
            PLAYERMOVERATE = PLAYERMOVERATE_to_reset
            pocion.remove(p)

        cereza_chocada = playerHasHitCherry(playerRect, cherry)
        if not cereza_chocada == False:
            cherry.remove(cereza_chocada)         
            drawText('+100', font, windowSurface, cherryRect.centerx, cherryRect.centery)
            cherries = cherries + 1
            PLAYERMOVERATE = PLAYERMOVERATE - 0.15
            score = score + 100

        if una_vez == True and cherries > 5 and cherries / 5 == int(cherries / 5):
            BADDIEMINSPEED = BADDIEMINSPEED + 2
            BADDIEMAXSPEED = BADDIEMAXSPEED + 2
            una_vez = False
            pasado = cherries 

        if not cherries / 5 == int(cherries / 5):
            una_vez = True

        if nivel == 1:
            if score > 5000 and nivel2 == False:
                drawText('Te has pasado el nivel 1', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                drawText('Aprieta una tecla para ir al nivel 2', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
                pygame.display.update()
                waitForPlayerToPressKey()
                score = 0
                nivel = 2   

        if nivel == 2:
            if score > 10000 and nivel3 == False:
                drawText('Te has pasado el nivel 2', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                drawText('Aprieta una tecla para ir al nivel 3', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
                pygame.display.update()
                waitForPlayerToPressKey()
                score = 0
                nivel = 3

        if nivel == 3:
            if score > 15000:
                drawText('Te has pasado el juego', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                pygame.display.update()

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.

    pygame.mixer.music.stop()
    gameOverSound.play()
           
    drawText('HAS PERDIDO', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Aprieta una tecla para volver a empezar.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
