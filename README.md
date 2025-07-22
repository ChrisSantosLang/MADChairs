# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986)

Some constants you can change easily in `MADChairs/__init__.py`:
* PLAYERS_PER_GROUP: The number of players (should be at least 5 for four buttons)
* NUM_ROUNDS: How many rounds to repeat the game
* MAX_HISTORY_DISPLAY: Display this many round of previous history 
* PRIZE: How many dollars (or server currency) to award players who click a button no other player clicks
* PLAYER_LABELS: A tuple of displayed names
* MAX_TIME: The maximum number of seconds per round
* BUFFER_INIT: How many seconds to remove from MAX_TIME if players to not request extra time
* TIMER_DISPLAY_AT: Allow players to request extra time when this many seconds remain
* TIMER_INCREMENT: How many more seconds to allow when players request extra time

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

You may want to use
* [oTree hub](https://www.otreehub.com/)
* [oTree HR](https://hr.otreehub.com/)
* [Heroku dashboard](https://dashboard.heroku.com/apps)
