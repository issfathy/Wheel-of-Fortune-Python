# Wheel of Fortune Python Project 
from MultiPlayer import PlayerBasics, colors, interactions
import time
import random
import json

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'

def tossup(Num,Name):

    category, phrase = interactions.CategoryAndPhrase()
    
    guessingWord = []
    lettersdash = ""

    for i in phrase:
        if LETTERS.__contains__(i):
            guessingWord.append('_')
        else:
            guessingWord.append(i)

    for i in guessingWord:
        lettersdash += i

    letterIndex =[]

    print("\n")
    print("Now Playing Toss up")

    while(True):

        # Random generator of numbers from - to len(guessingWord)
        value = random.randint(0, len(phrase) - 1)

        if letterIndex.__contains__(value):
            continue
        else:
            letterIndex.append(value)
            guessingWord[value] = phrase[value]
            time.sleep(1)
            print(*guessingWord)
            answer = input("Type 'A' to guess the phrase or Press 'Enter' to continue: ")
            answer = answer.upper()

            if answer == " ":
                continue
            elif answer == "A":
                print("\n")
                print("The list of players are:")
                for i in range(Num):
                    print("{}: ".format(i), Name[i].listPlayer())
                    
                time.sleep(1)
                PlayerGuess = input("Which player is guessing? e.g. 0,1,2: ")
                player = Name[int(PlayerGuess)]
                    
                print(colors.Green)
                print(player.listPlayer())
                print(colors.White)

                theGuess = input("Your guess is: ")
                
                theGuess = theGuess.upper()
                if theGuess == phrase:
                    time.sleep(1)

                    print("Great job you won $2000")
                    player.addMoney(2000)

                    print(colors.Green)
                    print(player.__str__())
                    print(colors.White)

                    break
                else: 
                    time.sleep(1)
                    print("You got it wrong")
                    continue

        if len(letterIndex) == len(phrase):
            print("No one guessed on this round of toss up")
            break

def ads():
    # Displaying the ads
    print("\n")
    print("A word from our sponsor")
    ads = interactions.displayAds()
    print(" ")

