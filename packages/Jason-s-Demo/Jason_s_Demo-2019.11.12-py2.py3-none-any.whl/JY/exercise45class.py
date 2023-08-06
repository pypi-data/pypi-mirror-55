from sys import exit
from random import randint
from textwrap import dedent

class fail(object):        #create the fail class first for further use in the other scenes.
    def enter(self):
        print("You fail!")
        exit(1)

class kingomstart(object):
    def enter(self):
        print(dedent("""
              Once upon a time, there was a kingdom called "jj's Nation".
              The king lost his beloved daughter, the beautiful princess.
              So the king made an announcement to enlist heroes to save
              the princess. The true hero who can bring the princess back
              can therefore marry the princess. So, on the day when the king
              meeting with all the signed heroes. The king asked you:\"
              How do you gonna bring my daughter back?\""""))

        reply = input(">")

        if reply == "Your Majesty: I will use my power!":
            print(dedent("""
                  The king looking at you and said:\"retarded! Musscle can't
                  solve the problem! I don't need dumbass barbarian.\""""))
            return 'Game_Over'

        if reply == "Your Majesty: I will use my wisdom!":
            print(dedent("""
                  The king looking at you and said: \"fuck off weak shit!
                  You as weak as a chicken, how can you save my daughter?\""""))
            return 'Game_Over'

        if reply == "Your Majesty: I will use my courage, power, and wisdom!":
            print(dedent("""
                  The king looking at you and said:\"Good! Go!\""""))
            return 'Armory_House'

        else:
            print("The king doesn't understand what you say.")
            print("Say it again.")
            return 'Kingdom_Start'


class armory(object):
    def enter(self):
        print(dedent("""
              You won the king's trust and you were told to visit the local Armory
              to get your weapons. The craftsman looking at you and ask you to defeat
              the one of the kingdom's warriors to show your drafts. If you win, you
              will get your weapon. The battle is begin, the warrior is fat and huge,
              he's coming to you, what are you going to do?"""))

        action = input(">")

        if action == 'punch the fatass in his face! Yoyoyo!':
            print(dedent("""
                  Your arm is like chicken leg and your punch is soft as fuck. At the
                  moment you touched his face, you were grabbed by him like a babydoll.
                  And the fat warrior beat the shit of you."""))
            return 'Game_Over'

        if action == 'dodge his attack like bruce lee! Yeeha!':
            print(dedent("""
                  Are you kidding me? Don't act like a fucking monkey! The fat warrior
                  destroyed your ass and choked you so that you won't make that bruce
                  lee noise any more."""))
            return 'Game_Over'

        if action == 'burger attack!':
            print(dedent("""
                  You brought two big mac burgers from your pocket. You hold the burger
                  and waving the burgers to your opponent. Surprisingly, the fat motherfucker
                  loves burger. You throw the burgers to the other side of the house and he
                  sprint to the burgers, you kicked him in his ass and win the battle!"""))
            return 'Lake_Wizzard'

        else:
            print("The warrior doesn't understand the situation.")
            print("try it again.")
            return 'Armory_House'


class lake(object):
    def enter(self):
        print(dedent("""
              Winning the battle and getting your sword from the armory house. You head to
              the wizzard lake. There's a big wizzard living there and he can help you.
              Because your IQ is too low, you need the wizzard's help to get smarter. The
              wizzard knows that you are the hero who decides to save the princess, so he's
              willing to help. The wizzard asks you to guess the 3 digit number that he's
              come up with in his mind. The number only consists of 1 and 2. You have only 3 attempts."""))

        yourguess = input(">")
        number = f"{randint(1,2)}{randint(1,2)}{randint(1,2)}" #generating 3 random numbers from 1 and 2.
        guesses = 0                                            #set the initial guesses to 0 for looping.

        while yourguess != number and guesses < 6:         #your input vs. the random number. And attempt limits.
            print("NO! Idiot!")
            guesses += 1                                   #reach the maximum limit.
            yourguess = input("So your guess is?> ")

        if yourguess == number:
            print(dedent("""
                  Yes! You are fucking genius! You IQ have just increased by 10000000000000 points."""))
            return 'Forest_Monster'

        else:
            print("You truely a dumbass! fuck off!")
            return 'Lake_Wizzard'

class forest(object):
    def enter(self):
        print(dedent("""
              You've just significantly increased your IQ. Now you are ready to go into the
              horror forest because your high IQ will prevent you from getting lost. However,
              the forest is too dark and evil. You can't do nothing but fight whatever that
              comes into your ugly face. There's a bunch of monsters approaching you,
              what are you going to do?"""))

        action = input(">")

        if action == "run!":
            print(dedent("""
                  Good choice! No surprise that you become clever! But running away will not
                  save the princess!!!!"""))
            return 'Game_Over'

        if action == 'fight!':
            print(dedent("""
                  Good! Very brave, you are a true hero! You swings your sword like a kungfu master and
                  you chopps the monster's head like a No.1 China town chef chopping carrot! wow! what a
                  master!"""))
            return 'Cave_Dragon'

        else:
            print("Don't know what are you doing. Try again.")
            return 'Forest_Monster'


class cave(object):
    def enter(self):
        print(dedent("""
              Finally, you find the cave where the princess was incaged. The cave is huge and dark.
              There's a dragon lives inside the cave and imprisoned the princess. To save the princess
              you have to kill the dragon. So what you gonna do?"""))

        action = input(">")

        if action == "Use my sword to kill it!":
            print(dedent("""
                  You are very brave and you are a true hero. But how can you fight the big dragon right in
                  front your face? Your sword is tiny compare to the dragon and it looks like the dragon's toothpick.
                  But you still go into the fight and try to use your sword to hurt the dragon. As a result, the
                  dragon whipped your ass by using one finger and smashed you into jelly jam. The princess saw all
                  this horrible picture and she passed out to die."""))
            return 'Game_Over'

        if action == "Use my IQ to skill it!":
            print(dedent("""
                  You decide to use the IQ from the wizzard to fight the dragon. Good Try! You ask the dragon to guess
                  the numbers just like you do with the wizzard. However, the dragon can't understand human language.
                  You pissed the dragon off! And you were smashed into jelly jam."""))
            return 'Game_Over'

        if action == "telling a joke in dragon language!":
            print(dedent("""
                  You've learned some dragon language from you grandpa. You told a joke in dragon language:\" bh$$ald du nb
                  ip**& cao ni ma hahah.\" The dragon listened to your joke and laugh the shit of it. The dragon laughed so
                  hard and cannot breath. BOOOOM!! The dragon dead!"""))
            return 'Kingdom_End'

        else:
            print("Don't know what are you doing. Try again.")
            return 'Cave_Dragon'


class kingdomend(object):
    def enter(self):
        print(dedent("""
              The dragon is dead. And you saved the princess from the cave and brought her back to her father. The king
              was so happy to see his daughter and you became the hero of the country. As promised, the king will marry
              the princess to you. The princess is so pretty, looks like 杨超越. You smile like a fucking retarded. You
              know you are the fucking lucky motherfucker! :)"""))
        exit(0)
