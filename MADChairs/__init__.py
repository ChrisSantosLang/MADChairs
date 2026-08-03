from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'MADChairs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    BUFFER_INIT = 60
    TIMER_INCREMENT = 30
    MAX_TIME = 120
    MAX_HISTORY_DISPLAY = {1:8, 21:8}
    PLAYER_LABEL = 'Player'
    ROBOT_LABEL = 'Bot'
    BUTTONS = ('A', 'B', 'C', 'D')
    TIMER_DISPLAY_AT = 30
    QUESTION_ROUNDS = (2,)
    QUESTION_TIMER = 120
    PRIZE = cu(0.25)
    ADVICE = {1:'{turntaking}', 21: None}
    SORT_HISTORY = True
    HIDE_CHAT = True
    HIDE_SKIP = True
    ADVICE_INFO = ["""You are the only player advised to <b>click {advice}</b> for this round. It is your turn to benefit from a unique button.""",
        """You are not advised to click a unique button this round. This is due to recent deviations from the advice. 
    Following the advice can get you back to be advised unique buttons.""",
        """You are not advised to click a unique button this round. This is to give others a turn at winning, 
    but you will be assigned future turns if you follow the advice.""",
        """The advice algorithm assigns a collision to two players each round, selecting them for exceeding 1 on "deviated" and 
    otherwise by least "owed". Your "deviated" statistic increases by 1 every time you do not follow the advice, 
    but it also decreases by 30% each round, so previous deviations become forgotten. 
    Your "owed" statistic indicates how much the other players owe you; it goes down when you lose and up when you win, 
    so everyone would take turns winning if everyone followed the advice.<br><br>
    We chose the advice algorithm for this study in the same way chess machines are developed: 
    We ran tournaments between the best potential algorithms we could find. 
    Players who followed the advice given in this study achieved the best outcomes for themselves. 
    Participants in previous studies won about three times as often when they followed the advice compared to when they did not. 
    Deviation tends to harm both oneself and any other player with whom one collides.""",
        """Your "owed" is {owed}. That is what you stand to collect by getting your "deviated" below 1. 
    Your "deviated" is currently {deviated}, so you would need to lose {penalty} round(s) before
    the advice will start assigning you what you are owed.<br><br>
    The advice algorithm assigns a collision to two players each round, selecting them for exceeding 1 on "deviated" and 
    otherwise by least "owed". Your "deviated" statistic increases by 1 every time you do not follow the advice, 
    but it also decreases by 30% each round, so previous deviations become forgotten. 
    Your "owed" statistic indicates how much the other players owe you; it goes down when you lose and up when you win, 
    so everyone would take turns winning if everyone followed the advice.<br><br>
    We chose the advice algorithm for this study in the same way chess machines are developed: 
    We ran tournaments between the best potential algorithms we could find. 
    Players who followed the advice given in this study achieved the best outcomes for themselves. 
    Participants in previous studies won about three times as often when they followed the advice compared to when they did not. 
    Deviation tends to harm both oneself and any other player with whom one collides """,
        """Your "owed" is {owed}, which is not higher than other players, 
    but it will go up and theirs will go down if you lose this round and they win.<br><br>
    The advice algorithm assigns a collision to two players each round, selecting them for exceeding 1 on "deviated" and 
    otherwise by least "owed". Your "deviated" statistic increases by 1 every time you do not follow the advice, 
    but it also decreases by 30% each round, so previous deviations become forgotten. 
    Your "owed" statistic indicates how much the other players owe you; it goes down when you lose and up when you win, 
    so everyone would take turns winning if everyone followed the advice.<br><br>
    We chose the advice algorithm for this study in the same way chess machines are developed: 
    We ran tournaments between the best potential algorithms we could find. 
    Players who followed the advice given in this study achieved the best outcomes for themselves. 
    Participants in previous studies won about three times as often when they followed the advice compared to when they did not. 
    Deviation tends to harm both oneself and any other player with whom one collides."""
    ]
    KOLKATA_PAISE = False
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    selection = models.StringField()
    timedOut = models.BooleanField(initial=False)
    secondsElapsed = models.FloatField()
    skill_estimate = models.FloatField(blank=True)
    debt = models.FloatField(initial=0)
    strategy = models.LongStringField(label='Considering rounds 1 and 2, explain briefly the thoughts behind your choices:')
    advice = models.StringField(blank=True)
    soughtInfo = models.BooleanField(initial=False)
