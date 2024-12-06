import random
cardChoice=0
cardOptions=['Ace_of_Spades','2_of_Spades','3_of_Spades','4_of_Spades','5_of_Spades','6_of_Spades','7_of_Spades','8_of_Spades','9_of_Spades','10_of_Spades','Jack_of_Spades','Queen_of_Spades',
            'King_of_Spades','Ace_of_Hearts','2_of_Hearts','3_of_Hearts','4_of_Hearts','5_of_Hearts','6_of_Hearts','7_of_Hearts','8_of_Hearts','9_of_Hearts','10_of_Hearts','Jack_of_Hearts',
            'Queen_of_Hearts','King_of_Hearts','Ace_of_Dimondonds','2_of_Dimondonds','3_of_Dimondonds','4_of_Dimondonds','5_of_Dimondonds','6_of_Dimondonds','7_of_Dimondonds','8_of_Dimondonds',
            '9_of_Dimondonds','10_of_Dimondonds','Jack_of_Dimondonds','Queen_of_Dimondonds','King_of_Dimondonds','Ace_of_Clubs','2_of_Clubs','3_of_Clubs','4_of_Clubs','5_of_Clubs',
            '6_of_Clubs','7_of_Clubs','8_of_Clubs','9_of_Clubs','10_of_Clubs','Jack_of_Clubs','Queen_of_Clubs','King_of_Clubs']
usedInts=[]
num=int(input("pick the number of cards youd like to stack"))
for i in range (num):
    cardChoice = random.randint(0,51)
    while (cardChoice in usedInts):
        cardChoice = random.randint(0,51)
        
    usedInts.append(cardChoice)
    card=cardOptions[cardChoice]

    print("bpy.context.collection.objects['",card,"'].location=(0,0,0)")
        
    
