#Taylor Howell 2015
# version 3.1
import pygame
import time
import timeit
import math as m


pygame.init() 
#pygame.mouse.set_visible(False)

### Display ###
display_width = 320
display_height = 240

### Colors ###
black = (0,0,0) 
white = (245,245,245) 
grayblue = (32,178,170)
red = (255,165,0)
green = (127,255,0)
red_bright = (255,140,0)
green_bright = (50,205,50)

### Display Setup ###
gameDisplay = pygame.display.set_mode((display_width,display_height)) # Add pygame.FULLSCREEN to make display take over entire window;define the screen size
pygame.display.set_caption('pumpGUI')
clock = pygame.time.Clock()

### Fonts ###
smallText = pygame.font.SysFont(None,16)
mediumText = pygame.font.SysFont(None,20)
largeText = pygame.font.SysFont(None,30)

### Motor ###
motorFullSteps = 200*5.2 #gear ratio motor 5.2:1
microstepping = 8.0 #1,2,8,16
lead = 1.25 # mm 
steps = motorFullSteps*microstepping # total number of steps per revolution due to microstepping
displacementPerStep = lead/steps # mm

### Tables ###
volumeDisplay = 0
volumeFlowDisplay = 0
volumeFlushDisplay = 0
volumeWithdrawDisplay = 0
volumeSym = ['mL','uL']
volumeConvert = [10**3,1]
flowrateDisplay = 0
flowrateFlowDisplay = 0
flowrateFlushDisplay = 0
flowrateWithdrawDisplay = 0
flowrate = ['mL/min','mL/hr','uL/min','uL/hr']
flowrateConvert = [100.0/6,1.0/3.6,1.0/60,1.0/3600]
materialDisplay = 0
material = ['plastic','glass','metal']
brandDisplay = 0
brand = ['BD','CUSTOM']
syringeDisplay = 0
syringe = ['1cc','3cc','5cc','10cc']
diameter = [4.7,8.59,11.99,14.48]
previousScreen = ''

### Volumes and Rates ###
flowVolume = '---'
flowRate = '---'
flushVolume = '---'
flushRate = '---'
withdrawVolume = '---'
calc = ''
ID = '---'
entry = [flowVolume,flowRate,flushVolume,flushRate,withdrawVolume,ID]
numLocation = None
decimal = False
pause = False
### Motor Functions ###

def up():
    print('Up')
    time.sleep(.05)

def down():
    print('Down')
    time.sleep(.05)
    
### GUI functions ###

def pausing():
    global pause
    pause = True
    paused()
    
def unpause():
    global pause
    pause = False
    
def paused(): # pause menu

    while pause:
        pygame.event.get()
        gameDisplay.fill(black)
        TextSurface, TextRectangle = text_objects("PAUSED",largeText,white)
        TextRectangle.center = ((display_width/2),(2*display_height/5))
        gameDisplay.blit(TextSurface,TextRectangle)
        circleButton("RESUME",100,175,30,white,white,green,3,unpause)
        circleButton("CANCEL", 220, 175,30, white,white, red,3,homescreen)
        pygame.display.update()
        clock.tick(60)
        
def materialToggle():
    global materialDisplay

    if materialDisplay == 0:
        i = 1
    if materialDisplay == 1:
        i = 2
    if materialDisplay == 2:
        i = 0
    
    materialDisplay = i
    time.sleep(.3)
    
def brandToggle():
    global brandDisplay

    if brandDisplay == 0:
        i = 1
    if brandDisplay == 1:
        i = 0
        
    brandDisplay = i
    time.sleep(.3)

def syringeToggle():
    global syringeDisplay

    if syringeDisplay == 0:
        i = 1
    if syringeDisplay == 1:
        i = 2
    if syringeDisplay == 2:
        i = 3
    if syringeDisplay == 3:
        i = 0
        
    syringeDisplay = i
    time.sleep(.3)

def quitProgram():
    pygame.quit()
    quit()

def text_objects(text, font, color):
    textSurface = font.render(text,True,color)
    return textSurface,textSurface.get_rect()

def text_locations(x,y,message,font,color):
    textSurf, textRect = text_objects(message,font,color)
    textRect.center = ((x ,y))
    gameDisplay.blit(textSurf,textRect)

def rectButton(message,x,y,width,height,textColor,inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    
    if x + width > mouse[0] > x   and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height),thickness)
        textSurf, textRect = text_objects(message,mediumText,activeColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height), thickness) 
        textSurf, textRect = text_objects(message,mediumText,textColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)

