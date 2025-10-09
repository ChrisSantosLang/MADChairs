from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'MADChairs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20
    BUFFER_INIT = 60
    TIMER_INCREMENT = 30
    MAX_TIME = 120
    MAX_HISTORY_DISPLAY = 8
    PLAYER_LABEL = 'Player'
    ROBOT_LABEL = 'Bot'
    BUTTONS = ('A', 'B', 'C', 'D')
    TIMER_DISPLAY_AT = 30
    QUESTION_ROUNDS = (2,)
    QUESTION_TIMER = 120
    PRIZE = cu(0.25)
    ADVICE = None
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    selection = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['skip', 'skip']])
    timedOut = models.BooleanField(initial=False)
    secondsElapsed = models.FloatField()
    skill_estimate = models.FloatField(blank=True)
    debt = models.FloatField(initial=0)
    strategy = models.LongStringField(label='Considering rounds 1 and 2, explain briefly the thoughts behind your choices:')
    advice = models.StringField(blank=True)
def random_selection():
    import random
    return random.choice(C.BUTTONS)
def live_update(player: Player, data):
    group = player.group
    participant = player.participant
    import time
    participant.disconnected = False
    player.secondsElapsed = time.time() - participant.time
    if "selected" in data and data["selected"] in C.BUTTONS:
        player.selection = data["selected"]
    elif "timeout" in data:
        player.timedOut = True
        player.selection = random_selection()
    return {player.id_in_group: "selection_made"}
def ensure_list(data):
    if isinstance(data, (tuple,list)):	
        return list(data)
    return [data]
def strategy_list(strategy, default=''):
    if not isinstance(strategy, dict):
        return strategy
    strategies = []
    current_strategy = default
    for round in range(1, C.NUM_ROUNDS+1):
        if round in strategy:
            current_strategy = strategy[round]
        strategies.append(current_strategy)
    return strategies
def group_by_arrival_time_method(subsession, waiting_players):
    if not waiting_players:
        return
    ids = waiting_players[0].participant.ids_in_group
    grouped = [p._get_current_player() for id in ids for p in subsession.session.get_participants() if p.id_in_session == id]
    waiting = [p for p in waiting_players if p in grouped]
    if len(waiting) >= len([p for p in grouped if p.participant.robot == ""]):
        if waiting[0].round_number == 1:
            import time
            for p in waiting:
                part = p.participant
                part.disconnectChecked = [False] * C.NUM_ROUNDS
                part.wait_seconds = time.time() - part.time
            group_vars = grouped[0].participant
            group_vars.popularity = {name: 0 for name in C.BUTTONS}
            group_vars.learnTurn = {id: 0 for id in range(1, len(group_vars.ids_in_group) + 1)}
            group_vars.learnCaste = {id: 0 for id in range(1, len(group_vars.ids_in_group) + 1)}
            num_losers = len(group_vars.ids_in_group) - len(C.BUTTONS)
            group_vars.turntaking = {index + 1: chair for index, chair in enumerate(([C.BUTTONS[0]] * num_losers) + list(C.BUTTONS))}
            group_vars.caste = {index + 1: chair for index, chair in enumerate(list(C.BUTTONS) + ([C.BUTTONS[-1]] * num_losers))}
            group_vars.equalize = {index + 1: chair for index, chair in enumerate(([C.BUTTONS[0]] * num_losers) + list(C.BUTTONS))}
        return grouped
def rotate(player, n=1, group_vars=None): 
    now = player.round_number
    ids = player.participant.ids_in_group
    if not group_vars:
        group_vars = [p for p in player.subsession.session.get_participants() if p.id_in_session == ids[0]][0]
    if now == 1:
        return group_vars.caste[player.id_in_group]
    rotated_id = ids[(ids.index(player.participant.id_in_session) + n) % len(ids)]
    rotated_player = [p for p in player.subsession.get_players() if p.participant.id_in_session == rotated_id][0]
    return rotated_player.in_round(now - 1).selection
