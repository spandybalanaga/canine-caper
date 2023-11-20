import pygame as pg
from pygame.locals import *
import random
pg.init()
pg.display.init()

pg.font.init()


from rooms import Room

running = False
title = True

dispH = 500 ##display height
dispW = 1000 ##display width

doorL = pg.Rect(0,124,5,368) ## doors
doorR = pg.Rect(995,124,30,368)

currentRoom = 5 ## where you start


bar = Room("bar", dispH, dispW, "img/bar.png")
garden = Room("garden", dispH, dispW, "img/garden.png")
street = Room("street", dispH, dispW, "img/street.png")
shop = Room("shop", dispH, dispW, "img/shop.png")
bakery = Room("bakery", dispH, dispW, "img/bakery.png")
busstop = Room("bus stop", dispH, dispW, "img/busstop.png")

##rooms = [shop, street, bar, garden, bakery, bridge]
rooms = [shop, garden, bakery, street, bar, busstop]

clock = pg.time.Clock()

player = pg.image.load("img/char_profile_R.png")
pldance1 = pg.image.load("img/char disco up.png")
pldance2 = pg.image.load("img/char disco down.png")

plsit = pg.image.load("img/charsitting.png")
plsit2 = pg.image.load("img/charsitting2.png")
plx = 234
ply = 90

##---------------------PLANTS-----------------------------------
allPlanted = False

cPothos = False # clicked pothos
pPothos = False # planted pothos
ptPothos = False #planted pothos textbox
pothos = pg.image.load("img/bar plant.png")


cMonsterra = False #clicked Monsterra
pMonsterra = False #planted monsterra
ptMonsterra = False #planted monsterra text box
monsterra = pg.image.load("img/street plant.png")


##---------------------STUFF-----------------------------------
peanutbutter = pg.image.load("img/peanutbutterjar.png")
flour = pg.image.load("img/flourbag.png")

cPB = False
cFlour = False
tSteal = False
paid = False
cCrystal = False
cBottle = False

cBench = False
benchIB = False

crystal = pg.image.load("img/crystal.png")
bustix = pg.image.load("img/bustix.png")
busx = 341

cookies = pg.image.load("img/cookies.png")
plate = pg.image.load("img/plate.png")

## -----------------PEOPLE-------------------------------

baker = pg.image.load("img/baker_temp.png")
bartender = pg.image.load("img/bartender_temp.png")
cashier = pg.image.load("img/cashier_temp.png")
dj = pg.image.load("img/dj_temp.png")
psychic = pg.image.load("img/fortuneteller_temp.png")
gardener = pg.image.load("img/gardener_temp.png")
dog = [pg.image.load("img/weinerdog1.png"), pg.image.load("img/weinerdog2.png"), pg.image.load("img/weinerdog3.png")]
dogx = -168


cBaker = False
cBartender = False
cCashier = False

cDJ = False
cDB = False
rejDJ = False
finDance = False
winDance = False

cPsychic = False
cPsyIB = False

cGardener = False

##-------------------------------------------------------

inventory =[]
missions = []

barOpen = False
danceBattle = False

danceCount = 1
danceTimer = 0

motion = [pg.image.load("img/char_profile_R.png") ,pg.image.load("img/char_profile_R.png"),
          pg.image.load("img/char R walk 1.png"), pg.image.load("img/char R walk 1.png"),
          pg.image.load("img/char_profile_R.png") ,pg.image.load("img/char_profile_R.png") ,
          pg.image.load("img/char R walk 2.png"), pg.image.load("img/char R walk 2.png")]
motionCount = 0
zoomies = False

rooms[currentRoom].setCurrentRoom()

def isStealing():
    if rooms[currentRoom] == shop:
        if peanutbutter in inventory or flour in inventory:
            if paid == False:
                if peanutbutter in inventory:
                    inventory.remove(peanutbutter)
                if flour in inventory:
                    inventory.remove(flour)
                return True
    return False