def numEntryButton(message,x,y,width,height,textColor,inactiveColor,activeColor,thickness,location,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    global numLocation
    numLocation = location
    
    if x + width > mouse[0] > x   and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height),thickness)
        textSurf, textRect = text_objects(message,mediumText,activeColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height), thickness) 
        textSurf, textRect = text_objects(message,mediumText,textColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        
def circleButton(message,x,y,radius, textColor, inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    
    if x + radius > mouse[0] > x - radius and y + radius > mouse[1] > y - radius:
        pygame.draw.circle(gameDisplay, activeColor, (x,y),radius,thickness)
        textSurf, textRect = text_objects(message,mediumText,activeColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and action != None:
            action()        
    else:
        pygame.draw.circle(gameDisplay, inactiveColor, (x,y), radius, thickness) 
        textSurf, textRect = text_objects(message,mediumText,textColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
    
def numberButton(number,location,message,x,y,radius, textColor, inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    global calc
    if x + 1*radius > mouse[0] > x - 1*radius and y + 1*radius > mouse[1] > y - 1*radius:
        pygame.draw.circle(gameDisplay, activeColor, (x,y),radius,thickness)
        textSurf, textRect = text_objects(message,mediumText,activeColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and message != '.':
            calc = calc + message
            if action !=None:
                action()
            time.sleep(.1)
        elif click != (0,0,0) and message == '.' and decimal == False:
            calc = calc + message
            if action !=None:
                decimalRestrict()
            time.sleep(.1)
    else:
        pygame.draw.circle(gameDisplay, inactiveColor, (x,y), radius, thickness) 
        textSurf, textRect = text_objects(message,mediumText,textColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
    
    time.sleep(.005)
    
def decimalRestrict():
    global decimal
    decimal = True
    
def enterButton():
    global flowVolume,flowRate,flushVolume,flushRate,withdrawVolume,calc,decimal,previousScreen,ID
    if calc == '':
        numberpad()
    if calc == '.':
        numberpad()
    
    decimal = False
    x = float(calc)
    calc = ''
    if numLocation == 0:
        flowVolume = x
        flowScreen()
    if numLocation == 1:
        flowRate = x
        flowScreen()
    if numLocation == 2:
        flushVolume = x
        flushScreen()
    if numLocation == 3:
        flushRate = x
        flushScreen()
    if numLocation == 4:
        withdrawVolume = x
        withdrawScreen()
    if numLocation == 5:
        ID = x
        previousScreen()
        
    time.sleep(.1)
    
def backspaceButton():
    global calc,decimal
    
    if calc == '':
        numberpad()
    if calc[-1] == '.':
        decimal = False
    if calc == '':
        numberpad()
    else:
        x = calc[:-1]
        calc = x
        
    time.sleep(.2)
    
def volumeFlowToggle():
    global volumeFlowDisplay
    
    if volumeFlowDisplay == 0:
        i = 1
    elif volumeFlowDisplay == 1:
        i = 0
        
    volumeFlowDisplay = i
    time.sleep(.3)
    
def volumeWithdrawToggle():
    global volumeWithdrawDisplay
    
    if volumeWithdrawDisplay == 0:
        i = 1
    elif volumeWithdrawDisplay == 1:
        i = 0
        
    volumeWithdrawDisplay = i
    time.sleep(.3)
    
def volumeFlushToggle():
    global volumeFlushDisplay
    
    if volumeFlushDisplay == 0:
        i = 1
    elif volumeFlushDisplay == 1:
        i = 0
        
    volumeFlushDisplay = i
    time.sleep(.3)

def flowrateFlowToggle():
    global flowrateFlowDisplay

    if flowrateFlowDisplay == 0:
        i = 1
    if flowrateFlowDisplay == 1:
        i = 2
    if flowrateFlowDisplay == 2:
        i = 3
    if flowrateFlowDisplay == 3:
        i =  0
        
    flowrateFlowDisplay = i
    time.sleep(.3)

def flowrateFlushToggle():
    global flowrateFlushDisplay

    if flowrateFlushDisplay == 0:
        i = 1
    if flowrateFlushDisplay == 1:
        i = 2
    if flowrateFlushDisplay == 2:
        i = 3
    if flowrateFlushDisplay == 3:
        i =  0
        
    flowrateFlushDisplay = i
    time.sleep(.3)

def flowrateWithdrawToggle():
    global flowrateWithdrawDisplay

    if flowrateWithdrawDisplay == 0:
        i = 1
    if flowrateWithdrawDisplay == 1:
        i = 2
    if flowrateWithdrawDisplay == 2:
        i = 3
    if flowrateWithdrawDisplay == 3:
        i =  0
        
    flowrateWithdrawDisplay = i
    time.sleep(.3)

### SCREENS ###
def homescreen():
    time.sleep(.3)
    global previousScreen
    previousScreen = homescreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("UP DOWN",100,70,40,white,white,grayblue,3,updownScreen)
        circleButton("FLOW",100,240-70,40,white,white,grayblue,3,flowScreen)
        circleButton('WITHDRAW',320-100,70,40,white,white,grayblue,3,withdrawScreen)
        circleButton("FLUSH",320- 100,240-70,40,white,white,grayblue,3,flushScreen)
        circleButton("QUIT", 320-30,240-30,20,white,white,red,3,quitProgram)
        text_locations(display_width/2,230,'TAYLOR HOWELL 2015',smallText,white)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def updownScreen():
    global previousScreen
    previousScreen = updownScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("UP",160,70,40,white,white,grayblue,3,up)
        circleButton("DOWN",160,240-70,40,white,white,grayblue,3,down)
        circleButton("HOME",320-40,240-40,30,white,white,red,3,homescreen)

        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def flowScreen():
    global previousScreen
    previousScreen = flowScreen
    time.sleep(.3)
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,white,white,red,3,homescreen)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay],175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeFlowDisplay],170,42,30,white,white,grayblue,3,volumeFlowToggle)
        circleButton(flowrate[flowrateFlowDisplay],170,117,30,white,white,grayblue,3,flowrateFlowToggle)
        circleButton("RUN", 320-65, 75, 40,white,white,green,3,flowRunScreen)
        numEntryButton(str(flowVolume),25,25,100,35,white,white,grayblue,3,0,numberpad)
        numEntryButton(str(flowRate),25,100,100,35,white,white,grayblue,3,1,numberpad)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,white,white,grayblue,3,5,numberpad)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def withdrawScreen():
    time.sleep(.3)
    global previousScreen
    previousScreen = withdrawScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,white,white,red,3,homescreen)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay],175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeWithdrawDisplay],170,75,30,white,white,grayblue,3,volumeWithdrawToggle)
        circleButton("WITHDRAW", 320-65, 75, 40,white,white,green,3,withdrawRunScreen)
        numEntryButton(str(withdrawVolume),25,57,100,35,white,white,grayblue,3,4,numberpad)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,white,white,grayblue,3,5,numberpad)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def flushScreen():
    time.sleep(.3)
    global previousScreen
    previousScreen = flushScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,white,white,red,3,homescreen)
        numEntryButton(str(flushVolume),25,25,100,35,white,white,grayblue,3,2,numberpad)
        numEntryButton(str(flushRate),25,100,100,35,white,white,grayblue,3,3,numberpad)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay],175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeFlushDisplay],170,42,30,white,white,grayblue,3,volumeFlushToggle)
        circleButton(flowrate[flowrateFlushDisplay],170,117,30,white,white,grayblue,3,flowrateFlushToggle)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,white,white,grayblue,3,5,numberpad)
        circleButton("RUN", 320-65, 75, 40,white,white,green,3,flushRunScreen)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def numberpad():
    time.sleep(.3)
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("RETURN",320-40,240-40,30,white,white,red,3,previousScreen)
        numberButton(1,None,"1",35,85,25,white,white,grayblue,3,None)
        numberButton(2,None,"2",95,85,25,white,white,grayblue,3,None)
        numberButton(3,None,"3",155,85,25,white,white,grayblue,3,None)
        numberButton(4,None,"4",35,145,25,white,white,grayblue,3,None)
        numberButton(5,None,"5",95,145,25,white,white,grayblue,3,None)
        numberButton(6,None,"6",155,145,25,white,white,grayblue,3,None)
        numberButton(7,None,"7",35,205,25,white,white,grayblue,3,None)
        numberButton(8,None,"8",95,205,25,white,white,grayblue,3,None)
        numberButton(9,None,"9",155,205,25,white,white,grayblue,3,None)
        numberButton(0,None,"0",215,85,25,white,white,grayblue,3,None)
        numberButton(None, None,".",215,145,25,white,white,grayblue,3,decimalRestrict)
        circleButton("<-",215,205,25,white,white,red,3,backspaceButton)
        circleButton("ENTER",280,40, 30, white,white,green, 3, enterButton)
        rectButton(str(calc),10,10,230,40,white,white,white,3,None)
        
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def flowRunScreen():
    global ID,displacementPerStep,volumeFlowDisplay,flowrateFlowDisplay,flowrate,flowVolume,flowRate,volumeConvert,flowrateConvert,diameter,syringeDisplay
    if type(flowVolume) == str or type(flowRate) == str or flowVolume == 0.0 or flowRate == 0.0:
        flowScreen()
 
    
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
       flowScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
    volume = flowVolume*volumeConvert[volumeFlowDisplay]
    rate = flowRate*flowrateConvert[flowrateFlowDisplay] 
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = (totalTime/numberSteps)/2 # seconds
    currentSteps = 0
    print('Flow Volume: ' + str(volume))
    print('Flow Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    t = range(1,(int(totalTime) + 1)*10,1)
    tic = timeit.default_timer()
    for i in t:
        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton('PAUSE',160,205,28, white, white,red,3,pausing)
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*i/t[-2],8),0)
        text_locations(display_width/2,20,'FLOWING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeFlowDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(flowrate[flowrateFlowDisplay],mediumText,white)
        textRect.center = ((218,90))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flowVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flowRate),mediumText,white)
        textRect.center = ((106,90))
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        time.sleep(.1)
    toc = timeit.default_timer()
    print('Run time: ' + str(toc -tic))
    print('Complete')
    completeScreen()
    
