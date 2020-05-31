Our game, Incan Gold, is implemented using Python, SQL, HTML, CSS, and Javascript
in a way similar to Finance in the Web Track problem set. The files in our folder set up
a website using CS50 IDE that is able to run full games of Incan Gold, with AIs set up
to play against the player.

To run the game from IDE, navigate to the Incan Gold folder, which contains all of our
files, using “cd incangold” in the terminal. From there, you can open the website that we create in our finals by running
the command “flask run” and then clicking on the line that appears.

If it is your first time visiting our website, please register an account, the username
for which will be used to track your top scores on our leaderboard. You can
then log in with the registered account and access our full website.

If unfamiliar with the rules and gameplay of Incan Gold, please direct your
attention to the “rules” tab, which includes an overview of how gameplay
works, which is important to fully comprehend before playing the actual game.

Once the rules have been absorbed, navigate to the play tab, where you will be
prompted to pick what level of AI you will face in your game (the process of training
these AIs is elucidated in the AI tab of the website). Now, play the game! Per the
rules, you will choose whether to continue in the temple or leave with the loot you
have already gathered each round. Once you leave a round you may have to click continue
several times as the ai players continue to make their moves. After five rounds, a winner
will be crowned (with confetti and all) and the winning score will be entered into the leaderboard.

For grading purposes, all of our html files are in the subfolder templates, and
the images we used are in the subfolder static. The main file is application.py,
which contains most of the logic and implementation of our project, although
incangold.db is also worth examining to see our database logic and tables.
Also included is the ipython notebook where the AIs were trained which unfortunately
is not fully commented.

Thank you for looking at our project! We’re really happy with it.
