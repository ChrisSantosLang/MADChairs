# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986)

**Installation:** This is the complete code for an app which could be [hosted on Heroku](https://otree.readthedocs.io/en/latest/server/heroku.html) (that's how we used it). You can establish OTREE_ADMIN_PASSWORD in Heroku Dashboard via Settings > Config Vars, then use that password to create a room when you access the app via its URL. Connecting this app to [Prolific](https://www.prolific.com/) required establishing OTREE_COMPLETION_URL in the same way (copied from your Prolific study) and copying the room URL into your Prolific study.

Some constants you can change easily in `MADChairs/__init__.py`:
* PLAYERS_PER_GROUP: The number of players (should be at least 5 for four buttons)
* NUM_ROUNDS: How many rounds to repeat the game
* MAX_HISTORY_DISPLAY: Display this many round of previous history 
* PRIZE: How many British pounds (or server currency) to award players who click a button no other player clicks
* PLAYER_LABELS: A tuple of displayed names
* MAX_TIME: The maximum number of seconds per round
* BUFFER_INIT: How many seconds to remove from MAX_TIME if players do not request extra time
* TIMER_DISPLAY_AT: Allow players to request extra time when this many seconds remain
* TIMER_INCREMENT: How many more seconds to allow when players request extra time
* QUESTION_TIMER: How many seconds to allow for the question after round 2
* WAIT_LIMIT: Maximum seconds in the wait room before a player is automatically advanced to the alterate ending

Some specal data columns of note:
* participant.skill_rating: The participant's [trueskill](https://trueskill.org/) rating at the end of the game
* participant.disconnected: "1" if the participant was disconnected
* participant.payoff: The participant's total winnings across all rounds.
* MADChairs.{round}.player.selection: What the player selected in that {round}
* MADChairs.{round}.player.secondsElapsed: How many seconds the player took to make their selection in that {round}
* MADChairs.{round}.player.payoff: How much the player won in that {round}
* MADChairs.{round}.player.timedOut: "1" is the player timed-out so selection was randomized in that {round}
* MADChairs.{round}.player.debt: Cumulative debt of favors owed to other players from the first round until that {round}
* MADChairs.{round}.player.skill_estimate: The player's estimated skill based on peformance in that and previous {rounds}
* MADChairs.{round}.player.strategy: The player's description of their strategy

You may want to use
* [oTree hub](https://www.otreehub.com/)
* [oTree HR](https://hr.otreehub.com/)
* [Heroku dashboard](https://dashboard.heroku.com/apps)
