# -*- coding: utf-8 -*-

from random import choice

hands = ["Rock", "Paper", "Scissors"]

def nextkey(key):
    return key if key != 2 else 0
        
while True:
    try:
        print("1: Rock, 2: Paper, 3: Scissors")
        key = raw_input("Enter your hand: ")
        
        if int(key) not in [1,2,3]:
            print "Enter one of 1: Rock, 2: Paper, 3: Scissors"
            continue

        index = int(key) - 1
        npc = choice(hands)
        user = hands[index]
        hands_pair = (user, npc)

        if npc == user:
            print "Draw!! -> user %s : npc %s" % hands_pair
        elif hands[nextkey(index)] == npc:
            print "Win!! -> user %s : npc %s" % hands_pair
        else:
            print "Lose!! -> user %s : npc %s" % hands_pair
    except:
        continue
        

