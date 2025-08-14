
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'MADChairs'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 20
    BUFFER_INIT = 60
    TIMER_INCREMENT = 30
    MAX_TIME = 120
    MAX_HISTORY_DISPLAY = 8
    PLAYER_LABELS = ('Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5')
    BUTTONS = ('A', 'B', 'C', 'D')
    TIMER_DISPLAY_AT = 30
    QUESTION_TIMER = 120
    PRIZE = cu(0.25)
    WAIT_LIMIT = 1200
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
        if selections.count(p.selection) == 1 and p.selection in C.BUTTONS and not p.timedOut:
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
def record_wait_time(group: Group):
    session = group.session
    import time
    ids_in_group = [p.participant.id_in_session for p in group.get_players()]
    for p in group.get_players(): 
        p.participant.ids_in_group = ids_in_group
        p.participant.wait_seconds = time.time() - p.participant.time
class Player(BasePlayer):
    selection = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['skip', 'skip']])
    timedOut = models.BooleanField(initial=False)
    secondsElapsed = models.FloatField()
    skill_estimate = models.FloatField(blank=True)
    debt = models.FloatField(initial=0)
    strategy = models.LongStringField(label='Considering rounds 1 and 2, explain briefly the thoughts behind your choices:')
    disconnectChecked = models.BooleanField(initial=False)
def live_update(player: Player, data):
    group = player.group
    participant = player.participant
    import time
    participant.disconnected = False
    player.secondsElapsed = time.time() - participant.time
    if "selected" in data and data["selected"] in C.BUTTONS:
        player.selection = data["selected"]
    elif "timeout" in data:
        import random
        player.timedOut = True
        player.selection = random.choice(C.BUTTONS)
    return {player.id_in_group: "selection_made"}
def waited_too_long(player: Player):
    participant = player.participant
    import time
    return time.time() - participant.time > C.WAIT_LIMIT
def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= C.PLAYERS_PER_GROUP:
        return waiting_players[:C.PLAYERS_PER_GROUP]
    for p in waiting_players:
        if waited_too_long(p):
            p.participant.disconnected = True
            p.participant.overwaited = True
            return [p]
class WaitingToBegin(WaitPage):
    group_by_arrival_time = True
    after_all_players_arrive = record_wait_time
    title_text = 'Waiting for all five players to join...'
    body_text = 'If you click on any other window or tab, you must click back here to be considered "available".'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class AlternateEnd(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.overwaited
class MADChairs(Page):
    form_model = 'player'
    live_method = 'live_update'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.overwaited:
            return False
        if not player.disconnectChecked:
            player.disconnectChecked = True
            if participant.disconnected:
                import random
                player.timedOut = True
                player.selection = random.choice(C.BUTTONS)
                return False
            participant.disconnected = True
        return True
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
            historyHTML.extend(["<td style='width: 110pt;'><b>Bonus</b></td>"])
        historyHTML.append("</tr>")
        for p in players:
            p.participant.time = time.time()
            if p.id_in_group == player.id_in_group:
                historyHTML.extend(["<tr><td style='width: 110pt'><b>", C.PLAYER_LABELS[p.id_in_group-1], " (Me)</b></td>"])
            else:
                historyHTML.extend(["<tr><td style='width: 110pt'>", C.PLAYER_LABELS[p.id_in_group-1], "</td>"])
            for hist in p.in_previous_rounds()[-C.MAX_HISTORY_DISPLAY:]:
                selection = [hist.selection]
                if [p.in_round(hist.round_number).selection for p in players].count(hist.selection) > 1:
                    selection = ["("] + selection + [")"]      
                if p.id_in_group == player.id_in_group:
                    selection = ["<b>"] + selection + ["</b>"]
                if hist.timedOut:
                    selection = ["<i>"] + selection + ["</i>"]
                historyHTML.extend(["<td style='width: 20pt; text-align: center;'>"] + selection + ["</td>"])
            timeouts = sum([int(hist.timedOut) for hist in p.in_previous_rounds()])
            total_payoff = sum([hist.payoff for hist in p.in_previous_rounds()])
            if timeouts > 0:
                total_payoff = "".join([str(total_payoff), "<i> (", str(timeouts), " timeouts)</i>"])
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
        return C.MAX_TIME
class Strategy(Page):
    form_model = 'player'
    form_fields = ['strategy']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 2 and not participant.disconnected
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.QUESTION_TIMER
class MADChairsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == C.NUM_ROUNDS and not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        participant.time = time.time()
page_sequence = [WaitingToBegin, AlternateEnd, MADChairs, Strategy, MADChairsWaitPage, Results]