def drawDiscoRays():
    layer = pg.surface.Surface((1000,500), pg.SRCALPHA)
    layer.set_alpha(50)
    
    lightColors = [(255,0,234), (85,225,0), (233,255,48), (0,255,250), (167,137,255)] ##pink, green, chartreuse, cyan, periwinkle
    
    pg.draw.polygon(layer,random.choice(lightColors),[(550,57),(95,455),(250,455),(577,83)]) 
    pg.draw.polygon(layer,random.choice(lightColors),[(560,13),(36,0),(36,86),(550,31)])
    pg.draw.polygon(layer,random.choice(lightColors),[(653,65),(931,455),(799,455),(634,82)]) 
    pg.draw.polygon(layer,random.choice(lightColors),[(653,24),(1000,0),(1000,94),(655,61)]) 
    rooms[currentRoom].screen.blit(layer,(0,0))

def danceSeq():
    global danceCount
    global currentTime
    global danceTimer
    global finDance
    global endTime

    dancemoves = [pg.image.load("img/dj dance1.png"), pg.image.load("img/dj dance1.png"),pg.image.load("img/dj dance1.png"),
                  pg.image.load("img/dj dance2.png"), pg.image.load("img/dj dance2.png"),
                  pg.image.load("img/dj dance3.png"),pg.image.load("img/dj dance3.png"), pg.image.load("img/dj dance3.png"),
                  pg.image.load("img/dj dance2.png"),pg.image.load("img/dj dance2.png")]
    
    if danceCount >= (len(dancemoves)-1):
        danceCount = 0
    else:
        danceCount += 1

    if danceCount == 9:
        danceTimer += 1

    if danceTimer == 3 and danceCount == 8:
        endTime = currentTime + 3000
        
    if danceTimer < 6:
        return dancemoves[danceCount]
    else:
        finDance = True
        if currentTime >= endTime:
            finDance = False
        return pg.image.load("img/dj_temp.png")

barlength = 0
def battleBar():
    global barlength
    
    top = 100
    left = 100
    height = 40
   
    font2 = pg.font.SysFont("Times New Roman", 18)
    dp = font2.render("DANCE POINTS:", 1, [255,255,255])
    
    pg.draw.rect(rooms[currentRoom].screen, [170,0,255], ((top,left), (barlength, height)))
    pg.draw.rect(rooms[currentRoom].screen, [0,0,0], ((left,top), (100, height)), width = 4) ##outline
    
    pg.draw.rect(rooms[currentRoom].screen, [0,0,0], ((70,80), (150, 20)))
    rooms[currentRoom].screen.blit(dp, (80,80))
    
    

def inputBox(string, str2, intg):
    ##font = pg.font.SysFont("Times New Roman", 30)
    font2 = pg.font.SysFont("Times New Roman", 21)
    
    box = pg.Surface((300,90), pg.SRCALPHA)
    box.set_alpha(220)
    box.fill([179,212,236])

    if intg == 1:
        font = pg.font.SysFont("Times New Roman", 30)
    elif intg == 2:
       font = pg.font.SysFont("Times New Roman", 20)
       
    word = font.render(str(string), 1, [0,0,0])
    words = font.render(str(str2), 1, [0,0,0])

    yes = font2.render("YES", 1, [0,0,0])
    no = font2.render("NO", 1, [0,0,0])

    rooms[currentRoom].screen.blit(box, (350,130))
    rooms[currentRoom].screen.blit(word, (375, 140))
    rooms[currentRoom].screen.blit(words, (375, 170))
    
    pg.draw.rect(rooms[currentRoom].screen, [90,194,97], ((380,200), (50,20))) ##yes button
    rooms[currentRoom].screen.blit(yes, (386,198))
    pg.draw.rect(rooms[currentRoom].screen, [210,41,41], ((520,200), (50,20))) ##no button
    rooms[currentRoom].screen.blit(no, (531,198))


