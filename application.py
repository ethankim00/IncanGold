import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import flask

import random
import math
import copy
import pandas as pd
import numpy as np

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///incangold.db")

#route for homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

#route for rules page
@app.route("/rules", methods=["GET"])
@login_required
def rules():
    return render_template("rules.html")

#route for leaderboard page
@app.route("/leaderboard")
@login_required
def leaderboard():

    leaderboards = db.execute("SELECT * FROM winners ORDER by score DESC")
    return render_template("leaderboard.html", leaderboards = leaderboards)

#log existing user in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #set player name for later use
        session["player_name"] = 'Player'
        session["player_name"] = request.form.get("username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#log user out
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#route for about page
@app.route("/about", methods=["GET"])
@login_required
def about():
    return render_template("about.html")

#register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation password has been provided
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Ensure confirmation password and password match
        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("confirmation password and password must match", 403)

        #Insert new user into database
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password_hash)",
                    username=request.form.get("username"),
                    password_hash = generate_password_hash(request.form.get("password")))

        #check if username is available
        if new_user == None:
            return apology("username already taken")

        #Remember which user has logged in
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

#route for AI page
@app.route("/AI", methods=["GET"])
@login_required
def AI():
    return render_template("AI.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


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

#defining the deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        # Insert Dangers
        dangers = ['Mummy', "Fire", "Avalanche", "Serpent", "Spiders"]
        num_dangers = 3
        for danger in dangers:
            for i in range(0, num_dangers):
                self.cards.append(Card(0, danger, None))
        #Insert treasure cards
        treasures = [1,2,3,4,5,5,7,7,9,11,11,13,14,15,17]
        for treasure in treasures:
                self.cards.append(Card(treasure, None, None))
        #Insert Artifacts
        #for i in range (0, num_artifacts_):
        self.cards.append(Card(0, None, True))

    def shows(self):
        for c in self.cards:
            c.show()


    #function to add artifacts to deck
    def add_artifact(self):
        self.cards.append(Card(0, None, True))

    #randomized shuffle of deck
    def shuffle(self):
        for i in range(len(self.cards) -1, 0, -1):
            r = random.randint(0,i)
            #Swap cards
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    #draw cards only when game is active
    def draw (self):
        return self.cards.pop()

#defining player
class Player:
    def __init__(self, player, strat):
        self.name = player
        self.score = 0
        self.loot = 0
        # Variables AI can use to make decisions
        self.number_dangers = 0
        self.num_players = 0
        self.expected_value = 0
        self.leader_score = 0
        self.strat = strat#str(input("Enter Strategy: "))
        self.prob_dying = 0
        # Extra gold to be gained from going back
        self.extra = 0
        self.num_artifacts = 0
        self.round_number = 1
    # Choice of whether to go forward or backward
    # https://gist.github.com/garrettdreyfus/8153571
    # If player type is normal, propmpts user for input, else makes choice based off of AI strategy
    def choose(self):
        if self.strat == "normal":
            while "invalid":
                #print("Make a choice {}".format(self.name))
                #print("Your current score is {}". format(self.score))
                #print("Your current loot is {}\n\n\n\n\n".format(self.loot))
                #check = str(input("Proceed into Temple? (Y/N):")).lower().strip()
                if request.form["choice"] == 'continue':
                    return True
                else:
                    return False
        elif self.strat == "AI Basic":
            a = random.random()
            if a < 0.8:
                return True
            else:
                return False

        elif self.strat == "AI 1rst-Gen":
            if self.loot == 0:
                return True
            if (self.score + self.loot + self.extra) < self.leader_score and self.round_number == 4:
                return True
            b = random.random()
            a = random.random()
            if self.num_artifacts > 0:
                if b > (0.65 - self.extra/100):
                    return False
            if self.number_dangers > 3:
               if a > 0.4:
                   return False

            if a < 0.9:
                return True
            else:
                return False
        elif self.strat == 'AI 2nd-Gen':
            if self.loot == 0:
                return True
            if (self.score + self.loot + self.extra) < self.leader_score and self.round_number == 4:
                return True
            b = random.random()
            a = random.random()
            if (self.score + self.loot + self.extra + 6.6*self.num_artifacts) > self.leader_score + 5 and self.round_number == 4:
                if b > 0.1:
                    return False

            if self.num_artifacts > 0:
                if b > (0.65 - self.extra/100):
                    return False
            if self.number_dangers > 3:
               if a > 0.4:
                   return False
            if self.loot > 10 and self.prob_dying > 0.15:
                if a > 0.2:
                    return False

            if self.num_players < 4:
                if b > (0.2 - .02*self.num_players):
                    return True

            if a < 0.9:
                return True
            else:
                return False


    # Player gains loot from treasure cards
    def add_loot(self, loot_share):
        self.loot += loot_share


    # Player retreats and transfers loot to tent

    def retreat(self):
        # Convert loot to score
        self.score += self.loot
        # Set loot = to 0
        self.loot = 0

    def die(self):
        self.loot = 0


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    if request.method == "POST":

        # Get choice that the user inputed
        player_choice = request.form.get('choice')
        # Get input from all players
        if session['counter'] == 0:
            # Active players will be a list of the indices of the players in self.players who are active
            session['active_players'] = [i for i in range(0, len(session["players_"]))]
            session['deck'] = Deck()
            for i in range(0, session['round_number']):
                session['deck'].add_artifact()
        session["deck"].shuffle()
        if session["round_number"] > 4:
            # Reset number of artifacts
            session["artifacts_taken"] = 0

            # Determine winner
            scores = []
            for player in session['players_']:
                scores.append(player.score)

            #Get Data for Winner page
            session['winner'] = session['players_'][scores.index(max(scores))].name
            session['winner_loot'] = session['players_'][scores.index(max(scores))].score
            scores = []

            #Insert Data into Database
            db.execute("INSERT INTO winners (name, score) VALUES (:name, :score)",
                        name = session["winner"],
                        score = session["winner_loot"])

            #Redirect to Winner Page
            return redirect("/winner")

        session['counter'] += 1
        # List of players who are leaving
        leaving_players = []
        for player in session['active_players']:
            if player != 4:
                choice = session["players_"][player].choose()
                if choice == False:
                    # Update players still in game
                    leaving_players.append(player)
            else:
                if player_choice != 'continue':
                    leaving_players.append(player)
        for player in leaving_players:
            session['active_players'].remove(player)
            #session['left'].append(player)

        # Handle Leaving players
        # session['left']  = []
        # for player in session['left']:
        #     session['left'].append(session['players_'][player])

        #Split Path Treasure and Artifacts
        session["num_leaving"] = len(leaving_players)
        if session["num_leaving"] != 0:
            leaving_split = math.floor(session["extra"]/session["num_leaving"])
            if session["num_artifacts"] != 0:
                artifact_split = math.floor(session["num_artifacts"]/session["num_leaving"])
                session["artifacts_taken"] = session["artifacts_taken"] + session["num_artifacts"]
                if artifact_split !=0:
                    session["num_artifacts"] = session["num_artifacts"] % artifact_split
            else:
                artifact_split = 0
        else:
            leaving_split = 0
        if leaving_split != 0:
            session["extra"] = session["extra"] % leaving_split

        #Add Treasure to Loot Piles
        for player in leaving_players:
            session["players_"][player].add_loot(leaving_split)
            if  session["artifacts_taken"] < 4:
                session["players_"][player].add_loot(5 * artifact_split)
                session["players_"][player].retreat()
            else:
                session["players_"][player].add_loot(10 * artifact_split)
                session["players_"][player].retreat()

        # Make sure there are players still active
        session["num_players"] = len(session['active_players'])
        if (session["num_players"] == 0):
            # move onto the next round
            session["round_number"] += 1
            # Reset active players
            active_players =  [i for i in range(0, len(session["players_"]))]
            # Reset other variables
            session["counter"] = 0
            session["value"] = 124
            # Shuffle the Deck
            session["deck"].add_artifact()
            session["deck"].shuffle()
            session["extra"] = 0
            #Present Dangers in the Round
            session["dangers_"] = []

        session['players_left'] = []
        for player in session['active_players']:
            session['players_left'].append(session["players_"][player])
        session["card"] = session["deck"].draw()
        # If danger update danger
        if session["card"].danger != None:
            # If death end round
            if session["card"].danger in session["dangers_"]:
                #print("You died to {}".format(card.danger))
                for player in session['active_players']:
                    session["players_"][player].die()
                session["round_number"] += 1
                active_players =  [i for i in range(0, len(session["players_"]))]
                # Reset other variables
                session["counter"] = 0
                session["value"] = 124
                # Add an artifact to the deck
                session["deck"].add_artifact()
                # Shuffle the deck
                session["deck"].shuffle()
                session["extra"] = 0
                #Reset Dangers in the Round
                session["dangers_"] = []

                session['players_left'] = []

                death = "Death to {}".format(session["card"].danger)

                # Add you died to this
                return render_template("play.html", dangers = session['dangers_'], gold_on_path = session['extra'], artifacts_on_path = session['num_artifacts'], artifacts_collected = session['artifacts_taken'], players = session['players_'], card_value = death, choice = session["player_choice"], round_number = session['round_number'], loot = session['players_'][4].loot, left = session['players_left'])

            else:
                session["dangers_"].append(session["card"].danger)
        # If card is artifact, print number of artifacts.

        if session["card"].artifact:
            session["num_artifacts"] += 1

        # If treasure split treasures
        if session["num_players"] > 0:
            split = math.floor(session["card"].points / session["num_players"])

        # Add loot for active players
        for player in session['active_players']:
            session["players_"][player].add_loot(split)
        # Update treaure on path
        if session["num_players"] > 0:
            session["extra"] += (session["card"].points % session["num_players"])

        # Calculate Expected value of next card
        session["value"] = session["value"] - session["card"].points
        # 30 - counter is the number of cards left in deck
        ev = session["value"]/(30 - session["counter"])
        # Calculate score of player in the lead
        session["scores"] = []
        for player in session["players_"]:
            session["scores"].append(player.score)
        prob_dying = (2*len(session["dangers_"]))/(30-session["counter"])
        # Update player objects with information that they can make decicions off of
        for player in session['active_players']:
            session["players_"][player].number_dangers = len(session["dangers_"])
            session["players_"][player].num_players = len(session['active_players'])
            session["players_"][player].expected_value = ev
            session["players_"][player].leader_score = max(session["scores"])
            session["players_"][player].prob_dying = prob_dying
            session["players_"][player].extra = session["extra"]
            session["players_"][player].num_artifacts = session["num_artifacts"]
            session["players_"][player].round_number = session["round_number"]


        if session["card"].points != 0:
            card_ = 'Treasure value: {}'.format(session["card"].points)
        elif session["card"].danger != None:
            card_ = 'Danger: {}'.format(session["card"].danger)
        elif session["card"].artifact == True:
            card_ = 'Artifact'

        return render_template("play.html", dangers = session['dangers_'], gold_on_path = session['extra'], artifacts_on_path = session['num_artifacts'], artifacts_collected = session['artifacts_taken'], players = session['players_'], card_value = session['card'].points, choice = session["player_choice"], round_number = session['round_number'], loot = session['players_'][4].loot,  left = session['players_left'])

    else:
        #Global variables

        #Creating Deck
        session['deck'] = Deck()
        session['deck'].shuffle
        session["extra"] = 0

        #session['left'] = []

        #Setting Up Variables
        session["card_"] = 'Top of Deck'
        session["player_choice"] = 'start of game'
        session["artifacts_taken"] = 0
        session["num_artifacts"] = 0
        session['counter'] = 0

        # Total Value of all treasure cards
        session["value"] = 124

        #Round Number
        session["round_number"] = 0

        #Players
        session["players"] = ['Rodrigo', 'David', 'Brian', 'Emma', session["player_name"]]
        #AI Strategiess
        session['players_left'] = []

        session["players_"] = []
        session["dangers_"] = []
        for i in range(0, 5):
            player = Player(session["players"][i], session["strategies"][i])
            session["players_"].append(player)

        #Move onto Playing Game
        return render_template("play.html", dangers = session['dangers_'], gold_on_path = session['extra'], artifacts_on_path = session['num_artifacts'], artifacts_collected = session['artifacts_taken'], players = session['players_'], card_value = 0, choice = session["player_choice"], round_number = session['round_number'], loot = session['players_'][4].loot,  left = session['players_left'])

@app.route("/setup", methods=["GET", "POST"])
@login_required
def setup():
    if request.method == "POST":
        choice = request.form.get('level')
        if choice == 'Easy':
            session["strategies"] = ['AI Basic', 'AI Basic', 'AI Basic', 'AI Basic', 'normal']
        elif choice == 'Intermediate':
            session["strategies"] = ['AI 1rst-Gen', 'AI 1rst-Gen', 'AI 1rst-Gen', 'AI Basic', 'normal']
        else:
            session["strategies"] = ['AI 2nd-Gen', 'AI 2nd-Gen', 'AI 1rst-Gen', 'AI 1rst-Gen', 'normal']

        return redirect("/play")
    else:
        return render_template("setup.html")

@app.route("/winner", methods=["GET", "POST"])
@login_required
def winner():
    return render_template("winner.html",Loot = session['winner_loot'] , Winner = session['winner'])