def game(Num,NamePlayers):
    # Setting category and phrase from the json files
    category, phrase = interactions.CategoryAndPhrase()
    

    # When the game winner is found it would turn this into True
    Gamewinner = False

    VOWELS_COST = 250
    ENDLETTERS = ""
    playerSpot = 0
    guessingWord = []
    lettersdash = ""
    letterguessed = []
    guessedSoFar = ""

    # Hiding the phrase
    for i in phrase:
        if LETTERS.__contains__(i):
            guessingWord.append('_')
        else:
            guessingWord.append(i)
            
    for i in guessingWord:
        lettersdash += i

    while(True):

        player = NamePlayers[playerSpot]

        wheel = interactions.WheelSpin()

        # The category to be guessed, is like a clue 
        print("This is the category to be guessed: {}".format(category))  
        print("\n")

        if(ENDLETTERS == ""):
            print("WORDS SO FAR: " + lettersdash)
        else:
            print("WORDS SO FAR: " + ENDLETTERS)


        if wheel["type"] == "bankrupt":
            player.Bankrupt()
            time.sleep(1)
            print("Player {} spun bankrupt".format(player.name))

        elif wheel["type"] == "loseturn":
            print("Player {} spun loseturn".format(player.name))
            time.sleep(1)
            pass
        elif wheel["type"] == "cash":

            print(colors.Green)        
            print("Player {} spun cash prize ${}".format(player.name, wheel["value"]))
            print(colors.White)

            time.sleep(1)
            guess = input("Guess a letter, phrase, or ('Quit'-To quit match or 'Pass'-Move to the next player): ")
            guess = guess.upper()

            if(guess == 'QUIT'):
                print("I'll see you next time")
                break
            elif(guess == 'PASS'):
                print("{} decided to skip to the next player".format(player.name))
                pass
            elif(len(guess) == 1):

                if letterguessed.__contains__(guess):
                    print("{} has already been guessed".format(guess))
                    print("\n")
                    playerSpot = (playerSpot + 1) % len(NamePlayers)
                    continue
                pass     
            
                letterguessed.append(guess)
                guessedSoFar = ""

                if(VOWELS.__contains__(guess) and player.prizeMoney < VOWELS_COST):
                    print("Need ${} to guess a vowel, let's try again".format(VOWELS_COST))
                    continue
                elif(VOWELS.__contains__(guess) and player.prizeMoney > VOWELS_COST):
                    player.vowelCost()

                for i in letterguessed:
                    guessedSoFar += i
                print("LETTERS GUESSED SO FAR: ", guessedSoFar)

                for i in range(len(phrase)):
                    if phrase[i] == guess:
                        guessingWord[i] = guess
                    else:
                        pass

                ENDLETTERS = ""
                for i in guessingWord:
                    ENDLETTERS += i
                
                count = phrase.count(guess)
                if(count > 0):

                    if(count == 1):
                        print("There is one {}. Great Job".format(guess))
                    else:
                        print("There are {} {}'s. Amazing".format(count, guess))

                    # Give them the money and the prizes
                    player.addMoney(count * wheel['value'])
                    if wheel['prize']:
                        player.addPrize(wheel['prize'])

                    # all of the letters have been guessed
                    if ENDLETTERS == phrase:
                        Gamewinner = player
                        break

                    continue  # this player gets to go again

                elif count == 0:
                    print("There are no {} in this phrase".format(guess))
            
            if len(guess) > 1:
                if(guess == phrase):
                    Gamewinner = player
                    count = phrase.count(guess)
                    player.addMoney(wheel['value'] * count)

                    if wheel['prize']:
                        player.addPrize(wheel['prize'])
                    break
                else:
                    print("PHRASE IS WRONG")
                    pass

        playerSpot = (playerSpot + 1) % len(NamePlayers)

        print(colors.Red)
        print("//////////////// End of Turn ////////////////")
        print(colors.White)

    if Gamewinner:
        time.sleep(1)
        print(interactions.winner())
        player.addRoundMoney(Gamewinner.prizeMoney)

        print('{} wins! The phrase was {}'.format(Gamewinner.name, phrase))
        print('Their prize money won is ${}'.format(Gamewinner.prizeMoney))
        print("\n")
        print("The overall money of player {} is ${}".format(Gamewinner.name ,Gamewinner.RoundBank))
        print("\n")

        print("LeaderBoard")        
        for i in range(Num):
            NamePlayers[i].Bankrupt()
            print("{}: ".format(i), NamePlayers[i].__str__())

    else:
        print('Noone has won. The phrase was {}'.format(phrase))
        print('Better luck next time')

    if Gamewinner.prizes:
        print(" ")
        print('{} also won:'.format(Gamewinner.name))
        for prize in Gamewinner.prizes:
            print('    - {}'.format(prize))
    print("\n")

def userChoices(phrase, lettersdash):
    guessingWChoices = []
    choices = []

    for i in range(3):
        while(True):
            con = input("Choose a consonant: ")
            if(VOWELS.__contains__(con.upper())):
                print("Not a consonant, please guess a consonant")
                pass
            else:
                choices.append(con)
                break
    while(True):
        vowel = input("Choose a vowel: ")
        if(VOWELS.__contains__(vowel.upper()) == False):
            print("Not a vowel, please guess a vowel")
        else:
            choices.append(vowel)
            print(" ")
            break
    
    for i in phrase:
        if i == 'R' or i == 'S' or i == 'T' or i == 'L' or i == 'N' or i == 'E':
            guessingWChoices.append(i)
        if i == choices[0].upper() or i == choices[1].upper() or i == choices[2].upper() or i == choices[3].upper():
            guessingWChoices.append(i)
        elif LETTERS.__contains__(i):
            guessingWChoices.append('_')
        else:
            guessingWChoices.append(i)
    lettersdash = " "

    for i in guessingWChoices:
        lettersdash += i

    return lettersdash
    