def textbox(string1, string2):
    font = pg.font.SysFont("Times New Roman", 24)
    
    box = pg.Surface((600,150), pg.SRCALPHA)
    box.set_alpha(220)
    box.fill([120,120,120])
    words1 = font.render(str(string1), 1, [255,255,255])
    words2 = font.render(str(string2), 1, [255,255,255])

    rooms[currentRoom].screen.blit(box, (200,320))
    rooms[currentRoom].screen.blit(words1, (220, 340))
    rooms[currentRoom].screen.blit(words2, (220, 380))

##
##def textboxImg(string1, string2, charImage):
##    textbox(string1, string2)
##    rooms[currentRoom].screen.blit(charImage, (230, 280))

num = 0
starttime = 0

def introSeq():
    global num
    global dogx
    global busx
    global starttime
    
    busstop.setCurrentRoom()
    screen.blit(crystal, (747,23))
    screen.blit(plsit, (234,122))

    pg.time.set_timer(pg.KEYUP, 150)

    
    if (pg.time.get_ticks() < (starttime + 5000)):
        textbox("You: Ugh this bus is taking forever. And there's barely", "any service around here")

    else:   
        while dogx < 179:
            
            for event in pg.event.get():
                if event.type == KEYUP:
                    ##print(dogx)
                    num+=1
                    dogx +=10
                if num > 2:
                    num = 0
            busstop.setCurrentRoom()
            screen.blit(crystal, (747,23))
            screen.blit(plsit, (234,122))
            screen.blit(dog[num], (dogx, 379))
            
            pg.display.flip()

        pg.time.set_timer(pg.KEYUP, 75)

        while ((dogx >= 179) and (dogx < 1000)):
        
            for event in pg.event.get():
                if event.type == KEYUP:
                    ##print(dogx)
                    num+=1
                    dogx +=10
                    busx +=10
                if num > 2:
                    num = 0
            busstop.setCurrentRoom()
            screen.blit(crystal, (747,23))
            screen.blit(plsit2, (234,95))
            screen.blit(bustix, (busx,388))
            screen.blit(dog[num], (dogx, 379))
            
            pg.display.flip()

        if dogx >= 1000:

            busstop.setCurrentRoom()
            screen.blit(crystal, (747,23))
            screen.blit(plsit2, (234,95))
        
            font = pg.font.SysFont("ArcadeClassic", 30)
            words = font.render("That  thieving  dog  just  stole  your  bus  ticket !", 1, [255,255,255])
            words2 = font.render("Youre  stuck  in  this  town  till  you  get  it  back", 1, [255,255,255])
            words4 = font.render("PRESS SPACE TO CONTINUE", 1, [255,255,255])
            
            screen.blit(words, (170,150))
            screen.blit(words2, (170,180))
            screen.blit(words4, (330,300))

            pg.display.flip()

def outro():
    global starttime
    global num
    global dogx
    global busx

    
    pg.time.set_timer(pg.KEYUP, 150)

    while dogx > 412:
            
        for event in pg.event.get():
            if event.type == KEYUP:
                ##print(dogx)
                num+=1
                dogx -=10
                busx = dogx - 20
            if num > 2:
                num = 0
                
        busstop.setCurrentRoom()
        
        screen.blit(player, (plx,ply))
        screen.blit(plate, (347,316))
        screen.blit(cookies, (347,316))
        screen.blit(bustix, (busx,388))
        screen.blit(pg.transform.flip(dog[num], True, False), (dogx, 379))
        pg.display.update()


    while dogx <= 412:
        busstop.setCurrentRoom()
    
        screen.blit(player, (plx,ply))
        screen.blit(plate, (347,316))
        screen.blit(cookies, (347,316))
        screen.blit(bustix, (busx,388))
        screen.blit(pg.transform.flip(dog[num], True, False), (dogx, 379))    

        font = pg.font.SysFont("ArcadeClassic", 120)
        youwin = font.render("YOU  WIN", 1, [255,255,255])
        gameover = font.render("GAME  OVER", 1, [255,255,255])
        youwin.set_alpha(190)
        gameover.set_alpha(190)
        
        screen.blit(gameover, (240,130))
        screen.blit(youwin, (290,230))

        pg.display.update()
    

