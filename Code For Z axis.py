import math
def Z_location():
    print("This code gets me the height that the card would have to be from the Z axis")
    angle=int(input("enter the angle that this card is at: "))
    angle=angle*0.0174533
    print("The height of this card from the Z axis is:",0.89*math.cos(angle)/2)
Z_location()