def advice(player, adviceList=C.ADVICE):
    advice = ensure_list(strategy_list(adviceList))
    advice = advice[(player.round_number-1) % len(advice)]
    advice = advice if advice else ""
    group_vars = [p for p in player.subsession.session.get_participants() if p.id_in_session == player.participant.ids_in_group[0]][0]
    if "{turntaking}" in advice:
        advice = str(advice).format(turntaking=group_vars.turntaking[player.id_in_group])
    if "{caste}" in advice:
        advice = str(advice).format(caste=group_vars.caste[player.id_in_group])
    if "{random}" in advice:
        advice = str(advice).format(random=random_selection())
    if "{rotate2}" in advice:
        advice = str(advice).format(rotate2=rotate(player, 2, group_vars=group_vars))
    if "{rotate}" in advice:
        advice = str(advice).format(rotate=rotate(player, group_vars=group_vars))
    if "{obey}" in advice:
        advice = str(advice).format(obey=player.field_maybe_none('advice'))
    if "{equalize}" in advice:
        advice = str(advice).format(equalize=group_vars.equalize[player.id_in_group])
    return advice
def name(player): 
    return (C.PLAYER_LABEL if player.participant.robot == "" else C.ROBOT_LABEL) + str(player.id_in_group)
def historyHTML(player, summary=False): 
    historyHTML = ["<tr><td style='width: 110pt'>"]
    players = [p for id in player.participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
    if len(players[0].in_previous_rounds()) > 0:
        historyHTML.extend(["<b>Previous rounds:</b>"])
        history = players[0].in_all_rounds() if summary else players[0].in_previous_rounds()[-C.MAX_HISTORY_DISPLAY:]
        for hist in history:
            historyHTML.extend(["</td><td style='width: 20pt; text-align: center;'><b>", str(hist.round_number), "</b>"])
    historyHTML.extend(["</td><td style='width: 60pt; text-align: center;'><b>Bonus</b></td><td></td>"])
    if not summary and player.advice != "":
        historyHTML.extend(["<td style='width: 60pt; text-align: center;'><b>Advice</b></td>"])
    historyHTML.append("</tr>")
    for p in players:
        if not summary and p.id_in_group == player.id_in_group:
            historyHTML.extend(["<tr><td style='width: 110pt'><b>", name(p), " (Me)</b></td>"])
        else:
            historyHTML.extend(["<tr><td style='width: 110pt'>", name(p), "</td>"])
        history = p.in_all_rounds() if summary else p.in_previous_rounds()[-C.MAX_HISTORY_DISPLAY:]
        for hist in history:
            selection = [hist.selection]
            if [p.in_round(hist.round_number).selection for p in players].count(hist.selection) > 1:
                selection = ["("] + selection + [")"]      
            if not summary and p.id_in_group == player.id_in_group:
                selection = ["<b>"] + selection + ["</b>"]
            if hist.timedOut:
                selection = ["<i>"] + selection + ["</i>"]
            historyHTML.extend(["<td style='width: 20pt; text-align: center;'>"] + selection + ["</td>"])
        timeouts = sum([int(hist.timedOut) for hist in p.in_all_rounds()])
        total_payoff = sum([hist.payoff for hist in p.in_all_rounds()])
        if not summary and p.id_in_group == player.id_in_group:
            historyHTML.extend(["<td style='width: 60pt; text-align: center;'><b>", str(total_payoff), "</b></td>"])
        else:
            historyHTML.extend(["<td style='width: 60pt; text-align: center;'>", str(total_payoff), "</td>"])
        if timeouts > 0:
            if not summary and p.id_in_group == player.id_in_group:
                historyHTML.extend(["<td style='width: 80pt; text-align: center;'><b><i>(", str(timeouts), " timeouts)</i></b></td>"])
            else:
                historyHTML.extend(["<td style='width: 80pt; text-align: center;'><i>(", str(timeouts), " timeouts)</i></td>"])    
        else:
            historyHTML.extend(["<td></td>"])
        if not summary and player.advice != "":    
            if p.id_in_group == player.id_in_group:
                historyHTML.extend(["<td style='width: 60pt; text-align: center;'><b>", p.advice, "</b></td>"])
            else:
                historyHTML.extend(["<td style='width: 60pt; text-align: center;'>", p.advice, "</td>"])    
        historyHTML.append("</tr>") 
    return "".join(historyHTML)
class MADChairsWaitPage(WaitPage):
    group_by_arrival_time = True
class MADChairs(Page):
    form_model = 'player'
    live_method = 'live_update'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.overwaited:
            return False
        if not participant.disconnectChecked[player.round_number - 1]:
            participant.disconnectChecked[player.round_number - 1] = True
            if participant.disconnected:
                player.timedOut = True
                player.selection = random_selection()
                return False
            if participant.robot == "":
                participant.disconnected = True
            players = [p for id in participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
            if C.ADVICE and player.field_maybe_none(advice) is None:
                for p in players:
                    p.advice = advice(p) 
            robots = set()
            for p in players:
                if p.participant.robot != "":
                    robots.add(p.participant.id_in_session)
                    if isinstance(p.participant.robot, dict):
                        p.participant.robot = strategy_list(p.participant.robot, default="{obey}")
                    strategy = advice(p, p.participant.robot) 
                    p.selection = strategy if strategy in C.BUTTONS else random_selection()
            player.group.get_player_by_id(1).participant.finished = robots
        return participant.robot == ""
    @staticmethod
    def js_vars(player: Player):
        import time
        player.participant.time = time.time()
        return dict(
            historyHTML = historyHTML(player),
            BUFFER_INIT = C.BUFFER_INIT,
            TIMER_DISPLAY_AT = C.TIMER_DISPLAY_AT,
            TIMER_INCREMENT = C.TIMER_INCREMENT
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            import time
            player.timedOut = True
            player.secondsElapsed = time.time() - player.participant.time
            player.selection = random_selection()
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.MAX_TIME
class Strategy(Page):
    form_model = 'player'
    form_fields = ['strategy']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        group_vars = player.group.get_player_by_id(1).participant
        if group_vars.finished:
            group_vars.finished.add(participant.id_in_session)
        if group_vars.finished and (len(group_vars.finished) >= len(group_vars.ids_in_group)):
            group_vars.finished = None
            import trueskill
            import math
            players = [p for id in participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
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
                else:
                    me.debt = (len(players) - me.id_in_group)/100  #residue to stabilize ties
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
            group_vars = player.group.get_player_by_id(1).participant
            for p in players:
                group_vars.popularity[p.selection] += 1 + p.id_in_group/10000 #residue to stabilize ties
                group_vars.learnTurn[p.id_in_group] = group_vars.learnTurn[p.id_in_group] * 0.9 
                if p.selection != group_vars.turntaking[p.id_in_group]:
                    group_vars.learnTurn[p.id_in_group] += 1 
                group_vars.learnCaste[p.id_in_group] = group_vars.learnCaste[p.id_in_group] * 0.9 
                if p.selection != group_vars.caste[p.id_in_group]:
                    group_vars.learnCaste[p.id_in_group] += 1
            sorted_chairs = sorted(group_vars.popularity.items(), key=lambda item: item[1])
            sorted_players = [id_in_group for debt, id_in_group in sorted([(-p.debt, p.id_in_group) for p in players])]
            sorted_equal = [id_in_group for bonus, id_in_group in sorted([(p.participant.payoff, p.id_in_group) for p in players])]
            num_losers = len(group_vars.ids_in_group) - len(C.BUTTONS)
            group_vars.equalize = {id: (sorted_chairs + ([sorted_chairs[-1]] * num_losers))[i][0] for i, id in enumerate(sorted_equal)}
            learners = [p for p in sorted_players if group_vars.learnCaste[p] < 1] 
            castePlayers = learners + [p for p in sorted_players if p not in learners]
            group_vars.caste = {id: (sorted_chairs + ([sorted_chairs[-1]] * num_losers))[i][0] for i, id in enumerate(castePlayers)}
            learners = [p for p in sorted_players if group_vars.learnTurn[p] < 1] 
            turnTakers = [p for p in sorted_players if p not in learners] + learners
            free = [chair for chair in sorted_chairs if chair[1] < player.round_number * 1.1] 
            sorted_chairs = [chair for chair in sorted_chairs if chair not in free] + free
            group_vars.turntaking = {id: (([sorted_chairs[0]] * num_losers) + sorted_chairs)[i][0] for i, id in enumerate(turnTakers)}
        return player.round_number in C.QUESTION_ROUNDS and not participant.disconnected and participant.robot == ""
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.QUESTION_TIMER
class Processing(Page):
    form_model = 'player'
    timeout_seconds = 0.1
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        players = [p for id in participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
        robots = [p for p in players if p.participant.robot != ""]
        return len(robots) == len(players)
class RobotResults(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        players = [p for id in participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
        robots = [p for p in players if p.participant.robot != ""]
        return ((player.round_number == C.NUM_ROUNDS) and (len(robots) == len(players)))
    @staticmethod
    def js_vars(player: Player): 
        return dict(historyHTML = historyHTML(player, summary=True))
page_sequence = [MADChairsWaitPage, MADChairs, Strategy, Processing, RobotResults]