def title():
    global starttime
    
    font = pg.font.SysFont("ArcadeClassic", 120)
    font2 = pg.font.SysFont("ArcadeClassic", 40)
    
    mainwords = font.render("CANINE CAPER", 1, [255,255,255])
    secwords = font2.render("press  space  to  begin ", 1, [255,255,255])
    mainwords.set_alpha(170)
    secwords.set_alpha(120)
    titlescreen = pg.image.load("img/titlescreen.png")
    
    screen.blit(titlescreen, (0,0))
    
    screen.blit(mainwords, (135,140))
    screen.blit(secwords, (300,400))
    
    
    pg.display.flip()
    


##---------------------GAME LOOP-----------------------------------

screen = pg.display.set_mode((dispW, dispH))
while running == False:

    while title:
        title()
        event = pg.event.wait()
        if event.type == KEYDOWN and event.key == K_SPACE:
            starttime = pg.time.get_ticks()
            title = False

    ##print("calling introseq")
    introSeq()
    
    event = pg.event.wait()
    if event.type == KEYDOWN and event.key == K_SPACE:
        ##print("moving on")
        running = True

    
    pg.display.flip()
    

while running == True:

    clock.tick(15)
    
    rooms[currentRoom].setCurrentRoom() #redraw backdrop
 
    currentTime = pg.time.get_ticks()

    keys = pg.key.get_pressed()
    
    if keys[pg.K_LEFT]:
        motionCount += 1
        if zoomies == False:
            plx -= 8
        else: plx -= 15

        if motionCount >= len(motion):
            motionCount = 0

        player = pg.transform.flip(motion[motionCount],True, False)

        if player.get_rect(topleft=(plx,ply)).colliderect(doorL): ##if touching Left edge of display ##maybe change to if x is less than
                if isStealing():
                    endTime = currentTime + 5000
                    plx = plx + 120
                    tSteal = True
                else:
                    endTime = 0
                    if currentRoom == 0:
                        currentRoom = (len(rooms) - 1)
                    else:
                        currentRoom -= 1
                
                    plx = (dispW - 165) #put player on right edge of display
    
    if keys[pg.K_RIGHT]:
        motionCount += 1
        if zoomies == False:
            plx += 8
        else: plx +=15

        if motionCount >= len(motion):
            motionCount = 0
    
        player = motion[motionCount]

        if  player.get_rect(topleft=(plx,ply)).colliderect(doorR): ##if touching Right edge of display
            
            if isStealing():
                endTime = currentTime + 5000
                plx = plx - 120
                tSteal = True
                    
            else:
                endTime = 0  
                if currentRoom == (len(rooms) - 1):
                    currentRoom = 0
                else:
                    currentRoom += 1
                plx = 25
        
    
    for event in pg.event.get(): ##for each event

           
        if event.type == pg.QUIT: #exit game
            running = False
            pg.quit()
            sys.exit()

##        if ((event.type == KEYDOWN) and (event.key == K_o)):
##            dogx = 1000
##            busx = 1000
##            outro()
##            pg.display.update()