def bonus(Winner): # only the winner
    print("\n")
    print("YOU'VE ENTERED THE BONUS ROUND")
    # Setting category and phrase from the json files

    def CategoryAndPhrase():
        with open("phrases.json", 'r') as f1:
            phrases = json.loads(f1.read())
            Allcategory = phrases.keys()
            print(" ")
            print("The categorys are:")
            print(*Allcategory)
            print(" ")
            category = input("Which catorgory do you want to guess for the bonus round: ")
            print(" ")
            category = category.upper()
            #category = random.choice(list(phrases.keys()))
            phrase = random.choice(phrases[category])

            return (category, phrase.upper())

    category, phrase = CategoryAndPhrase()
    

    # When the game winner is found it would turn this into True
    Gamewinner = False

    ENDLETTERS = ""
    playerSpot = 0
    guessingWord = []
    lettersdash = ""
    letterguessed = []
    guessedSoFar = ""

    # Hiding the phrase
    for i in phrase:
        if i == 'R' or i == 'S' or i == 'T' or i == 'L' or i == 'N' or i == 'E':
            guessingWord.append(i)
        elif LETTERS.__contains__(i):
            guessingWord.append('_')
        else:
            guessingWord.append(i)
            
    for i in guessingWord:
        lettersdash += i

    lettersdash = userChoices(phrase, lettersdash)

    while(True):
        # For Testing purposes, will not be in the final cut 
        wheel = interactions.BonusSpin()

        # The category to be guessed, is like a clue 
        print("This is the category to be guessed: {}".format(category))  
        print(" ")

        if(ENDLETTERS == ""):
            print("WORDS SO FAR: " + lettersdash)
        else:
            print("WORDS SO FAR: " + ENDLETTERS)

        if wheel["type"] == "cash":
            print(colors.Green) 
            print(Winner)
            print(colors.White)
            print("\n")

            time.sleep(1)
            guess = input("Guess a letter, phrase, or ('Quit'-To quit match or 'Pass'-Move to the next player): ")
            print("\n")
            guess = guess.upper()

            if(guess == 'QUIT'):
                print("I'll see you next time")
                break
            elif(guess == 'PASS'):
                print("{} decided to skip to the next player".format(Winner.name))
                pass
            elif(len(guess) == 1):
                if letterguessed.__contains__(guess):
                    print("{} has already been guessed".format(guess))
                    playerSpot = (playerSpot + 1) % len(Winner)
                    continue
                pass     

                letterguessed.append(guess)
                guessedSoFar = ""

                for i in letterguessed:
                    guessedSoFar += i

                print("LETTERS GUESSED SO FAR: ", guessedSoFar)

                for i in range(len(phrase)):
                    if phrase[i] == guess:
                        guessingWord[i] = guess
                    else:
                        pass

                ENDLETTERS = ""
                for i in guessingWord:
                    ENDLETTERS += i
                
                count = phrase.count(guess)
                if(count > 0):
                    if(count == 1):
                        print("There is one {}. Great Job".format(guess))
                    else:
                        print("There are {} {}'s. Nice one".format(count, guess))

                    # Give them the money and the prizes
                    Winner.addMoney(count * wheel['value'])
                    if wheel['prize']:
                        Winner.addPrize(wheel['prize'])

                    # all of the letters have been guessed
                    if ENDLETTERS == phrase:
                        Gamewinner = Winner
                        break

                    continue  # this player gets to go again

                elif count == 0:
                    print("There are no {} in this phrase".format(guess))
                    continue

            if len(guess) > 1:
                if(guess == phrase):
                    Gamewinner = Winner

                    count = phrase.count(guess)
                    Gamewinner.addMoney(wheel['value'] * count)
                    if wheel['prize']:
                        Gamewinner.addPrize(wheel['prize'])
                    break
                else:
                    print("PHRASE IS WRONG")
                    pass
    if Gamewinner:
        time.sleep(1)
        print(interactions.winner())
        Gamewinner.addRoundMoney(Gamewinner.prizeMoney)

        print('{} wins! The phrase was {}'.format(Gamewinner.name, phrase))
        print('Their prize money won is ${}'.format(Gamewinner.prizeMoney))
        print(" ")
        print("The overall money is ${}".format(Gamewinner.RoundBank))
    else:
        print('Noone has won. The phrase was {}'.format(phrase))
        print('Better luck next time')

    if Gamewinner.prizes:
        print(" ")
        print('{} also won:'.format(Gamewinner.name))
        for prize in Gamewinner.prizes:
            print('    - {}'.format(prize))
    print("\n")
