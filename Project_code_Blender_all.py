import random
import math
import subprocess
import sys
import bpy

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
first_card_last_row=0 #just addedddd!!!
levelTrack=0
last_Card_Added="8_of_Dimonds"


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
    for i in range (0,len(avaliable)):
        bpy.context.collection.objects[avaliable[i]].rotation_euler=(math.radians( 90 ),0,0)
        bpy.context.collection.objects[avaliable[i]].location=(0.73164,-1.2662 ,i*CardWidth+CardWidth/2)

        
def randomCard():
    cardChoice2 = random.randint(0,len(cardOptions)-1)
    cardChoice=random.randint(0,len(avaliable)-1)
    cardsChecked=[]
    card=avaliable[cardChoice]
    avaliable.remove(avaliable[cardChoice])
    return card
        
def chooseAngles(num):
    anglesChoosen=[]
    different=input("If you like to choose each angle please PRESS 1 or if you would like the same angle for ever card PRESS 2")
    if different== "2":
        angle=int(input("enter the angle that this card is at: "))
        for i in range(0,num):
            anglesChoosen.append(angle)
        return anglesChoosen
        
    for i in range(0,num):
        angle=int(input("enter the angle that this card is at: "))
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
    bpy.context.collection.objects[card].rotation_euler=(math.radians(angle),0,0)
    bpy.context.collection.objects[card].location=(0,Next_Start_Position,Z_Distance)
    return angleRadians,Height_of_Current_Card,Next_Start_Position
   
def Across(anglesChoosen,Cards_Per_level,numCards,levelTrack):
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
        if(i==0 ):
            location_from_Y=0 
        if(i%2==0 ):
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,randomCard(),Last_Angle,Height_of_Card,location_from_Y,True,anglesChoosen[i])
        else :
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,randomCard(),Last_Angle,Height_of_Card,location_from_Y,False,anglesChoosen[i])      
    if len(avaliable)==0:
        return
    flat_Cards()
    
    Heights_of_Cards.clear()
    pointDistance.clear()
    Distance_Base.clear()
    Left_Card_Locations.clear()
    if(numCards-2>0):
        levelTrack+=1
        Across(anglesChoosen[numCards:],Cards_Per_level,Cards_Per_level[levelTrack],levelTrack)
    cardDeck()
     
    reset()
    ##answer=input("want to run again? (press 1 for YES)")
    #if(answer=="1"):
        #this=int(input("is this entering (PRESS 1)or using set data(PRESS 2)"))
        #if this==1:
            #start()
        #else:
            #no_input_needed()

        
def flat_Cards():
    for i in range(0,len(pointDistance)-1):
        Height_F_Cards[i]=((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+CardWidth+Distance_Base[i]
        Z_Distance_F_Cards[i]=(((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+CardWidth/2)+Distance_Base[i]
        Stored_Flat_Cards.append(Z_Distance_F_Cards[i])
        if(Heights_of_Cards[i] - Heights_of_Cards[i+1]!=0):
            angle_F=math.atan(pointDistance[i]/(Heights_of_Cards[i] - Heights_of_Cards[i+1]))/radiansConvert
        else:
            angle_F=90
        card=randomCard()
        global last_Card_Added
        last_Card_Added=card
        bpy.context.collection.objects[card].rotation_euler=(math.radians(angle_F),0,0)
        bpy.context.collection.objects[card].location=(0,Left_Card_Locations[i]+pointDistance[i]/2,Z_Distance_F_Cards[i])
        
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




def get_location(frame):
    scene=bpy.context.scene
    scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj=bpy.data.objects[last_Card_Added].evaluated_get(depsgraph)
    current_location=obj.matrix_world.translation.z
    return current_location
    print(get_location(0))
    print(get_location(10))
    print(get_location(100))

def start():
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
            numPairs=int(input("how many cards on next level?"))
            if numPairs>0:
                Cards_Per_level.append(numPairs*2)
                totalCards+=numPairs*2+numPairs-1
                level+=1
    else:
        choice=2*int(input("How many pairs of cards on the bottom level"))
        while(choice>len(cardOptions)):
            print("we dont have enough cards for that")
            choice=int(input("how many cards are you using for the bottom row"))
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
            print(Height_F_Cards)
            Z_Distance_F_Cards.append(0)
    angles=chooseAngles(int(total_standing))
    Across(angles,Cards_Per_level,Cards_Per_level[levelTrack],levelTrack)


def no_input_needed():
    global Height_F_Cards
    Height_F_Cards=[0,0,0,0]
    global Z_Distance_F_Cards
    Z_Distance_F_Cards=[0,0,0,0]
    levelTrack=0
    angles=loadAngles(int(6))
    Across(angles,[4,2],4,0)
    reset()


#this=int(input("is this entering (PRESS 1)or using set data(PRESS 2)"))
this=2
if this==1:
    start()
else:
    no_input_needed()
    