##-----------------MVMT and CLICK INPUTS----------------

        if rooms[currentRoom] == bar: #While in the Bar
          
            #  DANCE MOVES
            if event.type == KEYDOWN and event.key == K_a:
                rooms[currentRoom].setCurrentRoom()
                player = pldance1
            elif event.type == KEYDOWN and event.key == K_d:
                rooms[currentRoom].setCurrentRoom()
                player = pldance2
                
                if barlength == 96:
                    endTime = currentTime + 4000
                    ##print(endTime)

            if danceBattle == True:
                if ((event.type == KEYDOWN and event.key == K_d) and (barlength <=100)) :
                    barlength += 4



            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()
                posx, posy = pg.mouse.get_pos()
                
                if pothos.get_rect(topleft = (143,54)).collidepoint(pos): ##if clicking plant
                    endTime = currentTime + 2000
                    ##print(endTime)
                    cPothos = True
                    inventory.append(pothos)

                if bartender.get_rect(topleft = (250,80)).collidepoint(pos): #if clicking bartender
                    endTime = currentTime + 5000
                    cBartender = True

                if dj.get_rect(topleft = (700,70)).collidepoint(pos):
                    endTime = currentTime + 5000
                    cDJ = True
                if posy > 208 and posy < 251 and posx > 200 and posx < 224 : ##if clicking green bottle on bar
                    endTime = currentTime +5000
                    cBottle = True

                    
        if rooms[currentRoom] == garden: #in garden
            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()
                posx, posy = pg.mouse.get_pos()

                if gardener.get_rect(topleft = (800,70)).collidepoint(pos): #if clicking gardener
                    endTime = currentTime + 5000
                    cGardener = True

                if posy > 300 and posy < 360 and posx > 510 and posx < 900 :
                    if pothos in inventory:
                        pPothos = True
                        ptPothos = True
                        inventory.remove(pothos)
                        pothos = pg.image.load("img/pothos planted.png")
                        
                    if monsterra in inventory:
                        pMonsterra = True
                        ptMonsterra = True
                        inventory.remove(monsterra)
                        monsterra = pg.image.load("img/monstera planted.png")

                    if pPothos and pMonsterra:
                        allPlanted = True
                        
                    endTime = currentTime + 1000

        if rooms[currentRoom] == street: #While in the Street
            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()
                
                if monsterra.get_rect(topleft = (517,130)).collidepoint(pos) and ((cPsyIB == False) or ("tea leaves" in missions)): ##if clicking plant
                    endTime = currentTime + 3000
                    ##print(endTime)
                    cMonsterra = True
                    inventory.append(monsterra)
                    
                if psychic.get_rect(topleft = (350,148)).collidepoint(pos):
                    endTime = currentTime + 5000
                    cPsychic = True
                    

        if rooms[currentRoom] == shop: #While in the SHOP
            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()

                if cashier.get_rect(topleft = (45,115)).collidepoint(pos):
                    endTime = currentTime + 5000
                    #print(endTime)
                    cCashier = True
                if peanutbutter.get_rect(topleft = (316,246)).collidepoint(pos):
                    endTime = currentTime + 1000
                    cPB = True
                    inventory.append(peanutbutter)
                if flour.get_rect(topleft = (837,160)).collidepoint(pos):
                    endTime = currentTime + 1000
                    cFlour = True
                    inventory.append(flour)

       
        if rooms[currentRoom] == bakery: #While in the BAKERY
            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()

                if baker.get_rect(topleft = (390, 15)).collidepoint(pos):
                    endTime = currentTime + 5000
                    cBaker = True
                
        if rooms[currentRoom] == busstop:
            if event.type == pg.MOUSEBUTTONUP: ##if you click
                pos = pg.mouse.get_pos()
                posx, posy = pg.mouse.get_pos()

                if crystal.get_rect(topleft = (747, 23)).collidepoint(pos):
                    inventory.append(crystal)
                    endTime = currentTime + 1000
                    cCrystal = True
                    
                if (posx > 180) and (posx < 594) and (posy > 244) and (posy < 428):
                    endTime = currentTime + 4000
                    cBench = True

                

            

