# Wheel of Fortune Python Project
from MultiPlayer import PlayerMove, interactions
from partsOfGame import game, bonus, tossup
import os

# Start the entire game with a nice introduction
print(" ")
print(".\ / \ / \ / \ /.".center(os.get_terminal_size().columns))
print("Welcome to Wheel of Fortune".center(os.get_terminal_size().columns))
print("./ \ / \ / \ / \.".center(os.get_terminal_size().columns))
print(" ")


# Get the amount of players that are going to play
NumPlayers = interactions.AmountPlaying(
    "How many players are playing? ", 2, 3)

# Get the names of the players plus saving them into playermove
# Having a loop so it keeps popping up until Number of players is exceeded
NamePlayers = [PlayerMove(input("Enter the names of the player # {} ".format(i+1)))
               for i in range(NumPlayers)]

def FinalWinner():
    FinalWinner = None
    for i in range(NumPlayers):
            NamePlayers[i].RoundBank
            #print("{}: ".format(i), NamePlayers[i].__str__())

            if NamePlayers[i].RoundBank > NamePlayers[1].RoundBank:
                FinalWinner = NamePlayers[i]
            elif NumPlayers == 3:
                if NamePlayers[1].RoundBank > NamePlayers[2].RoundBank:
                    FinalWinner = NamePlayers[i]

    print("\n")
    print("The overall winner is {}".format(FinalWinner))
    return FinalWinner

print("\n")
for i in range(5):
    if i == 0:
        print("Now Playing Toss up")
        tossup(NumPlayers,NamePlayers)
    elif i == 1 or i == 2 or i == 3:
        print("Starting round ", i)
        game(NumPlayers,NamePlayers)
    else:
        final = FinalWinner()
        bonus(final)


'''
THINGS TO FIX:
- when you win, it still says that you lost.
- validation for the consonants and vowels
- time limit (for just the overall round/game or for choices as well?)
'''