def flushRunScreen():
    global ID,displacementPerStep,volumeFlushDisplay,flowrateFlushDisplay,flowrate,flushVolume,flushRate,volumeConvert,flowrateConvert,diameter,syringeDisplay
    if type(flushVolume) == str or type(flushRate) == str or flushVolume == 0.0 or flushRate == 0.0:
        flushScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
        flushScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
    
    volume = flushVolume*volumeConvert[volumeFlushDisplay]
    rate = flushRate*flowrateConvert[flowrateFlushDisplay]
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = (totalTime/numberSteps)/2 # seconds
    currentSteps = 0
    print('Flush Volume: ' + str(volume))
    print('Flush Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    t = range(1,(int(totalTime) + 1)*10,1)
    tic = timeit.default_timer()
    for i in t:
        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton('PAUSE',160,205,28, white, white,red,3,pausing)
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*i/t[-2],8),0)
        text_locations(display_width/2,20,'FLUSHING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeFlushDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(flowrate[flowrateFlushDisplay],mediumText,white)
        textRect.center = ((218,90))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flushVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flushRate),mediumText,white)
        textRect.center = ((106,90))
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        time.sleep(.1)
    toc = timeit.default_timer()
    print('Run time ' + str(toc -tic))
    print('Complete')
    completeScreen()
    print('Run time: ' + str(toc - tic))
    print('Complete')
    completeScreen()
    