def makeMaxHistory(stored=None): 
    def inner():
        nonlocal stored
        if stored is not None:
            return stored 
        shifts = C.MAX_HISTORY_DISPLAY if isinstance(C.MAX_HISTORY_DISPLAY, dict) else {1: C.MAX_HISTORY_DISPLAY}
        if 1 not in shifts:
            shifts[1] = 8
        stored = {}
        maxHist = 0
        for round in range(1, C.NUM_ROUNDS + 1):
            if round in shifts:
                maxHist = shifts[round]
                count = 0
            stored[round] = min(count, maxHist)
            count = count + 1
        return stored
    return inner
maxHistory = makeMaxHistory()
def makeOptions(stored=None): 
    def inner():
        nonlocal stored
        if stored is not None:
            return stored 
        stored = list(C.BUTTONS) if C.HIDE_SKIP else list(C.BUTTONS) + ['skip']
        return stored
    return inner
playerOptions = makeOptions()
def makeCasteStart(stored=None): 
    def inner(num_players=0):
        nonlocal stored
        if stored is not None:
            return stored
        extra_options = [C.BUTTONS[-1] if C.HIDE_SKIP else 'skip'] * (num_players - len(C.BUTTONS)) 
        stored = {index + 1: button for index, button in enumerate(list(C.BUTTONS) + extra_options)}
        return stored
    return inner
casteStart = makeCasteStart()
def random_selection(player=None, n=0):
    import random
    if (n < 1) or (player is None):
        return random.choice(playerOptions())
    if player.round_number == 1:
        return random.choice(C.BUTTONS)
    if ((random.random() < 1/n) and not player.in_round(player.round_number - 1).payoff):
        previous = [p.selection for p in player.in_round(player.round_number - 1).group.get_players()]
        options = [button for button in C.BUTTONS if button not in previous]
        if len(options) < 1:
            options = [button for button in C.BUTTONS if previous.count(button) == 1]
        if len(options) < 1:
            options = C.BUTTONS
        return random.choice(options)
    return player.in_round(player.round_number - 1).selection
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
            group_vars.turnViolations = {id: 0 for id in range(1, len(group_vars.ids_in_group) + 1)}
            group_vars.casteViolations = {id: 0 for id in range(1, len(group_vars.ids_in_group) + 1)}
            group_vars.eqViolations = {id: 0 for id in range(1, len(group_vars.ids_in_group) + 1)}
            group_vars.caste = casteStart(len(group_vars.ids_in_group)).copy()
            group_vars.equalize = group_vars.caste.copy()
            group_vars.radicaleq = group_vars.caste.copy()
            extra_players = len(group_vars.ids_in_group) - len(C.BUTTONS)
            extra_options = [C.BUTTONS[0] if C.HIDE_SKIP else 'skip'] * extra_players 
            group_vars.turntaking = {index + 1: button for index, button in enumerate(extra_options + list(C.BUTTONS))}
            group_vars.session.prize = C.PRIZE
            group_vars.session.max_social = C.NUM_ROUNDS * C.PRIZE * (len(C.BUTTONS) - (1 if C.HIDE_SKIP else 0)) 
        return grouped
def shift(player, amount):
    if amount and int(amount) > 0:
        players = player.group.get_players()
        return players[(players.index(player) + int(amount)) % len(players)] 
    return player
def adviceType(player, adviceList=C.ADVICE):
    advice = ensure_list(strategy_list(adviceList))
    return advice[(player.round_number-1) % len(advice)] 