##------------------------------------DISPLAY COLLECTIBLE STUFF-----------
        
    if rooms[currentRoom] == bar:
        if not(pothos in inventory) and pPothos == False: ##you dont have it and also have not planted in garden !
            rooms[currentRoom].screen.blit(pothos, (143,54))

        if danceBattle == True:
            battleBar()
            
        if barlength == 100 and not("money" in inventory):
            winDance = True
            danceBattle = False


    if rooms[currentRoom] == street:
        if not(monsterra in inventory) and pMonsterra == False: ##you dont have it and also have not planted in garden !
            rooms[currentRoom].screen.blit(monsterra, (517,130))

    if rooms[currentRoom] == garden:
        if pMonsterra == True:
            rooms[currentRoom].screen.blit(monsterra, (630,180))
        if pPothos == True:
            rooms[currentRoom].screen.blit(pothos, (565,264))

    if rooms[currentRoom] == shop:
        if not(peanutbutter in inventory):
            rooms[currentRoom].screen.blit(peanutbutter, (316,246))
        if not(flour in inventory):
            rooms[currentRoom].screen.blit(flour, (837,160))

    if rooms[currentRoom] == busstop:
        if not(crystal in inventory):
            rooms[currentRoom].screen.blit(crystal, (747,23))
        if cBench == True and benchIB== True:
            screen.blit(plate, (347,316))
            screen.blit(cookies, (347,316))
            

    


##------------------------------------DISPLAY NPCs-----------------------------------------------------


    if rooms[currentRoom] == bar:
        rooms[currentRoom].screen.blit(bartender,(250,65))
        if barOpen:
            if danceBattle == True:
                dj = danceSeq()
            rooms[currentRoom].screen.blit(dj,(700,70))
                
                

    if rooms[currentRoom] == garden:
        rooms[currentRoom].screen.blit(gardener,(800,70))

    if rooms[currentRoom] == street:
        rooms[currentRoom].screen.blit(psychic,(350,148))

    if rooms[currentRoom] == garden:
        rooms[currentRoom].screen.blit(gardener,(800,70))

    if rooms[currentRoom] == bakery:
        rooms[currentRoom].screen.blit(baker,(390,15))

    if rooms[currentRoom] == shop:
        rooms[currentRoom].screen.blit(cashier,(45,115))


            
#-------------------------------------------------------------------------------------------------------------------------

    rooms[currentRoom].screen.blit(player,(plx,ply)) #update player