def withdrawRunScreen():
    global ID,pause,displacementPerStep,volumeWithdrawDisplay,volumeSym,flowrateDisplay,flowrate,flowVolume,flowRate,volumeConvert,flowrateConvert,diameter,syringeDisplay,withdrawVolume
    if type(withdrawVolume) == str or withdrawVolume == 0:
        withdrawScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
       withdrawScreen() 
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
        
    volume = withdrawVolume*volumeConvert[volumeWithdrawDisplay]
    rate = 10 # uL/s       
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = (totalTime/numberSteps)/2 # seconds
    currentSteps = 0
    print('Withdraw Volume: ' + str(volume))
    print('Withdraw Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    t = range(1,(int(totalTime) + 1)*10,1)
    tic = timeit.default_timer()
    for i in t:
        pygame.event.get() # aquires any event(input) occuring on screen, per frame per second   
        gameDisplay.fill(black) # creates background
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*i/t[-2],8),0)
        circleButton('PAUSE',160,205,28, white, white,red,3,pausing)
        text_locations(display_width/2,20,'WITHDRAWING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeWithdrawDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(withdrawVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flushRate),mediumText,white)
        pygame.display.update()
        time.sleep(.1)
    toc = timeit.default_timer()
    print('Run time ' + str(toc -tic))
    print('Complete')
    completeScreen()
          
def completeScreen():
    gameDisplay.fill(black) # creates background
    text_locations(display_width/2,display_height/2,'COMPLETE',largeText,white)
    pygame.display.update()
    time.sleep(3)
    
    homescreen()
###
        
#Loop
homescreen()