def advice(player, adviceList=C.ADVICE):
    import re
    advice = adviceType(player, adviceList)
    if not advice:
        return ""
    advice = str(advice)
    group_vars = [p for id in player.participant.ids_in_group for p in player.subsession.session.get_participants() if id == p.id_in_session][0]
    while True:
        m = re.search(r'\{turntaking(\d*)\}', advice)
        if m is None:
            break
        advice = advice.replace(m.group(0), group_vars.turntaking[shift(player, m.group(1)).id_in_group])
    while True:
        m = re.search(r'\{caste(\d*)\}', advice)
        if m is None:
            break
        advice = advice.replace(m.group(0), group_vars.caste[shift(player, m.group(1)).id_in_group])
    while True:
        m = re.search(r'\{equalize(\d*)\}', advice)
        if m is None:
            break
        advice = advice.replace(m.group(0), group_vars.equalize[shift(player, m.group(1)).id_in_group])
    while True:
        m = re.search(r'\{radicaleq(\d*)\}', advice)
        if m is None:
            break
        advice = advice.replace(m.group(0), group_vars.radicaleq[shift(player, m.group(1)).id_in_group])
    while True:
        m = re.search(r'\{random(\d*)\}', advice)
        if m is None:
            break
        n = int(m.group(1)) if m.group(1) else 0
        advice = advice.replace(m.group(0), random_selection(player, n))
    while True:
        m = re.search(r'\{rotate(\d*)\}', advice)
        if m is None:
            break
        rotation = (int(m.group(1)) if m.group(1) else 1) * (player.round_number - 1)
        ids = group_vars.ids_in_group
        advice = advice.replace(m.group(0), casteStart()[((ids.index(player.participant.id_in_session) + rotation) % len(ids)) + 1])
    while True:
        m = re.search(r'\{obey(\d*)\}', advice)
        if m is None:
            break
        advice = advice.replace(m.group(0), shift(player, m.group(1)).field_maybe_none('advice'))
    return advice
def name(player): 
    return (C.PLAYER_LABEL if player.participant.robot == "" else C.ROBOT_LABEL) + str(player.id_in_group)
