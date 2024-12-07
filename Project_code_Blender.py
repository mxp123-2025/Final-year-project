import random
import math
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
usedInts=[]
choice=0

cardOptions=['Queen_of_Dimonds','King_of_Dimonds','Queen_of_Hearts','King_of_Clubs',
             'Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades',
             'Queen_of_Spades','King_of_Spades']
avaliable=['Queen_of_Dimonds','King_of_Dimonds','Queen_of_Hearts','King_of_Clubs',
             'Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades',
             'Queen_of_Spades','King_of_Spades']
cardOptionsLarge=['Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades','Queen_of_Spades',
            'King_of_Spades','Ace_of_Hearts','2_of_Hearts','3_of_Hearts','4_of_Hearts','5_of_Hearts','6_of_Hearts','7_of_Hearts','8_of_Hearts','9_of_Hearts','10_of_Hearts','Jack_of_Hearts',
            'Queen_of_Hearts','King_of_Hearts','Ace_of_Dimondonds','2_of_Dimondonds','3_of_Dimondonds','4_of_Dimondonds','5_of_Dimondonds','6_of_Dimondonds','7_of_Dimondonds','8_of_Dimondonds',
            '9_of_Dimondonds','10_of_Dimondonds','Jack_of_Dimondonds','Queen_of_Dimondonds','King_of_Dimondonds','Ace_of_Clubs','2_of_Clubs','3_of_Clubs','4_of_Clubs','5_of_Clubs',
            '6_of_Clubs','7_of_Clubs','8_of_Clubs','9_of_Clubs','10_of_Clubs','Jack_of_Clubs','Queen_of_Clubs','King_of_Clubs']
def cardDeck():
    x=0
    for i in range (0,len(avaliable)):
        print("bpy.context.collection.objects['"+avaliable[i]+"'].rotation_euler=(math.radians( 90 ),0,0)")
        print("bpy.context.collection.objects['"+avaliable[i]+"'].location=(0.73164,-1.2662 ,",(x*CardWidth)+CardWidth/2,")")
        x=x+1
        
def randomCard():
    cardChoice2 = random.randint(0,len(cardOptionsLarge)-1)
    cardChoice=random.randint(0,len(avaliable)-1)
    cardsChecked=[]

    #while (cardOptions[cardChoice] in usedInts):
    
    #usedInts.append(avaliable[cardChoice])
    card=avaliable[cardChoice]
    avaliable.remove(avaliable[cardChoice])
    return card
        
def chooseAngles(num):
    anglesChoosen=[]
    for i in range(0,num):
        angle=int(input("enter the angle that this card is at: "))
        anglesChoosen.append(angle)
    return anglesChoosen,num

def Z_location(i,card, Last_Angle,Height_of_Last_Card, start_Position,Opposite,angle):
    #print("This code gets me the height that the card would have to be from the Z axis")
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
        #Left_Card_Locations.append()
    Distance_Base.append(Height_F_Cards[i])
    Z_Distance=Z_Distance+Height_F_Cards[i]        
    Next_Start_Position=LeftDistance+start_Position
    #Next_Start_Point=LeftDistance+LeftDistance-start_Position
    #print("The height of this card from the Z axis is:",Z_Distance)
    #print("The distance of this card from the LEFT object is:",LeftDistance)
    #print("The Blender code is:")
        

    print("bpy.context.collection.objects['"+card+"'].rotation_euler=(math.radians(",angle,"),0,0)")
    print("bpy.context.collection.objects['"+card+"'].location=(0,",Next_Start_Position,",",Z_Distance,")")
    return angleRadians,Height_of_Current_Card,Next_Start_Position
   
def Across(anglesChoosen,numCards):
    if len(avaliable)==0:
        return
    Height_of_Card=1000
    Last_Angle=0
    for i in range(0,numCards):
        if(i==0):
            location_from_Y=0
        if(i%2==0):
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,randomCard(),Last_Angle,Height_of_Card,location_from_Y,True,anglesChoosen[i])
        else:
            Last_Angle,Height_of_Card,location_from_Y= Z_location(i//2,randomCard(),Last_Angle,Height_of_Card,location_from_Y,False,anglesChoosen[i])      
    #print(anglesChoosen)
    #print(pointDistance)
    #print(Heights_of_Cards)
    if len(avaliable)==0:
        return        
    flat_Cards()
    
    Heights_of_Cards.clear()
    pointDistance.clear()
    Distance_Base.clear()
    #Z_Distance_F_Cards.clear()
    #Height_F_Cards.clear()
    Left_Card_Locations.clear()
    if(numCards-2>0):
        Across(anglesChoosen[numCards:],numCards-2)
    cardDeck()
     
    #print("Heights_of_Flat_Cards",Height_F_Cards)    
    answer=input("want to run again? (press 1 for YES)")
    if(answer=="1"):
        choice2=int(input("how many cards are you using for the bottom row"))
        angles,numCards=chooseAngles(choice2)
        if(numCards!=0):
            Across(angles,numCards)

        
def flat_Cards():

    for i in range(0,len(pointDistance)-1):
        Height_F_Cards[i]=((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+CardWidth+Distance_Base[i]
        Z_Distance_F_Cards[i]=(((Heights_of_Cards[i] +Heights_of_Cards[i+1])/2)+CardWidth/2)+Distance_Base[i]
        if(Heights_of_Cards[i] - Heights_of_Cards[i+1]!=0):
            angle_F=math.atan(pointDistance[i]/(Heights_of_Cards[i] - Heights_of_Cards[i+1]))/radiansConvert
        else:
            angle_F=90
        card=randomCard()
        print("bpy.context.collection.objects['"+card+"'].rotation_euler=(math.radians(",angle_F,"),0,0)")
        print("bpy.context.collection.objects['"+card+"'].location=(0,",Left_Card_Locations[i]+pointDistance[i]/2,",",Z_Distance_F_Cards[i],")")
    Stored_Flat_Cards.append(Z_Distance_F_Cards)
        
    
totalCards=0
total_standing=0
total_flat=0
print(len(cardOptions))
choice=int(input("how many cards are you using for the bottom row"))
while(choice>len(cardOptions)):
    print("we dont have enough cards for that")
    choice=int(input("how many cards are you using for the bottom row"))
    
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
    

        
print(totalCards)
print(total_standing)
print(total_flat)
print("The Blender Code is:\n\n")
angles,numCards=chooseAngles(int(total_standing))
Across(angles,choice)

