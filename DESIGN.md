We implemented our project in a way similar to finance using python to run the game logic
and html templates to make up the website, with SQL databases to back up the python. There
were several critical decisions we made during the design process.

We used python classes to define most of our functions, to make the code sleeker and easier
to understand. We decided to make classes for the deck of cards, individual cards, and players
that we could then manipulate to actually run the game.

First, we had to decide whether we wanted to allow multiple human-controlled players
in each game. Instead, we decided that spending time on the AI would make for a more
interesting project and game. If interested in how we designed the AI, refer to AI.html
in the folder or on the website.

We ran into a roadblock midway through the project when we discovered that it was hard
to update the user via html on the current game state. We only had one template (play.html)
that had to be reloaded and updated every time the player made a choice and the game state
advanced to the next time the player made a choice. We hit upon the solution of storing
variables in session in order to conveniently store them while reloading the html page.
Much like the user_id is stored, many of our “global” variables are stored in session.

We ended up using a SQL database for both users and our leaderboard because it was the
simplest way to store that data between users on our website. We also considered making
the deck a SQL database but eventually figured out a way to make the deck in Python.

Ultimately we ran out of time to fully implement to AI. The decision making models are fitted in a separate Jupyter notebook using Sklearn.
For the game implementation we hard coded strategies for the 1rst and 2nd generation AI. The AI players make informed decisions 
based on the spefific game situation with a little bit of randomness added to make things interesting. 

