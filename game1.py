import random
import math
import copy
#import pandas as pd
#import numpy as np

# Create class for our different cards
class Card:
    def __init__(self, points, danger, artifact):
        # Number of points
        self.points = points
        # Type of danger (choose from 5)
        self.danger = danger
        # Is it an artifact or not
        self.artifact = artifact


    def show(self):
        # Show value of card:
        if self.points != 0:
            print("Treasure! Value: {}".format(self.points))
        if self.danger != None:
            print("Danger: {}".format(self.danger))
        if self.artifact:
            print("Artifact")


dangers = ['Mummy', "Fire", "Avalanche", "Serpent", "Spiders"]

num_dangers = 3

num_artifacts = 4


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        # Insert Dangers
        for danger in dangers:
            for i in range(0, num_dangers):
                self.cards.append(Card(0, danger, None))
        #Insert treasure cards
        treasures = [1,2,3,4,5,5,7,7,9,11,11,13,14,15,17]
        for treasure in treasures:
                self.cards.append(Card(treasure, None, None))
        #Insert Artifacts
        for i in range (0, num_artifacts):
            self.cards.append(Card(0, None, True))

    def shows(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        for i in range(len(self.cards) -1, 0, -1):
            r = random.randint(0,i)
            #Swap cards
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
    def draw (self):
        return self.cards.pop()




# Look at next card and update gameplay accordingly

class Player:
    def __init__(self):
        self.name = str(input("Enter Name: "))
        self.score = 0
        self.loot = 0
        self.strat = str(input("Enter Strategy: "))

    # Choice of whether to go forward or backward
    # https://gist.github.com/garrettdreyfus/8153571

    # If player type is normal, propmpts user for input, else makes choice
    # based off of AI strategy
    def choose(self):
        if self.strat == "normal":
            while "invalid":
                print("Make a choice {}".format(self.name))
                print("Your current score is {}". format(self.score))
                print("Your current loot is {}\n\n\n\n\n".format(self.loot))
                check = str(input("Proceed into Temple? (Y/N):")).lower().strip()
                if check[0] == 'y':
                    return True
                elif check[0] == 'n':
                    return False
                else:
                    print('Invalid Input')
        else:
            #Run strat function to get choice made by AI
            return False


    # Player gains loot from treasure cards
    def add_loot(self, loot_share):
        self.loot += loot_share


    # Player retreats and transfers loot to tent

    def retreat(self):

        self.score += self.loot
        self.loot = 0

    def die(self):
        self.loot = 0


# Game engines runs a game
class Game:
    # Input number of players
    def __init__(self, player_number):
        self.players = []
        for i in range(0, player_number):
            player = Player()
            self.players.append(player)
        # Create player object for each player

        # Round function
    def Round(self,round_number):
        # Build and shuffle a deck
        deck = Deck()
        deck.shuffle()
        extra = 0
        dangers_ = []
        num_artifacts = 0
        counter = 0
        # Repeat until all players ha`ve left or death occurs
        while "round is active":
        # Get input from all players
            if counter == 0:
                # Active players will be a list of the indices of the players in self.players who are active
                active_players = [i for i in range(0, len(self.players))]

            counter += 1
            # List of players who are leaving
            leaving_players = []

            for player in active_players:
                choice = self.players[player].choose()
                print(active_players)
                if choice == False:
                    # Update players still in game
                    leaving_players.append(player)
                    # Remove player from active players
                    # Why is this removing from self.players as well
            for player in leaving_players:
                active_players.remove(player)
            # Handle Leaving players
            num_leaving = len(leaving_players)
            if num_leaving != 0:
                leaving_split = math.floor(extra/num_leaving)
                if num_artifacts != 0:
                    artifact_split = math.floor(num_artifacts/num_leaving)
                    if artifact_split !=0:
                        num_artifacts = num_artifacts % artifact_split
                else:
                    artifact_split = 0
            else:
                leaving_split = 0
            if leaving_split != 0:
                extra = extra % leaving_split
            for player in leaving_players:
                self.players[player].add_loot(leaving_split)
                self.players[player].add_loot(5 * artifact_split)
                self.players[player].retreat()
            # Make sure there are players still active
            num_players = len(active_players)
            if (num_players == 0):
                active_players =  [i for i in range(0, len(self.players))]
                return False
            # Draw card off of deck
            card = deck.draw()
            card.show()
            # If danger update danger
            if card.danger != None:
                # If death end round
                if card.danger in dangers_:
                    print("You died to {}".format(card.danger))
                    for player in active_players:
                        self.players[player].die()
                    active_players = [i for i in range(0, len(self.players))]
                    return False
                else:
                    dangers_.append(card.danger)
            # If card is artifact, print number of artifacts.

            if card.artifact:
                num_artifacts += 1

            # If treasure split treasures
            split = math.floor(card.points / num_players)
            for player in active_players:
                self.players[player].add_loot(split)
            # Update treaure on path
            extra += (card.points % num_players)


            # Update players on current status
            print(" There amount of treasure on the path is {}".format(extra))
            print("The current dangers are:")
            for danger in dangers_:
                print('{}'.format(danger))
            print("There are this many artifacts on the path: {}".format(num_artifacts))




    # Run Appropriate Number of Rounds
    def play_game(self):

        # Run 4 Rounds
        for i in range(0,2):
            self.Round(i+1)

        scores = []
        print(self.players)
        for player in self.players:
            print("{} has {} points".format(player.name, player.score))
            scores.append(player.score)

        scores.index(max(scores))
        print("Winner is {}".format(self.players[scores.index(max(scores))].name))


    # Tally scoress and declare winner.


# Implements a single round of the game

# object or function??
 # list of player objects


a = Game(3)
a.play_game()
