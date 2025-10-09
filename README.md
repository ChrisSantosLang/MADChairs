# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986)

![screenshot](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/advice.png?raw=true)

**Installation:** This is the complete code for an app which could be [hosted on Heroku](https://otree.readthedocs.io/en/latest/server/heroku.html) (that's how we used it). You can establish OTREE_ADMIN_PASSWORD in Heroku Dashboard via Settings > Config Vars, then use that password to create a room when you access the app via its URL. Connecting this app to [Prolific](https://www.prolific.com/) required establishing OTREE_COMPLETION_URL in the same way (copied from your Prolific study) and copying the room URL into your Prolific study.

To test locally, [install otree](https://github.com/oTree-org/otree-core) locally, download this project to a local folder, navigate your command prompt to that folder, and run `otree devserver`. When testing, it can be helpful to set `SKIP_PREGAME = True` in `Instructions/__init__.py` to skip straight to the game.

In `GroupPlayers`, it can be useful to adjust these constants:
* `PLAYERS_PER_GROUP` (default `5`): The number of players (should be at least 5 for four buttons)
* `WAIT_LIMIT` (default `1200`): Maximum seconds in the wait room before a player is automatically advanced to the alternate ending
* `ROBOTS` (default `None`): Specifies which players to replace with robots of which kinds. For example `{2: "A"}` would replace player 2 with a robot that always selects "A". `"all"` means to replace all players with robots making the specified selection. If ROBOTS is not specified as a dictionary, then `"all"` is assumed, so `"A"` is equivalent to `{"all": "A"}`. If all players are replaced with robots, then a simulation will be triggered as soon as any player hits the waiting room (so it can be handy to combine such settings with `SKIP_PREGAME = True`). 
  * `{caste}` and `{turntaking}` will be replaced by the selections recommended by the caste and turn-taking strategies described [here](https://arxiv.org/abs/2503.20986). 
  * `{rotate}` will be replaced by the previous selection of the next player (or by `{caste}` in first round).
  * `{rotate2}` will be replaced by the previous selection of player after the next player (or by `{caste}` in first round).
  * `{equalize}` will be replaced by the selections of a strategy like caste but favoring those with the least accumulated bonus, rather than most debt.
  * `{obey}` will be replaced by whatever advice is given to that robot.
  * Invalid selections will be relaced with random valid selections.

To specify different selections for different rounds, specify a sequence of selections through which to cycle like `{4: ("A", "B", "C")}` or use an inner-dictionary to specify the round number in which to switch to a selection like `{4: {1: "A", 4: "B"}}`, which would be equivalent to `{4: ("A", "A", "A", "B", "B", B", "B",`... When using an inner-dictionary, there must be an outer dictionary (which may require specifying `"all"`), and `"{obey}"` will be assumed for round 1 if not specificied. As examples, the following simulations (with at least 20 rounds) are useful to see that turn-taking does not seek equality (it allows that some past inequities may have been justified), but it pays more reparations than simple rotation would: 
* `ROBOTS = {"all": {1: "{caste}", 7:"{turntaking}"}}`
* `ROBOTS = {"all": {1: "{caste}", 7:"{rotate2}"}}`
* `ROBOTS = {"all": {1: "{caste}", 7:"{equalize}"}}`
Other ways in which `{turntaking}` differs from `{equalize}` and `{rotate}` are to be harder to learn (difficult to apply without help from a computer) and to be more robust against players who refuse to follow it. 

In `MADChairs/__init__.py`, it can be useful to adjust these constants:
* `NUM_ROUNDS` (default `20`): How many rounds to repeat the game
* `MAX_HISTORY_DISPLAY` (default `8`): How many round of previous history to display 
* `PRIZE` (default `cu(0.25)`): How many British pounds (or server currency) to award players who click a button no other player clicks
* `PLAYER_LABEL` (default `'Player'`): The prefix for player ids (e.g. "Player1")
* `ROBOT_LABEL` (default `'Bot'`): The prefix when players are replaced with robots (e.g. "Bot1")
* `MAX_TIME` (default `120`): The maximum number of seconds per round
* `BUFFER_INIT` (default `60`): How many seconds to remove from MAX_TIME if players do not request extra time
* `TIMER_DISPLAY_AT` (default `30`): Allow players to request extra time when this many seconds remain
* `TIMER_INCREMENT` (default v30`): How many more seconds to allow when players request extra time
* `QUESTION_ROUNDS` (default `(2,)`): The rounds after which to ask users to describe their strategy
* `QUESTION_TIMER` (default `120`): The time limit (in seconds) for describing one's strategy
* `HIDE_CHAT` (default `True`): Hides the ability to chat with other players
* `ADVICE` (default `None`): What to display in the advice column. As with ROBOTS, a cycle or dictionary can be used to specify different advice in different rounds. For example, `{8: "Turn={turntaking}; Caste={caste}", 17: None}` would display the turn-taking and caste selections in rounds 8-16 formatted like "Turn=B; Caste=A". 

Some special data columns of note:
* `participant.skill_rating`: The participant's [trueskill](https://trueskill.org/) rating at the end of the game
* `participant.disconnected`: `1` if the participant was disconnected
* `participant.overwaited`: `1` if the participant never started (i.e. was in the waiting room too long)
* `participant.payoff`: The participant's total winnings across all rounds.
* `participant.robot`: The type of robot replacing this player.
* `MADChairs.{round}.player.selection`: What the player selected in that {round}
* `MADChairs.{round}.player.secondsElapsed`: How many seconds the player took to make their selection in that round
* `MADChairs.{round}.player.payoff`: How much the player won in that {round}
* `MADChairs.{round}.player.timedOut`: `1` if the player timed-out (so their selection was randomized in that round)
* `MADChairs.{round}.player.debt`: Cumulative debt of favors owed to other players from the first round until that round
* `MADChairs.{round}.player.skill_estimate`: The player's estimated skill based on performance in that and previous rounds
* `MADChairs.{round}.player.strategy`: The player's description of their strategy
* `MADChairs.{round}.player.advice`: What advice was displayed to the player

You may want to use
* [oTree HR](https://hr.otreehub.com/)
* [Heroku dashboard](https://dashboard.heroku.com/apps)
* [oTree depository](https://github.com/oTree-org/otree-core)
* [oTree documentation](https://otree.readthedocs.io/en/latest/index.html)