def historyHTML(player, summary=False): 
    players = [p for id in player.participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id]
    if C.SORT_HISTORY:
        players = sorted(players, key=lambda p: sum([hist.payoff for hist in p.in_all_rounds()]), reverse=True)
    group_vars = [p for id in player.participant.ids_in_group for p in player.subsession.session.get_participants() if id == p.id_in_session][0]
    historyCap = maxHistory()[player.round_number]
    readMore = ""
    if isinstance(C.ADVICE_INFO, list) and "turntaking" in str(adviceType(player)):
        readMore = " <span id='infolink' style='cursor:pointer' onclick='readMore(event)'><u>Read more</u></span>"
        more = ""
        if len(C.ADVICE_INFO) > 0 and player.advice != "skip" and [p.advice for p in players].count(player.advice) < 2:
            historyHTML = ["<div>", C.ADVICE_INFO[0].replace("{advice}", player.advice)]
            if len(C.ADVICE_INFO) > 3:
                more = C.ADVICE_INFO[3] 
        else:
            deviated = round(group_vars.turnViolations[player.id_in_group], 2)
            penalty = max([p[0] for p in ((0, -1), (1, 1), (2, 1.42), (3, 2.04), (4, 2.92)) if deviated > p[1]])
            owed = "0.0"
            if historyCap > 0 and len(players[0].in_previous_rounds()) > 0:
                owed = round(player.in_previous_rounds()[-1].debt * -17.5, 1)
            if group_vars.turnViolations[player.id_in_group] >= 1:
                historyHTML = ["<div>", C.ADVICE_INFO[1].replace("{advice}", player.advice)]
                if len(C.ADVICE_INFO) > 4:
                    more = C.ADVICE_INFO[4].replace("{owed}", str(owed)).replace("{deviated}", f"{deviated:.2f}").replace("{penalty}", str(penalty))
            else:
                historyHTML = ["<div>", C.ADVICE_INFO[2].replace("{advice}", player.advice)]
                if len(C.ADVICE_INFO) > 5:
                    more = C.ADVICE_INFO[5].replace("{owed}", str(owed)).replace("{deviated}", f"{deviated:.2f}").replace("{penalty}", str(penalty))
        if len(more) > 0:
            historyHTML.extend([readMore, "</div><br><div class='hidden' style='display: none'><div>", more, "</div><br>"])
            if player.participant.showColumns:
                historyHTML.extend("</div><input type='checkbox' id='showColumns' checked onclick='boxClicked()'> <label for='showColumns'>Always show Owed and Deviated</label><br><br>")
            else:
                historyHTML.extend("<input type='checkbox' id='showColumns' onclick='boxClicked()'> <label for='showColumns'>Always show Owed and Deviated</label><br><br></div>")
        else: 
            historyHTML.extend(["</div><br>"])
    else:
        historyHTML = ["<div class='hidden' style='display: none'><div>", str(C.ADVICE_INFO), "</div><br></div>"]
    historyHTML.extend(["<table><tr><td style='width: 110pt'>"])

    if historyCap > 0 and len(players[0].in_previous_rounds()) > 0:
        historyHTML.extend(["<b>Previous rounds:</b>"])
        history = players[0].in_all_rounds() if summary else players[0].in_previous_rounds()[-historyCap:]
        for hist in history:
            historyHTML.extend(["</td><td style='text-align: center;'><b>", str(hist.round_number), "</b>"])
    historyHTML.extend(["</td><td style='width: 60pt; text-align: center;'><b>Bonus</b></td>"])
    if player.participant.showColumns:
        historyHTML.extend(["<td class='hidden' style='width: 60pt; text-align: center;'><b>Owed</b></td>"])
        historyHTML.extend(["<td class='hidden' style='width: 60pt; text-align: center;'><b>Deviated</b></td><td></td>"])
    else:
        historyHTML.extend(["<td class='hidden' style='width: 60pt; text-align: center; display: none;'><b>Owed</b></td>"])
        historyHTML.extend(["<td class='hidden' style='width: 60pt; text-align: center; display: none;'><b>Deviated</b></td><td></td>"])
    if not summary and player.advice != "":
        historyHTML.append("<td style='text-align: center;'><b>Advice</b>")
        if len(readMore) < 1:
            historyHTML.append(" <span id='infolink' style='cursor:pointer' onclick='readMore(event)'>(<u>info</u>)</span>") 
        historyHTML.append("</td>")
    historyHTML.append("</tr>")
    payoffs = []
    # team_one = []
    # team_two = []
    for p in players:
        boldRow = not summary and p.id_in_group == player.id_in_group
        historyHTML.append("<tr><td style='width: 110pt'>")
        if boldRow:
            historyHTML.extend(["<b>", name(p), " (Me)</b>"])
        else:
            historyHTML.append(name(p))
        history = p.in_all_rounds() if summary else (p.in_previous_rounds()[-historyCap:] if historyCap > 0 else [])
        for hist in history:
            selection = [hist.selection]
            if hist.selection != "skip" and [p.in_round(hist.round_number).selection for p in players].count(hist.selection) < 2:
                selection = ["<u>"] + selection + ["</u>"]      
            if hist.timedOut:
                selection = ["<i>"] + selection + ["</i>"]
            if not summary and hist.advice in playerOptions():
                if hist.selection == hist.advice:
                    selection.extend(["<span style='font-size: 0.8rem'>(", hist.advice, ")</span>"])
                else:
                    selection.extend(["<span style='color: red; font-size: 0.8rem'>(", hist.advice, ")</span>"])
            if boldRow: 
                selection = ["<b>"] + selection + ["</b>"]  
            historyHTML.extend(["</td><td style='text-align: center;'> &nbsp;"] + selection + ["&nbsp;"])

        total_payoff = sum([hist.payoff for hist in p.in_all_rounds()])
        payoffs.append(total_payoff)
        # if p.id_in_group in (1, 3, 5):
        #     team_one.append(total_payoff)
        # else:
        #     team_two.append(total_payoff)
        bonus = [str(total_payoff)]
        if boldRow:
            bonus = ["<b>"] + bonus + ["</b>"]
        historyHTML.extend(["</td><td style='width: 60pt; text-align: center;'>", "".join(bonus), "</td><td class='hidden' style='width: 60pt; text-align: center;"]) 

        owed = ["0.0"]
        if historyCap > 0 and len(players[0].in_previous_rounds()) > 0:
            owed = [str(round(p.in_previous_rounds()[-1].debt * -17.5, 1))]
        if boldRow:
            owed = ["<b>"] + owed + ["</b>"]
        if not player.participant.showColumns:
           historyHTML.append(" display: none;")
        historyHTML.extend(["'>", "".join(owed), "</td><td class='hidden' style='width: 60pt; text-align: center;"])

        deviated = round(group_vars.turnViolations[p.id_in_group], 2)
        if deviated > 1:
            deviated = ["<span style='color: red; font-size: 0.8rem'>"] + [f"{deviated:.2f}"] + ["</span>"]
        else:
            deviated = [f"{deviated:.2f}"]    
        if boldRow:
            deviated = ["<b>"] + deviated + ["</b>"]
        if not player.participant.showColumns:
           historyHTML.append(" display: none;")
        historyHTML.extend(["'>", "".join(deviated), "</td>"])

        timeouts = sum([int(hist.timedOut) for hist in p.in_all_rounds()])
        if timeouts > 0:
            if boldRow:
                historyHTML.extend(["<td style='width: 80pt; text-align: center;'><i><b>(", str(timeouts), " timeouts)</b></i></td>"])
            else:
                historyHTML.extend(["<td style='width: 80pt; text-align: center;'><i>(", str(timeouts), " timeouts)</i></td>"])    
        else:
            historyHTML.extend(["<td></td>"])

        if not summary and p.advice != "":    
            if boldRow:
                historyHTML.extend(["<td style='text-align: center;'><b>", p.advice, "</b></td>"])    
            else:
                historyHTML.extend(["<td style='text-align: center;'>", p.advice, "</td>"]) 

        historyHTML.append("</tr>")
    historyHTML.append("</table>") 
    if summary:
        historyHTML.extend(["<br><div style='text-align: center;'>Social utility=<b>", str(sum(payoffs))])
        historyHTML.extend(["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>Disparity=<b>", str(max(payoffs)-min(payoffs)),"</b></div>"])
        # max_pay = C.PRIZE * C.NUM_ROUNDS  
        # historyHTML.extend(["<br><div style='text-align: center;'>one mean=<b>", str(sum(team_one)/(max_pay * len(team_one))), "&nbsp;</b>min=<b>", str(min(team_one)/max_pay), "&nbsp;</b>max=<b>", str(max(team_one)/max_pay),"</b></div>"])
        # historyHTML.extend(["<br><div style='text-align: center;'>two mean=<b>", str(sum(team_two)/(max_pay * len(team_two))), "&nbsp;</b>min=<b>", str(min(team_two)/max_pay), "&nbsp;</b>max=<b>", str(max(team_two)/max_pay),"</b></div>"]) 
    return "".join(historyHTML)
