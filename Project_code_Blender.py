import random
import math
import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np
from cmaes import CMA
import datetime
import time

CardHeight=0.89
CardLength=0.64
CardWidth=0.002
CardWeight=CardHeight*CardWidth*CardWidth*0.3
radiansConvert=0.0174533
Heights_of_Cards=[]
Distance_Base=[]
pointDistance=[]
Height_F_Cards=[]
Z_Distance_F_Cards=[]
Stored_Flat_Cards=[]
Left_Card_Locations=[]
choice=0
levelTrack=0
last_Card_Added="8_of_Dimonds"
lastLevelDifference=0
lastLevelStart=0

def startPage():
    f = open('blenderScript.txt', 'w')
    f.write("import bpy\n")
    f.write("import math\n")
    f.close()

def run_blender():
    get_location()
    f = open('blenderScript.txt', 'a')
    if optimising==True:
        f.write('bpy.ops.wm.quit_blender()\n')
    else:
        f.write("scene.frame_set(0)\n")
        f.write("bpy.ops.screen.animation_play()\n")#Start animation
    f.close()
    # Path to Blender executable on macOS
    blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
    blend_file = "cardSimulation_cardsDesigned.blender.blend"
    python_script = "blenderScript.txt"
    # Construct the command to run Blender in the background with the Python script
    # Running Blender from the terminal using subprocess
    subprocess.run([blender_path, blend_file, "-P", python_script])

def reset():
    global avaliable
    avaliable =cardOptions.copy()
    global Heights_of_Cards
    Heights_of_Cards.clear()
    global Distance_Base
    Distance_Base.clear()
    global pointDistance
    pointDistance.clear()
    global Height_F_Cards
    Height_F_Cards.clear()
    global Z_Distance_F_Cards
    Z_Distance_F_Cards.clear()
    global Stored_Flat_Cards
    Stored_Flat_Cards.clear()
    global Left_Card_Locations
    Left_Card_Locations.clear()
    global choice
    choice=0
    global levelTrack
    levelTrack=0

    
cardOptionsShort=['Ace_of_Dimonds','Queen_of_Dimonds','King_of_Dimonds','Queen_of_Hearts','King_of_Clubs','King_of_Hearts',
             'Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades',
             'Queen_of_Spades','King_of_Spades']
cardOptions=['Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades','Queen_of_Spades',
            'King_of_Spades','Ace_of_Hearts','2_of_Hearts','3_of_Hearts','4_of_Hearts','5_of_Hearts','6_of_Hearts','7_of_Hearts','8_of_Hearts','9_of_Hearts','10_of_Hearts','Jack_of_Hearts',
            'Queen_of_Hearts','King_of_Hearts','Ace_of_Dimonds','2_of_Dimonds','3_of_Dimonds','4_of_Dimonds','5_of_Dimonds','6_of_Dimonds','7_of_Dimonds','8_of_Dimonds',
            '9_of_Dimonds','10_of_Dimonds','Jack_of_Dimonds','Queen_of_Dimonds','King_of_Dimonds','Ace_of_Clubs','2_of_Clubs','3_of_Clubs','4_of_Clubs','5_of_Clubs',
            '6_of_Clubs','7_of_Clubs','8_of_Clubs','9_of_Clubs','10_of_Clubs','Jack_of_Clubs','Queen_of_Clubs','King_of_Clubs']
avaliable=cardOptions.copy()
def cardDeck():
    f = open('blenderScript.txt', 'a')
    for i in range (0,len(avaliable)):
        f.write("bpy.context.collection.objects['")
        f.write(avaliable[i])
        f.write("'].rotation_euler=(math.radians( 90 ),0,0)\n")
        f.write("bpy.context.collection.objects['")
        f.write(avaliable[i])
        f.write("'].location=(0.73164,-1.2662 ,")
        f.write(str((i*CardWidth)+CardWidth/2))
        f.write(")\n")
    f.close()
        
def randomCard():
    cardChoice2 = random.randint(0,len(cardOptions)-1)
    cardChoice=random.randint(0,len(avaliable)-1)
    cardsChecked=[]
    card=avaliable[cardChoice]
    avaliable.remove(avaliable[cardChoice])
    return card
        
