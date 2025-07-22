
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'MADChairs'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 4
    BUFFER_INIT = 60
    TIMER_INCREMENT = 30
    MAX_TIME = 120
    MAX_HISTORY_DISPLAY = 8
    PLAYER_LABELS = ('Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5')
    PRIZE = cu(0.4)
    BUTTONS = ('A', 'B', 'C', 'D')
    TIMER_DISPLAY_AT = 30
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def set_payoffs(group: Group):
    import trueskill
    import math
    players = group.get_players()
    selections = [p.selection for p in players]
    winners = []
    for p in players:
        if selections.count(p.selection) == 1 and p.selection in C.BUTTONS:
            p.payoff = C.PRIZE
            winners.append(0)
        else:
            winners.append(1)
    for me in players:
        myRating = me.participant.skill_rating 
        if len(me.in_previous_rounds()) > 0:
            me.debt = me.in_previous_rounds()[-1].debt
        for other in players:
            if me.id_in_group != other.id_in_group:
                otherRating = other.participant.skill_rating 
                denom = math.sqrt(2 * trueskill.BETA**2 + myRating.sigma**2 + otherRating.sigma**2)
                if myRating.mu == otherRating.mu:
                    myWin = 0.5
                elif myRating.mu > otherRating.mu:
                    myWin = trueskill.global_env().cdf((myRating.mu - otherRating.mu) / denom)
                else:
                    myWin = 1 - trueskill.global_env().cdf((otherRating.mu - myRating.mu) / denom)
                nondraw = 1 - trueskill.quality_1vs1(myRating, otherRating)
                if (me.payoff == 0) or (other.payoff > 0):
                    me.debt -= myWin * nondraw
                if (me.payoff > 0) or (other.payoff == 0):
                    me.debt += (1 - myWin) * nondraw 
    for player_rating in zip(players, trueskill.rate([(p.participant.skill_rating,) for p in players], winners)):
        player_rating[0].participant.skill_rating = player_rating[1][0]
        player_rating[0].skill_estimate = player_rating[1][0].mu
class Player(BasePlayer):
    selection = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['skip', 'skip']])
    timedOut = models.BooleanField(initial=False)
    secondsElapsed = models.FloatField()
    skill_estimate = models.FloatField(blank=True)
    debt = models.FloatField(initial=0)
def live_update(player: Player, data):
    group = player.group
    participant = player.participant
    import time
    player.participant.disconnected = False
    if "selected" in data and data["selected"] in C.BUTTONS:
        player.secondsElapsed = time.time() - player.participant.time
        player.selection = data["selected"]
        return {player.id_in_group: "selection_made"}
    if "timeout" in data:
        import random
        player.timedOut = True
        player.secondsElapsed = time.time() - player.participant.time
        player.selection = random.choice(C.BUTTONS)
        return {player.id_in_group: "selection_made"}
class MADChairs(Page):
    form_model = 'player'
    timer_text = 'Time left to make selection'
    live_method = 'live_update'
    @staticmethod
    def js_vars(player: Player):
        group = player.group
        participant = player.participant
        import time
        historyHTML = ["<tr>"]
        players = group.get_players()
        if len(players[0].in_previous_rounds()) > 0:
            historyHTML.extend(["<td style='width: 110pt'><b>Previous rounds:</b></td>"])
            for hist in players[0].in_previous_rounds()[-C.MAX_HISTORY_DISPLAY:]:
                historyHTML.extend(["<td style='width: 20pt; text-align: center;'><b>", str(hist.round_number), "</b></td>"])
        historyHTML.append("</tr>")
        for p in players:
            p.participant.time = time.time()
            if p.id_in_group == player.id_in_group:
                historyHTML.extend(["<tr><td style='width: 110pt'><b>", C.PLAYER_LABELS[p.id_in_group-1], " (Me)</b></td>"])
            else:
                historyHTML.extend(["<tr><td style='width: 110pt'>", C.PLAYER_LABELS[p.id_in_group-1], "</td>"])
            for hist in p.in_previous_rounds()[-C.MAX_HISTORY_DISPLAY:]:
                if p.id_in_group == player.id_in_group:
                    if hist.payoff > 0:
                        historyHTML.extend(["<td style='width: 20pt; text-align: center;'><b>", hist.selection, "</b></td>"])
                    else:
                        historyHTML.extend(["<td style='width: 20pt; text-align: center;'><b>(", hist.selection, ")</b></td>"])
                else:
                    if hist.payoff > 0:
                        historyHTML.extend(["<td style='width: 20pt; text-align: center;'>", hist.selection, "</td>"])
                    else:
                        historyHTML.extend(["<td style='width: 20pt; text-align: center;'>(", hist.selection, ")</td>"])
            total_payoff = sum([hist.payoff for hist in p.in_previous_rounds()])
            if p.id_in_group == player.id_in_group:
                historyHTML.extend(["<td style='width: 60pt'><b>", str(total_payoff), "</b></td>"])
            else:
                historyHTML.extend(["<td style='width: 60pt'>", str(total_payoff), "</td>"])
            historyHTML.append("</tr>") 
        return dict(
            historyHTML = "".join(historyHTML),
            BUFFER_INIT = C.BUFFER_INIT,
            TIMER_DISPLAY_AT = C.TIMER_DISPLAY_AT,
            TIMER_INCREMENT = C.TIMER_INCREMENT
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            import random
            import time
            player.timedOut = True
            player.secondsElapsed = time.time() - player.participant.time
            player.selection = random.choice(C.BUTTONS)
    @staticmethod
    def get_timeout_seconds(player: Player):
        participant = player.participant
        if participant.disconnected:
            return 0
        else:
            participant.disconnected = True
            return C.MAX_TIME
class MADChairsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
page_sequence = [MADChairs, MADChairsWaitPage]