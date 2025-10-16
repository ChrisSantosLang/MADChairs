# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986)

![screenshot](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/advice.png?raw=true)

## Installation
This is the complete code for an app which could be [hosted on Heroku](https://otree.readthedocs.io/en/latest/server/heroku.html) (that's [how we used it](https://download.ssrn.com/2025/10/13/5599171.pdf?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCboYFOJ34w8MpZtH16qOJFrlzCKuJ0aE5w4PvvbJRApAIhALCLOXSfqpvp4AywFYpfWUs%2BMEez9zA2jCY0buLnxcIeKsYFCJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBBoMMzA4NDc1MzAxMjU3IgzaMKvRsn%2FSa%2BfkjM4qmgWgm1PbuL2YPvaZ1mXJxa5Hlht1SCgr%2Bc107MOv5sCLDr5cBjpg3XoNobDOVxtKSPTi0dOtZCV78wh3gcYZEo%2B4d7HSKmXhTF43FyCYnT2Zi3tsAZnYNisK%2F3Nd%2Fhz%2FH6n1FyQUpmmuEevLWA%2Fw3il1lX62ab%2F3ludTN1bBUcGP84OO9UwbKSmmWMM2yedHDZLMQdg1to5JojfpSYsNaBHQfdSTFng2D5XQcoXPrCD3gEqUgXx2dqOzepd16EDoklPmBYZV7GWHUgjjl%2FrZuWKMRZ9a8QKwT%2FHHtt94oh3K4ZWkdlB1OqAPTPuCi4OF4%2FZzNqw5QKCwIlKpL5Q8nrwWTw%2Bq4TJClRwtwbReFxp9CNXeoAHKiI3hmmTsRUDnCU2%2BFQmSrp9wyJfaha1CsWkJAi2UofjGKZZvcU%2FtSf6hjtbYpVW7YOnneU4FIkwW%2Fs5Eb2y%2BfoEO3UkrzMviSWPIVUBPTfijkg8HNKQzvclu2BQc0BMFMPEMZuRQ0SyYxesF8y%2FErg5fX%2BLH6C9m0XPb4gi2G8GAlQncDkUufkM%2FPI36Pv5sTQqL6jSY7CIN1woh61nvbmjNF4%2FNOf36bupldjVPfAKkbk6EJh9ToRnT555oL5%2BwnPwj6PAxpQdd6A7JgSU92iJ%2FmJIl3Xms2gdJ113UdFgXdb83YX6RopjblgVUYp0%2Bhd%2Fs7S41xxlv90uOx3YyDevkfho4QsOiaIgWusQBqJm9pCyGExjvUFX83V7ZrFKam4j317OO3e0FPbVx9Pb%2FJmHQcRYQOgqEkegFlqxU2NplRw4hqoZH0kFWKG%2FCwMToeVtpgGqXya4mSEXR8hXKGFIOdVEua64V0oR83AC7UVf%2FCyfx3VyDhfIOg5k8jKxn8nPYUJkwlo7FxwY6sAE5vgdpyQLUEQBuTeumAi8EQrBjF%2FHANiLFYkcsky7N5X8Ybi2eNfUJL2zqpEW0lblqe20KAkoRglLS%2BmmhBGVyH9vvKxooKvANgTzULz1ioWdSIkOteO7FnV9y9mJpDLtIg19Ru%2FfsYY3qMuOctSx5IXkJjbOgpvmVWj0h7HYz0lS%2Bef9gRbv2NJ7zUvIuPO14UBq4DOAct%2FMzPRtOdm%2Bj2A5IuvGzUjR5KsOHUKVn4w%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20251016T194352Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAUPUUPRWESNMG5PRC%2F20251016%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=c3499472a8204a7364d9c80f5430936b3321b8b4d7da8c9bb03d15a933e5a1db&abstractId=5599171)). You can establish OTREE_ADMIN_PASSWORD in Heroku Dashboard via Settings > Config Vars, then use that password to create a room when you access the app via its URL. Connecting this app to [Prolific](https://www.prolific.com/) required establishing OTREE_COMPLETION_URL in the same way (copied from your Prolific study) and copying the room URL into your Prolific study.

To test locally, [install otree](https://github.com/oTree-org/otree-core) locally, download this project to a local folder, navigate your command prompt to that folder, and run `otree devserver`. When testing, it can be helpful to set `SKIP_PREGAME = True` in `Instructions/__init__.py` to skip straight to the game.

## Player settings
In `GroupPlayers`, it can be useful to adjust these constants:
* `PLAYERS_PER_GROUP` (default `5`): The number of players (should be at least 5 for four buttons)
* `WAIT_LIMIT` (default `1200`): Maximum seconds in the wait room before a player is automatically advanced to the alternate ending
* `ROBOTS` (default `None`): Specifies which players to replace with robots of which kinds. For example `{2: "A"}` would replace Player2 with a robot that always selects "A". `"default"` refers to al players not otherwise named, so `{"default": "A", 2: None, 3: "B"}` would replace Player3 with a robot that always selects "B", would leave Player2 human, and replace all other players with robot that always select "A". If ROBOTS is not specified as a dictionary, then it is assumed to be specifying a default, so `"A"` is equivalent to `{"default": "A"}`. If all players are replaced with robots, then a simulation will be triggered as soon as any player hits the waiting room (so it can be handy to combine such settings with `SKIP_PREGAME = True`). 
  * `{turntaking}` will be replaced by selections that reserve a unique button for each player with *lowest* debt as described [here](https://arxiv.org/abs/2503.20986). 
  * `{caste}` will be replaced by selections that reserve a unique button for each player with *highest* debt as described [here](https://arxiv.org/abs/2503.20986). 
  * `{equalize}` will be replaced by selections that reserve a unique button for each of the *poorest* players. 
  * `{rotate}` will be replaced by the initial caste selections rotated N positions per round. If no positive integer N is appended (e.g. `{rotate1}`), then N is assumed to be 1.
  * `{random}` will be replaced by a random valid selection. If an integer N > 0 is appended (e.g. `{random1}`), and the player lost the last round, then it will have 1/N probability of shifting to a random button not selected in the previous round (or selected only once, if all buttons were selected); otherwise the selection will repeat. 
  * `{obey}` will be replaced by whatever advice was given to that robot (see ADVICE below). If a positive integer N is appended (e.g. `{obey1}`) it will be relaced by the advice assigned to the player with N higher ID.
  * Invalid selections will be relaced with random valid selections.

To specify different selections for different rounds, specify a sequence of selections through which to cycle like `("A", "B", "C")` or use an inner-dictionary to specify the round number in which to switch to a selection like `{4: {4: "B"}}`, which would be equivalent to `{4: ("{obey}", "{obey}", "{obey}", "B", "B", B", "B",`... When using an inner-dictionary, there must be an outer dictionary (which may require specifying `"default"`), and `"{obey}"` will be assumed for round 1 if no other selection is specified. As examples, `{3: {3: "D", 4: "D", 5: "{obey}"}, "default": "{obey}"}` was used to run the following experiments with advice of `"{rotate}"`, `"{caste}"`, `"{equalize}"`, and `"{turntaking}"` to see the consequences of deviating from different kinds of advice:

![Comparing turn-taking, equalize, and rotate2](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/Robots.png?raw=true)

To deviate from `"{rotate}"` results in losses for the deviant and victims of collision. To deviate from `"{caste}"` also results in losses for the deviant and victims, and the deviant shifts to the bottom caste (a potentially endless loss). The losses dues to deviation from `"{equalize}"` are shared by the entire population (leaving no incentive against deviation). To deviate from `"{turntaking}"` results in losses for the deviant, and remaining losses are shared by the entire population. `"{turntaking}"` is the only norm the penalizes players who deviate when assigned to skip. 

The following table shows the average % of maximum bonus accumulated in a team of three bots competing for five buttons against another team of three bots that occupied the even slots and played as specified in the column label. Italic numbers represent situations in which players had incentive to defect either because they were suppressed by their teammates (red) or achieved significantly lower bonuses than their opponents.  

![Comparing norms by mixing equal populations](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/mixes.png?raw=true)

`"{turntaking}"` dominated every norm other than `"{equalize}"`. `"{equalize}"` dominated `"{random3}"` which dominated `"{rotate}"` which dominated `"{equalize}"`. `"{caste}"`, `"{random3}"`,  and `"{rotate0}"` all proved very unstable due to internal inequity, but `"{caste}"` was the least-often dominated. `"{random}"` was dominated by all other norms in this comparison.

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