def chooseAngles(num):
    anglesChoosen=[]
    different=input("If you like to choose each angle please ENTER 1, if you wouuld like to choose two angles to be set to every pair of cards please ENTER 2,if you would like the same angle for ever card ENTER 3")
    if different== "3":
        angle=float(input("enter the angle that this card is at: "))
        for i in range(0,num):
            anglesChoosen.append(angle)
        return anglesChoosen
    elif different=="2":
        angle=float(input("enter the angle that this card is at: "))
        angle2=float(input("enter the angle that this card is at: "))
        for i in range(0,num):
            if i%2==0:
                anglesChoosen.append(angle)
            else:
                anglesChoosen.append(angle2)
    return anglesChoosen        
    for i in range(0,num):
        angle=float(input("enter the angle that this card is at: "))
        anglesChoosen.append(angle)
    return anglesChoosen

def loadAngles(num):
    anglesChoosen=[]
    for i in range(0,num):
        anglesChoosen.append(20)
    return anglesChoosen

def Z_location(i,card, Last_Angle,Height_of_Last_Card, start_Position,Opposite,angle):
    LeftDistance=0
    angleRadians=(angle%90)*radiansConvert
    if (angle % 90==0):
        Z_Distance=CardWidth/2
    if (angle % 180==0):
        Z_Distance=CardHeight/2
    else:
        Z_Distance=(CardHeight/2)*math.cos(angleRadians)+(CardWidth/2)*math.sin(angleRadians)
    if (Z_Distance<0):
        Z_Distance=-Z_Distance
    
    Height_of_Current_Card=Z_Distance*2
    LeftDistance=(CardWidth/2)*math.sin((90*radiansConvert)-angleRadians)+(CardHeight/2)*math.sin(angleRadians)
    if (LeftDistance<0):
        LeftDistance=-LeftDistance

    if (Height_of_Last_Card!=1000 and Opposite==False):
        pointDistance.append(LeftDistance*2)
        Left_Card_Locations.append(start_Position+Height_of_Last_Card*math.tan(Last_Angle))
        if (Height_of_Last_Card>Height_of_Current_Card):
            LeftDistance=LeftDistance+(math.tan(Last_Angle)*Height_of_Current_Card - (math.tan(Last_Angle)*Height_of_Last_Card)/2)
        elif (Height_of_Last_Card<Height_of_Current_Card):
            LeftDistance=(Height_of_Last_Card/2)*math.tan(Last_Angle)+Height_of_Last_Card * math.tan(angleRadians)-Height_of_Current_Card/2*math.tan(angleRadians)
        elif (Height_of_Last_Card==Height_of_Current_Card):
            LeftDistance=2*LeftDistance
    elif (Height_of_Last_Card!=1000 and Opposite==True):
        LeftDistance=LeftDistance + math.tan(Last_Angle)*Height_of_Last_Card/2 + math.sin(angleRadians)*CardWidth
    if(Opposite==True):
        angle=-angle
    else:
        if (Height_of_Last_Card<Height_of_Current_Card):
            Heights_of_Cards.append(Height_of_Current_Card)
        else:
            Heights_of_Cards.append(Height_of_Last_Card)
    Distance_Base.append(Height_F_Cards[i])
    Z_Distance=Z_Distance+Height_F_Cards[i]        
    Next_Start_Position=LeftDistance+start_Position
    global last_Card_Added
    last_Card_Added=card
    f = open('blenderScript.txt', 'a')
    f.write("bpy.context.collection.objects['")
    f.write(card)
    f.write("'].rotation_euler=(math.radians(")
    f.write(str(angle))
    f.write("),0,0)\n")
    f.write("bpy.context.collection.objects['")
    f.write(card)
    f.write("'].location=(0,")
    f.write(str(Next_Start_Position))
    f.write(",")
    f.write(str(Z_Distance))
    f.write(")\n")
    f.close()
    return angleRadians,Height_of_Current_Card,Next_Start_Position
   
