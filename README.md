# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986)

![screenshot](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/advice.png?raw=true)

## Installation
This is the complete code for an app which could be [hosted on Heroku](https://otree.readthedocs.io/en/latest/server/heroku.html) (that's how we used it). You can establish OTREE_ADMIN_PASSWORD in Heroku Dashboard via Settings > Config Vars, then use that password to create a room when you access the app via its URL. Connecting this app to [Prolific](https://www.prolific.com/) required establishing OTREE_COMPLETION_URL in the same way (copied from your Prolific study) and copying the room URL into your Prolific study.

To test locally, [install otree](https://github.com/oTree-org/otree-core) locally, download this project to a local folder, navigate your command prompt to that folder, and run `otree devserver`. When testing, it can be helpful to set `SKIP_PREGAME = True` in `Instructions/__init__.py` to skip straight to the game.

## Player settings
In `GroupPlayers/__init__.py`, it can be useful to adjust the following constants:
* `PLAYERS_PER_GROUP` (default `5`): The number of players
* `WAIT_LIMIT` (default `1200`): Maximum seconds in the wait room before a player is automatically advanced to the alternate ending (in case there aren't enough people wanting to play)
* `ROBOTS` (default `None`): Specifies which players to replace with robots of which kinds. For example `{2: "A"}` would replace Player2 with a robot that always selects "A". `"default"` refers to all players not otherwise named, so `{"default": "A", 2: None, 3: "B"}` would replace Player3 with a robot that always selects "B", would leave Player2 human, and replace all other players with robots that always select "A". If ROBOTS is not a dictionary, then it is assumed to be specifying a default, so `"A"` is equivalent to `{"default": "A"}`. If all players are replaced with robots, then a simulation will be triggered as soon as any player hits the waiting room (so it can be handy to combine such settings with `SKIP_PREGAME = True`). 
  * `{turntaking}` will be replaced by selections that reserve a unique button for each player with *lowest debt* as described [here](https://arxiv.org/abs/2503.20986). 
  * `{caste}` will be replaced by selections that reserve a unique button for each player with *highest debt* as described [here](https://arxiv.org/abs/2503.20986).
  * `{equalize}` will be replaced by selections that reserve a unique button for each of the *poorest* players.
  * `{rotate}` will be replaced by what the player with the next highest number selected in the previous round (or will match `{caste}` in round 1). If the word "rotate" is followed by a positive integer N, then the selection will copy from the player whose number is N greater (i.e. `{rotate}` means `{rotate1}`)
  * `{random}` will be replaced by a random valid selection. If the word "random" is followed by an integer N > 0 and the robot lost the last round, then the selection has a 1/N probability of shifting to a random button not selected in the previous round (or selected only once, if all buttons were selected); otherwise the selection will repeat. RandomN never skips a round.
  * `{obey}` will be replaced by whatever advice was given to that robot (see ADVICE below).
  * Invalid selections will be relaced with random valid selections.

To specify different selections for different rounds, specify a sequence of selections through which to cycle like `("A", "B", "C")` or use an inner-dictionary to specify the round number in which to switch to a selection like `{4: {4: "B"}}`, which would be equivalent to `{4: ("{obey}", "{obey}", "{obey}", "B", "B", B", "B",`... When using an inner-dictionary, there must be an outer dictionary (which may require specifying `"default"`); if no other selection is specified for round 1, then `"{obey}"` will be assumed. 

In the example below, `{1: "{obey}", 2: "{obey}", 5: "{random3}", "default": {1: "{random3}", 7: "{obey}"}}` was used to see the differences between advising `"{turntaking}"`, `"{equalize}"`, and `"{rotate2}"`. Bot1 and Bot2 always follow the advice; Bot3 and Bot4 delay following it until round 7, and robot 5 never follows the advice. Turntaking, equalize, and rotate, each maximize total bonus with zero disparity when *all* players follow. However, equalize completely forgives Bot3 and Bot4 for delaying obedience (i.e. it offers no incentive against experiments with anti-social behavior); rotate2 does not forgive, but it becomes fragile if even one player deviates. Turn-taking is robust, but may be too complicated for players to master without machine assistance.

![Comparing turn-taking, equalize, and rotate2](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/Robots.png?raw=true)

## Game settings
In `MADChairs/__init__.py`, it can be useful to adjust the following constants:
* `NUM_ROUNDS` (default `20`): How many rounds to repeat the game
* `BUTTONS` (default `('A', 'B', 'C', 'D')`: The button labels. This also determines the number and order of buttons
* `HIDE_SKIP` (default `True`): Hides the ability to skip the round. Allowing players to skip may help clarify when a player has simply given up, and many real-world situations permit players to skip. Players can raise their average payout by coordinating to use this option, so it makes ADVICE and CHAT more compelling. 
* `ADVICE` (default `None`): What to display in the advice column of the history table (if anything). As with ROBOTS, a cycle or dictionary can be used to specify different advice in different rounds. For example, `{8: "Turn={turntaking}; Caste={caste}", 17: None}` would display the turn-taking and caste selections in rounds 8-16 formatted like "Turn=B; Caste=A".
* `HIDE_CHAT` (default `True`): Hides the ability to chat with other players. Chat logs are stored separate from other data, but can be found on the main Data tab of oTree
* `PRIZE` (default `cu(0.25)`): How many British pounds (or server currency) to award players who click a button no other player clicks
* `MAX_HISTORY_DISPLAY` (default `8`): How many round of previous history to display 
* `PLAYER_LABEL` (default `'Player'`): The prefix for player IDs (e.g. "Player1")
* `ROBOT_LABEL` (default `'Bot'`): The prefix when players are replaced with robots (e.g. "Bot1")
* `MAX_TIME` (default `120`): The maximum number of seconds per round
* `BUFFER_INIT` (default `60`): How many seconds to remove from MAX_TIME if players do not request extra time
* `TIMER_DISPLAY_AT` (default `30`): Allow players to request extra time when this many seconds remain
* `TIMER_INCREMENT` (default `30`): How many seconds to add when players request extra time
* `QUESTION_ROUNDS` (default `(2,)`): The round(s) after which to ask users to describe their strategy
* `QUESTION_TIMER` (default `120`): The time limit (in seconds) for describing one's strategy

## Data
Data can be exported in to Excel. Some special data columns of note:
* `participant.skill_rating`: The participant's [trueskill](https://trueskill.org/) rating at the end of the game
* `participant.disconnected`: `1` if the participant was disconnected
* `participant.overwaited`: `1` if the participant never started (i.e. was in the waiting room too long)
* `participant.payoff`: The participant's total winnings across all rounds
* `participant.robot`: The type of robot replacing this player (if any)
* `MADChairs.{round}.player.selection`: What the player selected in that {round}
* `MADChairs.{round}.player.advice`: What advice was displayed to the player
* `MADChairs.{round}.player.secondsElapsed`: How many seconds the player took to make their selection in that round
* `MADChairs.{round}.player.payoff`: How much the player won in that {round}
* `MADChairs.{round}.player.timedOut`: `1` if the player timed-out (so their selection was randomized in that round)
* `MADChairs.{round}.player.debt`: Cumulative debt of favors owed to other players from the first round until that round
* `MADChairs.{round}.player.skill_estimate`: The player's estimated skill based on performance in that and previous rounds
* `MADChairs.{round}.player.strategy`: The player's description of their strategy

## References
You may want to use
* [oTree HR](https://hr.otreehub.com/)
* [Heroku dashboard](https://dashboard.heroku.com/apps)
* [oTree depository](https://github.com/oTree-org/otree-core)
* [oTree documentation](https://otree.readthedocs.io/en/latest/index.html)
