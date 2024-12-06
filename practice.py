import math
for x in range (0,10):
    print('this is a count, i am at:', x)
    raw= input("please enter a number to multiple this by: ")
    while raw.isnumeric() ==False:
        print("i asked for a numberr..")
        raw= input("please enter a number to multiple this by: ")
    num=int(raw)
    print(num*x)
    if num==x:
        print('Look at that, this is a square')