def Across(anglesChoosen,Cards_Per_level,numCards,levelTrack):
    global lastLevelDifference
    global lastLevelStart
    CardsOnLevel=[]
    using=0
    if len(avaliable)==0:
        return
    if (numCards>len(avaliable)):
        using=len(avaliable)
    else:
        using=numCards
    Height_of_Card=1000
    Last_Angle=0
    for i in range(0,using):
        card=randomCard()
        CardsOnLevel.append(card)
        if(i==0 ):
            location_from_Y=0
        if(i%2==0 ):
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,card,Last_Angle,Height_of_Card,location_from_Y,True,anglesChoosen[i])
            if i==0:
                currentLevelStart=location_from_Y
        else :
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,card,Last_Angle,Height_of_Card,location_from_Y,False,anglesChoosen[i])       
    currentLevelEnd=location_from_Y
    currentLevelDifference=currentLevelEnd-currentLevelStart
    
    if lastLevelDifference>0:
        currentLevelStart=(lastLevelDifference-currentLevelDifference)/2+lastLevelStart
    else:
        currentLevelStart=currentLevelStart
    lastLevelDifference=currentLevelDifference
    
    for x in range(0,len(CardsOnLevel)):
        f = open('blenderScript.txt', 'a')
        f.write("bpy.context.collection.objects['")
        f.write(CardsOnLevel[x])
        f.write("'].location.y+=")
        f.write(str(currentLevelStart))
        f.write("\n")
        f.close()
    lastLevelStart=currentLevelStart    
    
    if len(avaliable)==0:
        return
    flat_Cards(currentLevelStart)
    
    Heights_of_Cards.clear()
    pointDistance.clear()
    Distance_Base.clear()
    Left_Card_Locations.clear()
    if(numCards-2>0):
        levelTrack+=1
        Across(anglesChoosen[numCards:],Cards_Per_level,Cards_Per_level[levelTrack],levelTrack)



        