#-------------------------------------------------------------------------------------------------------------------------
##--------------------------------TEXT BOXES----------------------------------# text box needs to be on top of player 

    if rooms[currentRoom] == bar:
        if cBottle == True:
            textbox("You try a sip of this drink. It gives you the zoomies!", "SPEED increases +10")
            if currentTime > endTime:
                zoomies = True
                cBottle = False
        if cPothos == True: 
            textbox("+ Pothos to inventory!", " ")
            if currentTime > endTime:
                #print("times up")
                cPothos = False;
        if cBartender == True:
            if barOpen == False:
                if not("get herbs" in missions):
                    missions.append("get herbs")

                if not("herbs" in inventory):
                    textbox("I cant open my bar without supplies for my signature drink!", "Can you ask the gardener for some mint and basil?")

                if "herbs" in inventory:
                    textbox("Thank you so much!", "Now I can open up the bar!")
                    if currentTime > (endTime - 2000):
                        inventory.remove("herbs")
                        barOpen = True

            if barOpen:
                textbox("Its party time!", "Couldn't have done it without you")
                    
            if currentTime > endTime:
                #print("times up")
                cBartender = False

        if ((barOpen) and (cDJ == True) and (not("money" in inventory))):
            textbox("The only thing better than my music is my dance moves ;)", "I bet you 50 bucks you can't beat me in a dance battle!")
            
            if currentTime > endTime:
                cDJ = False
                cDB = True

                
        if ((barOpen) and (cDB == True) and (not("money" in inventory))):
            inputBox("Dance Battle ?", "", 1)
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect((380,200), (50,20)).collidepoint(pos): ## YES BUTTON
                    #print("entering dance battle")
                    cDB = False
                    danceBattle = True
                    if danceBattle == True:
                        danceCount = 0
                        
                elif pg.Rect((520,200), (50,20)).collidepoint(pos): ##NO BUTTON
                    cDB = False
                    endTime = currentTime + 5000
                    rejDJ = True

        if rejDJ == True:
            textbox("Hah! I knew it. You're no match for me.", "Come back when you learn to dance")
            if currentTime >= endTime:
                rejDJ = False

        if finDance == True:
            textbox("your turn! Lets see what you've got", "[Use keys A and D to dance]")

        if winDance == True:
            textbox("Oh shit, you slayed that! I guess i owe you then, huh?", "+ $50 to inventory")

            if currentTime > endTime:
                ##print("ending textbox")
                inventory.append("money")
                winDance = False
                 

                    

    if rooms[currentRoom] == street:
        if cMonsterra == True: 
            textbox("+ Monsterra to inventory", " ")
            if currentTime > endTime:
                #print("times up")
                cMonsterra = False

        if cPsychic == True:
            if not ("tea leaves" or "crystal ball" or "bake cookies") in missions:
                textbox("My divine intuition tells me something of yours was stolen", "I can help you, if you would like.")
                if currentTime > endTime:
                    cPsyIB = True
                    cPsychic = False
                    #print("time to open input box")
                
            if cPsychic and cPsyIB:
                if not (crystal in inventory) or not ("tea leaves" in inventory):
                    textbox("To summon the spirits, I need you to find me some tools", "Get me a crystal ball and some tea leaves to read...")
                    missions.append("tea leaves")
                    missions.append("crystal ball")

                elif (crystal in inventory) and ("tea leaves" in inventory) and not("dog biscuits" in inventory):
                    textbox("Perfect! Let me see what the spirits say.... Animals are ", "simple creatures, easily swayed by gifts. Perhaps food?")
                    if currentTime > endTime:
                        missions.append("bake cookies")

                if "dog biscuits" in inventory:
                    textbox("Yes, these biscuits will do the trick. I suggest you place", "them at the scene of the crime. I am sure he will come")
                    
            if currentTime > endTime:
                cPsychic = False
                
        if cPsyIB == True and cPsychic == False and (not ("tea leaves" or "crystal ball") in missions):
            #print("input box open!")
            inputBox("Ask the psychic to consult the ",  "spirits to help you find the dog?", 2)
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect((380,200), (50,20)).collidepoint(pos): ## YES BUTTON
                    endTime = currentTime + 5000
                    cPsychic = True
                    
                elif pg.Rect((520,200), (50,20)).collidepoint(pos): ##NO BUTTON
                    cPsyIB = False
                    
                

            
    
    if rooms[currentRoom] == garden: #GARDEN
        
        if cGardener == True:
            if allPlanted:
##                if not("herbs" in inventory):
                textbox("Thanks ! Give these to the bartender", "+ Herbs to inventory")
                inventory.append("herbs")
                if "get herbs" in missions:
                    missions.remove("get herbs")
