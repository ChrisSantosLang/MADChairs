# MADChairs
Code for an [oTree](https://otree.readthedocs.io/en/latest/index.html) server to play the [MAD Chairs game](https://arxiv.org/abs/2503.20986) (a.k.a. the [Lifeboat Problem](https://www.sciencedirect.com/science/article/pii/S0014292111001231?casa_token=Lk71pF1iix4AAAAA:4tvPXdyzSc6Nh0UzddxhizMqx3xNA1U7PSeArEcQvWUUD32aH2duyonpB1DqeHfiBXhw-7Vy4i4)). This game is a metaphor for real-world division of scarce resources including division of jobs, hospital beds, and spaces in traffic. One important application is the division of opportunity to have voice in a conversation. Representative democracies, for example, explicitly establish a limited set of channels through which citizens can have voice in their government, and any of those channels can be overcrowded. 

![screenshot](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/advice.png?raw=true)

The "Advice" column in the bottom section is optional (and can show each player multiple recommendations). Each previous selection is followed by what was advised (in parentheses) to that player for that round and is underlined if no other player clicked the same button in that round. The "Bonus" column displays each player's accumulated winnings thus far.

## Installation
This is the complete code for an app which could be [hosted on Heroku](https://otree.readthedocs.io/en/latest/server/heroku.html) (that's [how we used it](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5599171)). You can establish OTREE_ADMIN_PASSWORD in Heroku Dashboard via Settings > Config Vars, then use that password to create a room when you access the app via its URL. Connecting this app to [Prolific](https://www.prolific.com/) required establishing OTREE_COMPLETION_URL in the same way (copied from your Prolific study) and copying the room URL into your Prolific study.

To test locally, [install otree](https://github.com/oTree-org/otree-core) locally, download this project to a local folder, navigate your command prompt to that folder, and run `otree devserver`. When testing, it can be helpful to set `SKIP_PREGAME = True` in `Instructions/__init__.py` to skip straight to the game.

## Player settings
In `GroupPlayers`, it can be useful to adjust these constants:
* `PLAYERS_PER_GROUP` (default `5`): The number of players (should be at least 5 for four buttons)
* `WAIT_LIMIT` (default `1200`): Maximum seconds in the wait room before a player is automatically advanced to the alternate ending
* `ROBOTS` (default `None`): Specifies which players to replace with robots of which kinds. For example `{2: "A"}` would replace Player2 with a robot that always selects "A". `"default"` refers to all players not otherwise named, so `{"default": "A", 2: None, 3: "B"}` would replace Player3 with a robot that always selects "B", would leave Player2 human, and replace all other players with robots that always select "A". If ROBOTS is not specified as a dictionary, then it is assumed to be specifying a default, so `"A"` is equivalent to `{"default": "A"}`. If all players are replaced with robots, then a simulation will be triggered as soon as any player hits the waiting room (so it can be handy to combine such settings with `SKIP_PREGAME = True`). 
  * `{random}` will be replaced by a random valid selection. If an integer N > 0 is appended (e.g. `{random1}`), and the player lost the last round, then it will have 1/N probability of shifting to a random button not selected in the previous round (or selected only once, if all buttons were selected); otherwise the selection will repeat. `{random3}` may be an idealized version of initial observed human play.
  * `{caste}` will be replaced by selections that reserve a unique button for each player with *highest* debt as described [here](https://arxiv.org/abs/2503.20986). 
  * `{turntaking}` will be replaced by selections that reserve a unique button for each player with *lowest* debt as described [here](https://arxiv.org/abs/2503.20986). 
  * rotate is the kind of turn-taking that is unresponsive to deviation. `{rotate}` will be replaced by the initial caste selections rotated 1 position per round. If a positive integer N is appended (e.g. `{rotate2}`), then it will rotate N positions per round.
  * `{radicaleq}` will be replaced by selections that reserve a unique button for each of the *poorest* players (i.e., whichever players have the highest bonus thus far are assigned to lose a given round). 
  * `{equalize}` is like radicaleq except that deviants are (temporarily) excluded from the list of poorest players. Any history of deviance is gradually forgotten, so any player can rejoin the list by repeatedly following the equalize strategy, but keeping track of who to punish (like keeping track of debt used in caste and turntaking strategies) may require the help of a computer.   
  * `{obey}` will be replaced by whatever advice was given to that robot (see ADVICE below). 
  * Invalid selections will be relaced with random valid selections.

To specify different selections for different rounds, specify a sequence of selections through which to cycle like `("A", "B", "C")` or use an inner-dictionary to specify the round number in which to switch to a selection like `{4: {4: "B"}}`, which would be equivalent to `{4: ("{obey}", "{obey}", "{obey}", "B", "B", B", "B",`... When using an inner-dictionary, there must be an outer dictionary (which may require specifying `"default"`), and `"{obey}"` will be assumed for round 1 if no other selection is specified. As examples, values like `{'default':'{obey}', 2: {2:'A', 3:'{obey}'}}` were used to run experiments measuring the consequences of a single deviation when following the advice of `"{rotate}"`, `"{radicaleq}"`, `"{equalize}"`, or `"{turntaking}"`:

![Comparing turn-taking, equalize, and rotate2](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/Robots.png?raw=true)

All four of these strategies have been called "turn taking" because they all yield optimal results when no player ever deviates, but the differences between these kinds of turn taking become apparent under deviation. `"{rotate}"` is a very simple strategy, but it does nothing to penalize deviance, and any player assigned to lose would lose if they don't deviate, so the costs of their deviance are born entirely by the victims with whom they collide. If carelessness would be problematic, `"{rotate}"` fails to discourage it. Even though `"{equalize}"` immediately punishes deviance, it aims to equalize total outcomes, so all players share equally in the costs of deviance (ending-up the same as `"{radicaleq}"` in the long-run). They discourage carelessness to some extent (but to negligible degree when there are enough other players). Only the strategy we have officially named `"{turntaking}"` disproportionately penalizes deviance, bringing justice and stability when conflict is inevitable.

The following table shows the average portion of maximum bonus accumulated in a team of three bots that played as specified in the row label (occupying the odd positions) competing for five buttons against another team of three bots that played as specified in the column label (occupying the even positions). Italic numbers represent situations in which players had incentive to defect either because they were suppressed by their teammates (red) or achieved significantly lower bonuses than their opponents.  

![Comparing norms by mixing equal populations](https://github.com/ChrisSantosLang/MADChairs/blob/main/Media/mixes.png?raw=true)

`"{turntaking}"` dominated every norm other than `"{equalize}"`. `"{equalize}"` dominated `"{random3}"` which dominated `"{rotate}"` which dominated `"{equalize}"`. `"{caste}"`, `"{random3}"`,  and `"{rotate0}"` all proved very unstable due to internal inequity, but `"{caste}"` was less-often dominated than the other two. `"{random}"` was dominated by all other norms in this comparison.

## Game settings
In `MADChairs/__init__.py`, it can be useful to adjust the following constants:
* `NUM_ROUNDS` (default `20`): How many rounds to repeat the game
* `BUTTONS` (default `('A', 'B', 'C', 'D')`: The button labels. This also determines the number and order of buttons
* `HIDE_SKIP` (default `True`): Hides the ability to skip the round. Many real-world situations permit players to skip. Players can raise their average payout by coordinating about skipping, so the option to skip makes ADVICE and CHAT more compelling. 
* `ADVICE` (default `None`): What to display in the advice column of the history table (if anything). As with ROBOTS, a cycle or dictionary can be used to specify different advice in different rounds. For example, `{8: "Turn={turntaking}; Caste={caste}", 17: None}` would display the turn-taking and caste selections in rounds 8-16 formatted like "Turn=B; Caste=A".
* `HIDE_CHAT` (default `True`): Hides the ability to chat with other players. Chat logs can be found on the main Data tab of oTree
* `PRIZE` (default `cu(0.25)`): How many British pounds (or server currency) to award players who click a button no other player clicks
* `MAX_HISTORY_DISPLAY` (default `8`): How many rounds of previous history to display. This can be specified by round as a dictionary, but history is lost each time the max is reset, so `{1:8, 16:8}` would show eight previous rounds in rounds 9-15, but zero in round 16, 1 in round 17, and so forth. 
* `PLAYER_LABEL` (default `'Player'`): The prefix for player IDs (e.g. "Player1")
* `ROBOT_LABEL` (default `'Bot'`): The prefix when players are replaced with robots (e.g. "Bot1")
* `MAX_TIME` (default `120`): The maximum number of seconds per round
* `BUFFER_INIT` (default `60`): How many seconds to remove from MAX_TIME if players do not request extra time
* `TIMER_DISPLAY_AT` (default `30`): Allow players to request extra time when this many seconds remain
* `TIMER_INCREMENT` (default `30`): How many seconds to add when players request extra time
* `QUESTION_ROUNDS` (default `(2,)`): The round(s) after which to ask users to describe their strategy
* `QUESTION_TIMER` (default `120`): The time limit (in seconds) for describing one's strategy

## Data
Data can be exported in Excel format. Some special data columns of note:
* `participant.skill_rating`: The participant's [trueskill](https://trueskill.org/) rating at the end of the game
* `participant.disconnected`: `1` if the participant was disconnected
* `participant.overwaited`: `1` if the participant advanced t0 the alternate ending because they were in the waiting room too long
* `participant.payoff`: The participant's total winnings across all rounds
* `participant.robot`: The type of robot replacing this player (if any)
* `MADChairs.{round}.player.selection`: What the player selected in that round
* `MADChairs.{round}.player.advice`: What advice was displayed to the player (if any)
* `MADChairs.{round}.player.secondsElapsed`: How many seconds the player took to make their selection in that round
* `MADChairs.{round}.player.payoff`: How much the player won in that round
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
* To include LLMs: [Botex](https://github.com/trr266/botex), [Alter ego](https://github.com/mrpg/ego)