def flat_Cards(start):
    for i in range(0,len(pointDistance)-1):
        Height_F_Cards[i]=((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+Distance_Base[i]+CardWidth
        Z_Distance_F_Cards[i]=(((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+CardWidth/2)+Distance_Base[i]
        Stored_Flat_Cards.append(Z_Distance_F_Cards[i])
        if(Heights_of_Cards[i] - Heights_of_Cards[i+1]!=0):
            angle_F=math.atan(pointDistance[i]/(Heights_of_Cards[i] - Heights_of_Cards[i+1]))/radiansConvert
        else:
            angle_F=90
        card=randomCard()
        global last_Card_Added
        last_Card_Added=card
        f = open('blenderScript.txt', 'a')
        f.write("bpy.context.collection.objects['")
        f.write(card)
        f.write("'].rotation_euler=(math.radians(")
        f.write(str(angle_F))
        f.write("),0,0)\n")
        f.write("bpy.context.collection.objects['")
        f.write(card)
        f.write("'].location=(0,")
        f.write(str(start+Left_Card_Locations[i]+pointDistance[i]/2))
        f.write(",")
        f.write(str(Z_Distance_F_Cards[i]))
        f.write(")\n")
        f.close()
        
        if len(avaliable)<=0:
            return
    
def standing_cards(choice):
    totalCards=0
    total_standing=0
    total_flat=0
    for x in range(0,(choice//2)):
        Height_F_Cards.append(0)
        Z_Distance_F_Cards.append(0)
        if totalCards+choice-2*x<len(cardOptions):
            total_standing=total_standing+choice-2*x
            totalCards=totalCards+choice-2*x
        else:
            total_standing=total_standing+len(cardOptions)-totalCards
            totalCards=len(cardOptions)
            x=100
        if totalCards<len(cardOptions):
            if totalCards-x-1+choice/2<len(cardOptions):
                total_flat=total_flat-x-1+choice/2
                totalCards=totalCards-x-1+choice/2
            else:
                total_flat=total_flat+len(cardOptions)-totalCards
                totalCards=len(cardOptions)
                x=100

    return int(total_standing)        




def get_location():
    f = open('blenderScript.txt', 'a')
    f.write("for x in range(0,")
    f.write(str(frame+1))
    f.write("):\n")
    f.write("    scene=bpy.context.scene\n")
    f.write("    scene.frame_set(x)\n")
    f.write("def get_location(frame):\n")
    f.write("    scene=bpy.context.scene\n")
    f.write("    scene.frame_set(frame)\n")
    f.write("    depsgraph = bpy.context.evaluated_depsgraph_get()\n")
    f.write("    obj=bpy.data.objects['")
    f.write(last_Card_Added)
    f.write("'].evaluated_get(depsgraph)\n")
    f.write("    current_location=obj.matrix_world.translation.z\n")
    f.write("    return current_location\n")
    f.write("f=open('result.txt', 'w')\n")
    f.write('f.write(str(get_location(')
    f.write(str(frame))
    f.write(')))\n')
    f.write('f.close()\n')

def start2():
    total_standing,Cards_Per_level=starts_Core()
    angles=chooseAngles(int(total_standing))
    Across(angles,Cards_Per_level,Cards_Per_level[levelTrack],levelTrack)
    cardDeck()
    run_blender()
    reset()
    
def starts_Core():
    totalCards=0
    total_flat=0
    print(len(cardOptions))
    Cards_Per_level=[]
    choice1=int(input("Do you want to make a normal card tower (PRESS 1) or create something UNIQUE choose the amount of cards per level (PRESS 2)?"))
    if choice1==2:
        print("Choose your cards for each row:")
        numPairs=2
        level=0
        while(numPairs>1):
            numPairs=int(input("how many pairs of cards on next level?"))
            if numPairs>0:
                Cards_Per_level.append(numPairs*2)
                totalCards+=numPairs*2+numPairs-1
                level+=1
    else:
        choice=2*int(input("How many pairs of cards on the bottom level"))
        while(choice>len(cardOptions)):
            print("we dont have enough cards for that")
            choice=int(input("how many pairs of cards are you using for the bottom row"))
            choice=choice*2
        while(choice>=1):
            Cards_Per_level.append(choice)
            totalCards+=choice+choice/2-1
            choice-=2

    total_standing=0
    print("This card tower will have: ",totalCards," Cards")
    for n in range (0, len(Cards_Per_level)):
        total_standing+=Cards_Per_level[n]
        for z in range(0,Cards_Per_level[n]-1):
            Height_F_Cards.append(0)
            Z_Distance_F_Cards.append(0)
    return(total_standing,Cards_Per_level)

def start():
    total_standing,Cards_Per_level=starts_Core()
    numAngles=input("Same angle generated for each card(PRESS 1) otherwise (PRESS 2)")
    if numAngles=="2":
        optimise(int(total_standing),Cards_Per_level)
    else:
        optimise2(int(total_standing),Cards_Per_level)

def optimise(numCards,Cards_Per_level):
    startTime=time.time()
    global optimising
    num=2
    numAngles=input("Same angle bewteen pairs of cards(PRESS 1) or an angle for each card(PRESS 2)")
    print("There will be 50 generations in total(0-49)\n")
    if numAngles=="2":
        num=numCards
    optimizer = CMA(mean=np.zeros(num), sigma=1.3)
    angles=[]
    results=[]
    usedAngles=[]
    for generation in range(50):
        solutions = []
        for _ in range(optimizer.population_size):
            angles.clear()
            x = optimizer.ask()
            if numAngles=="2":
                angle1=x[0]
                angle2=x[1]
                if angle1<0:
                    angle1=-angle1
                if angle2<0:
                    angle2=-angle2
                angle=angle1+angle2
            for y in range(0,numCards):
                if numAngles=="3":
                    angles.append(x[y])
                if numAngles=="2":
                    if y%2==0:
                        angles.append(angle1)
                    else:
                        angles.append(angle2)
                else:
                    angle=x[0]
                    for y in range(0,numCards):
                        angles.append(angle)        
            if generation==49 and _==optimizer.population_size-1:
                optimising=False
                endTime=time.time()
            value=Get_Value(angles,numCards,Cards_Per_level)
            run_blender()
            optimising=True
            if generation==49 and _==optimizer.population_size-1:
                print("\nWe're on generation: "+str(generation)+" Part: ",_)
                if numAngles=="2":
                    print("angles choosen were:",angles[0]," and ",angles[1])
                if numAngles=="3":
                    print("angles choosen were:",angles)
                else:
                    print("angle choosen was:",angles[0])
                print("The height at frame ",frame," is: ",value,"\n")    
            elif _==0:
                print("We're on generation: "+str(generation))
            solutions.append((x, -value))
            results.append(value)
            if numAngles =="2"or "1":
                usedAngles.append(angle)
            else:
                total=0
                for x in range(0,numCards):
                    total+=numCards[x]
                usedAngel.append(total/numCards)
                
            startPage()
            reset()
        optimizer.tell(solutions)
    graphs(usedAngles,results)
        

    print("this test ran for: ",(endTime-startTime)//60,"minutes and ",(endTime-startTime)%60," seconds")

def graphs(usedAngles,results):
    xpoints=np.array(usedAngles)
    ypoints=np.array(results)

    fig, axs = plt.subplots(3, 1, constrained_layout=True)
    

    ### graph to demonstrate the relationship between time and height measured ###
    axs[0].plot(ypoints)
    axs[0].set_xlabel("Iteration")
    axs[0].set_ylabel("Height at frame "+str(frame)+"(meters)")
    axs[0].set_title('Graph to demonstrate the relationship between time and height measured', fontsize=10)

    ### graph to demonstrate the relationship between degrees choosen and height measured ###
    axs[1].plot(xpoints,ypoints,"o")
    axs[1].set_xlabel("Angle between cards (Degrees)")
    axs[1].set_ylabel("Height at frame "+str(frame)+"(meters)")
    axs[1].set_title('Graph to demonstrate the relationship between degrees choosen and height measured', fontsize=10)

    ### graph to demonstrate the relationship between time and degree choosen ###
    axs[2].plot(xpoints)
    axs[2].set_xlabel("Iteration")
    axs[2].set_ylabel("Angle between cards (Degrees)")
    axs[2].set_title('Graph to demonstrate the relationship between time and degree choosen', fontsize=10)
    plt.show()
    plt.close()
    
def optimise2(numCards,Cards_Per_level):
    global optimising
    optimising=True
    startTime=time.time()
    highestAngle=0
    highestValue=0
    angles=[]
    usedAngles=[]
    results=[]
    anglesBest=[]
    for x in range (1,90):
        angles.clear()
        usedAngles.append(x)
        for z in range(0,numCards):
            angles.append(x)
        total=0
        for p in range(0,5):
            total+=Get_Value(angles,numCards,Cards_Per_level)
        value=total/5
        results.append(value)
        if value>=highestValue:
            highestValue=value
            highestAngle=x
            anglesBest=angles
        print(x,",",value)
        
    newhighestValue=highestValue
    newhighestAngle=highestAngle
    numb=0.1
    continu="yes"
    count=0
    while continu!="stop":
        count+=1
        LasthighestValue=newhighestValue
        for y in range(1,10):
            angle=highestAngle+y*numb
            angles.clear() 
            usedAngles.append(angle)
            for z in range(0,numCards):
                angles.append(angle)
            value=Get_Value(angles,numCards,Cards_Per_level)
            print("Using the angle:",angle,", the  for height at frame",frame,"was: ",value)
            results.append(value)
            if value>=newhighestValue:
                newhighestValue=value
                newhighestAngle=angle
                anglesBest=angles  
        if LasthighestValue==newhighestValue or count==5:
            x=10
            continu="stop"
        numb=numb/10
        highestValue=newhighestValue
        highestAngle=newhighestAngle

    optimising=False
    results.append(Get_Value(anglesBest,numCards,Cards_Per_level))
    usedAngles.append(highestAngle)
    endTime=time.time()
    print("this test ran for: ",(endTime-startTime)//60,"minutes and ",int((endTime-startTime)%60)," seconds")
    print("Best angle was:", highestAngle)
    print("the Height of last card frame ",frame,": ",highestValue)
    graphs(usedAngles,results)
        
def Get_Value(angles,numCards,Cards_Per_level):
    global Height_F_Cards
    global Z_Distance_F_Cards
    for y in range (numCards):
        Height_F_Cards.append(0)
        Z_Distance_F_Cards.append(0)
    levelTrack=0  
    Across(angles,Cards_Per_level,Cards_Per_level[levelTrack],levelTrack)
    cardDeck()
    run_blender()
    startPage()
    reset()
    f=open("result.txt","r")
    value = float(f.readline())
    f.close()
    return(value)
        
this=""
while this.upper()!="X":
    startPage()
    global frame
    frame=int(input("What frame would you like to test to(if tester please put 100 or 250)\n"))    
    optimising=True
    this=input("Is this entering (PRESS 1), using entering with optimised angles(PRESS 2), using set data(PRESS 3)\n")
    if this=="1":
        optimising=False
        start2()
    if this=="2":
        start()
    if this=="3":
        this=input("Gerating one angle for all cards(PRESS 1), generating more than angle(PRESS 2) ")
        if this=="1":
            optimise2(2,[2])
            optimise2(6,[4,2])
            optimise2(8,[6,2])
            optimise2(14,[8,4,2])
            optimise2(26,[12,8,4,2])
        if this=="2":
            optimise(2,[2])
            optimise(6,[4,2])
            optimise(8,[6,2])
            optimise(14,[8,4,2])
            optimise(26,[12,8,4,2])
    this=input("Would you like to comtinue(Type 'X' if no)? ")
    
    
