
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'GroupPlayers'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 1
    WAIT_LIMIT = 1200
    ROBOTS = None
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
def waited_too_long(player: Player):
    participant = player.participant
    import time
    return time.time() - participant.time > C.WAIT_LIMIT
def make_robots(stored=None):
    def robot_return():
        nonlocal stored
        if stored is not None:
            return stored
        stored = C.ROBOTS if isinstance(C.ROBOTS, dict) else {'all': C.ROBOTS}
        stored = [stored.get('all', stored.get(player)) for player in range(1, C.PLAYERS_PER_GROUP + 1)]
        return stored
    return robot_return
robot_list = make_robots()
def group_by_arrival_time_method(subsession, waiting_players):
    robots = robot_list().copy()
    if len(waiting_players) >= (C.PLAYERS_PER_GROUP - len(robots) + robots.count(None)):
        parts = subsession.session.get_participants()
        part = parts.pop(0)
        robot = robots.pop(0) if robots else None
        players = [] 
        if (len(robot_list()) >= C.PLAYERS_PER_GROUP) and (robot_list()[:C.PLAYERS_PER_GROUP].count(None) == 0):
            player = waiting_players.pop(0)
            player.participant.robot = robot
            players.append(player)
            if robots:
                robot = robots.pop(0)
        while len(players) < C.PLAYERS_PER_GROUP:    
            if robot is None:
                player = waiting_players.pop(0)
                player.participant.robot = ""
                players.append(player)
                if robots:
                    robot = robots.pop(0)
            elif part.visited:
                part = parts.pop(0)
            else:
                part.initialize(None)
                part._visit_current_page()
                part.robot = robot
                part._submit_current_page()
                players.append(part._get_current_player())
                robot = robots.pop(0) if robots else None 
        ids = [p.participant.id_in_session for p in players]
        for p in players: 
            p.participant.ids_in_group = ids
        return players
    for p in waiting_players:
        if waited_too_long(p):
            p.participant.disconnected = True
            p.participant.overwaited = True
            return [p]
class WaitingToBegin(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for all five players to join...'
    body_text = 'If you click on any other window or tab, you must click back here to be considered "available".'
class AlternateEnd(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.overwaited
page_sequence = [WaitingToBegin, AlternateEnd]