def makeButtons(stored=None): 
    def inner():
        nonlocal stored
        if stored is not None:
            return stored
        buttonHTML = ["<table><tr>"]
        for button in C.BUTTONS:
            buttonHTML.extend(['<td><button id="', button, '" class="btn btn-primary">&nbsp;', button, '&nbsp;</button>&nbsp;&nbsp;&nbsp;&nbsp;</td>'])
        if not C.HIDE_SKIP:
            buttonHTML.append('<td><a href="javascript:;" onclick="skipClicked()">skip this round</a></td>') 
        buttonHTML.append("</tr></table>") 
        stored = "".join(buttonHTML)
        return stored
    return inner
buttonHTML = makeButtons()
class MADChairsWaitPage(WaitPage):
    group_by_arrival_time = True
class MADChairs(Page):
    form_model = 'player'
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        participant = player.participant
        import time
        if "round" in data and data["round"] != player.round_number:
            return {player.id_in_group: None}
        participant.disconnected = False
        if "extended" in data:
            return {player.id_in_group: None}
        player.secondsElapsed = time.time() - participant.time
        if "selected" in data and data["selected"] in playerOptions():
            player.selection = data["selected"]
            participant.showColumns = data["showColumns"]
            player.timedOut = False
        elif "timeout" in data:
            player.timedOut = True
            player.selection = random_selection()
        elif "showMore" in data:
            player.soughtInfo = True
            return {player.id_in_group: "show more"}
        return {player.id_in_group: "selection_made"}
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
            if player.field_maybe_none(advice) is None:
                for p in players:
                    p.advice = advice(p) if C.ADVICE else ""
            robots = set()
            for p in players:
                if p.participant.robot != "":
                    robots.add(p.participant.id_in_session)
                    if isinstance(p.participant.robot, dict):
                        p.participant.robot = strategy_list(p.participant.robot, default="{obey}")
                    strategy = advice(p, p.participant.robot) 
                    p.selection = strategy if strategy in playerOptions() else random_selection()
            player.group.get_player_by_id(1).participant.finished = robots
        return participant.robot == ""
    @staticmethod
    def js_vars(player: Player):
        import time
        player.participant.time = time.time()
        return dict(
            historyHTML = historyHTML(player),
            buttonHTML= buttonHTML(),
            BUFFER_INIT = C.BUFFER_INIT,
            TIMER_DISPLAY_AT = C.TIMER_DISPLAY_AT,
            TIMER_INCREMENT = C.TIMER_INCREMENT,
            BUTTONS = C.BUTTONS,
            HIDE_CHAT = C.HIDE_CHAT,
            round = player.round_number
        )
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            playerName=name(player),
            groupId=player.participant.ids_in_group[0]
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
def updateTrueSkill(players):
    import trueskill
    import math
    selections = {"skip": set()}
    for p in players:
        if p.selection not in selections:
            selections[p.selection] = {p}
        else:
            selections[p.selection].add(p)
    if C.KOLKATA_PAISE and not C.HIDE_SKIP:
        import random
        for selection, selectors in selections.items():
            if (len(selectors) == 1) or (selection == "skip"):
                continue
            else:
                for p in random.sample(selectors, k=len(selectors)-1):
                    p.selection = "skip"
                    selectors.remove(p)
    winners = []
    for p in players:
        if len(selections[p.selection]) == 1 and p.selection in C.BUTTONS and not p.timedOut:
            p.payoff = C.PRIZE
            winners.append(0)
        else:
            winners.append(1)
    for me in players:
        myRating = me.participant.skill_rating 
        if len(me.in_previous_rounds()) > 0:
            me.debt = me.in_previous_rounds()[-1].debt
        else:
            me.debt = (len(players) - me.id_in_group)/100000  #residue to stabilize ties
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
def updateStrategies(players, group_vars):
    updateTrueSkill(players)
    for p in players:
        if p.selection in C.BUTTONS:
            group_vars.popularity[p.selection] += 1 + p.id_in_group/10000 #residue to stabilize ties
        group_vars.turnViolations[p.id_in_group] = group_vars.turnViolations[p.id_in_group] * 0.7 
        if (p.selection != group_vars.turntaking[p.id_in_group]) and not (C.KOLKATA_PAISE and p.selection == "skip"):
            group_vars.turnViolations[p.id_in_group] += 1 
        group_vars.casteViolations[p.id_in_group] = group_vars.casteViolations[p.id_in_group] * 0.7 
        if p.selection != group_vars.caste[p.id_in_group] and not (C.KOLKATA_PAISE and p.selection == "skip"):
            group_vars.casteViolations[p.id_in_group] += 1
        group_vars.eqViolations[p.id_in_group] = group_vars.eqViolations[p.id_in_group] * 0.7 
        if p.selection != group_vars.equalize[p.id_in_group] and not (C.KOLKATA_PAISE and p.selection == "skip"):
            group_vars.eqViolations[p.id_in_group] += 1
    extra_players = len(group_vars.ids_in_group) - len(C.BUTTONS)
    sorted_buttons = sorted(group_vars.popularity.items(), key=lambda item: item[1])
    # equalize
    win_sorted_players = [id_in_group for bonus, id_in_group in sorted([(p.participant.payoff, p.id_in_group) for p in players])]
    learners = [p for p in win_sorted_players if group_vars.eqViolations[p] < 1] 
    equal_players = learners + [p for p in win_sorted_players if p not in learners]
    extra_buttons = [(sorted_buttons[-1] if C.HIDE_SKIP else ('skip',))] * extra_players
    group_vars.equalize = {id: (sorted_buttons + extra_buttons)[i][0] for i, id in enumerate(equal_players)}
    group_vars.radicaleq = {id: (sorted_buttons + extra_buttons)[i][0] for i, id in enumerate(win_sorted_players)}
    # caste
    debt_sorted_players = [id_in_group for debt, id_in_group in sorted([(-p.debt, p.id_in_group) for p in players])]
    learners = [p for p in debt_sorted_players if group_vars.casteViolations[p] < 1] 
    castePlayers = learners + [p for p in debt_sorted_players if p not in learners]
    group_vars.caste = {id: (sorted_buttons + extra_buttons)[i][0] for i, id in enumerate(castePlayers)}
    #turn-taking
    learners = [p for p in debt_sorted_players if group_vars.turnViolations[p] < 1] 
    turnTakers = [p for p in debt_sorted_players if p not in learners] + learners
    free = [button for button in sorted_buttons if button[1] < players[0].round_number * 1.4] 
    sorted_buttons = [button for button in sorted_buttons if button not in free] + free
    extra_buttons = [(sorted_buttons[0] if C.HIDE_SKIP else ('skip',))] * extra_players
    group_vars.turntaking = {id: (extra_buttons + sorted_buttons)[i][0] for i, id in enumerate(turnTakers)}
class Strategy(Page):
    form_model = 'player'
    form_fields = ['strategy']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        group_vars = player.group.get_player_by_id(1).participant
        if isinstance(group_vars.finished, set):
            group_vars.finished.add(participant.id_in_session)
            if (len(group_vars.finished) >= len(group_vars.ids_in_group)):
                group_vars.finished = None
                players = [p for id in participant.ids_in_group for p in player.subsession.get_players() if p.participant.id_in_session == id] 
                updateStrategies(players, group_vars)
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