##                if "herbs" in inventory:
##                    textbox("Thanks again for helping my with my garden!", "")
                
            elif "get herbs" in missions:
                ##print("talking to gardener")
                textbox("You need some herbs? Hmmm...", "Collect some plants for my garden and Ill see what I can do")
            else:
                textbox("My last garden bed is empty.", "I wish I had more plants to fill it with")
                
            if currentTime > endTime:
                cGardener = False

        if ptMonsterra == True:
            textbox("You planted a Plant!", " ")
            if currentTime > endTime:
                #print("times up")
                ptMonsterra = False;
                
        if ptPothos == True: 
            textbox("You planted a Plant!", " ")
            
            if currentTime > endTime:
                #print("times up")
                ptPothos = False;

    if rooms[currentRoom] == shop:
        if tSteal == True:
            textbox("Hey! You need to pay for that! I'm putting these back", "on the shelves till you come back with money")
            if currentTime > endTime:
                #print("times up")
                tSteal = False
                
        if cCashier == True:

            if ((peanutbutter in inventory) and (flour in inventory) and ("money" in inventory)):
                paid = True
                textbox("Hi there! That will be $13.47, please....", "Perfect. Here are your items! Have a nice day")
                
            elif ((peanutbutter in inventory) or (flour in inventory)) and ("money" in inventory):
                textbox("You sure thats all you need today?", "")
                
            elif (not "money" in inventory) and ((peanutbutter in inventory) or (flour in inventory)):
                if (peanutbutter in inventory) and (flour in inventory):
                    
                    textbox("Hi there! That will be $13.47 please.... Oh im going to", "have to keep these if you cant pay for them, sorry")
                    if currentTime > endTime:
                        inventory.remove(peanutbutter)
                        inventory.remove(flour)
                        
                elif (peanutbutter in inventory):
                    textbox("Hi there! That will be $6.89 please.... Oh im going to", "have to keep these if you cant pay for them, sorry")
                    if currentTime > endTime:
                        inventory.remove(peanutbutter)
                        
                elif flour in inventory:
                    textbox("Hi there! That will be $6.58 please.... Oh im going to", "have to keep these if you cant pay for them, sorry")
                    if currentTime > endTime:
                        inventory.remove(flour)
            else:
                textbox("Hey there! Find what you're looking for?", "Holler if you need me!")

            if currentTime > endTime:
                #print("times up")
                cCashier = False;

        if cPB == True:
            textbox("+ Peanut Butter to inventory", "")
            if currentTime > endTime:
                #print("times up")
                cPB = False
        if cFlour == True:
            textbox("+ Flour to inventory", "")
            if currentTime > endTime:
                #print("times up")
                cFlour = False
                

    if rooms[currentRoom] == bakery:
        if cBaker == True:
            if "bake cookies" in missions:
                if (peanutbutter and flour) in inventory:
                    textbox("Oh perfect! I can whip up some wicked biscuits for you!", "+ Peanut Butter Dog Biscuits to Inventory")
                    if currentTime > endTime:
                        inventory.append("dog biscuits")
                else: textbox("You need to make dog biscuits? I can definitely help with", "that! I just need some peanut butter and flour first...")

            elif "tea leaves" in missions:
                textbox("Tea leaves? Luckily we offer complementary black tea!", "+ Tea leaves to Inventory")
                inventory.append("tea leaves")
            else:
                textbox("Hi there! Welcome to my bakery.", "Let me know if anything strikes your fancy!")
            
            if currentTime > endTime:
                #print("times up")
                cBaker = False

    if rooms[currentRoom] == busstop:
        if cCrystal == True:
            textbox("+ Crystal Ball to inventory", "")
            if currentTime > endTime:
                cCrystal = False

    if rooms[currentRoom] == busstop:
            
        if cBench == True and benchIB == False:
            if "dog biscuits" in inventory:
                benchIB = True
                cBench = False
            else: textbox("You: This is where that dog stole my bus pass...", "")

            if currentTime > endTime:
                cBench = False

        elif cBench == True and benchIB== True:
            textbox("you place the dog biscuits by the bus stop...", "")
            if currentTime > endTime:
                cBench = False
                dogx = 1000
                busx = 1000
                outro()

        elif benchIB == True:
            inputBox("Use biscuits to lure the dog? ",  "", 2)
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect((380,200), (50,20)).collidepoint(pos): ## YES BUTTON
                    endTime = currentTime + 5000
                    cBench = True
                    
                elif pg.Rect((520,200), (50,20)).collidepoint(pos): ##NO BUTTON
                    benchIB = False
                    
            

                
#-------------------------------------------------------------------------------------------------------------------------

    if rooms[currentRoom] == bar and barOpen == True: ## draw disco rays in bar
        drawDiscoRays()
        
    pg.display.flip()
    

