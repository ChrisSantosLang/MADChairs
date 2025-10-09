from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Results'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
def group_by_arrival_time_method(subsession, waiting_players):
    if not waiting_players:
        return
    ids = waiting_players[0].participant.ids_in_group
    grouped = [p._get_current_player() for id in ids for p in subsession.session.get_participants() if p.id_in_session == id]
    waiting = [p for p in waiting_players if p in grouped]
    if len(waiting) >= len([p for p in grouped if p.participant.robot == ""]):
        return grouped  
class WaitingForResults(WaitPage):
    group_by_arrival_time = True
class Results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        participant.time = time.time()
page_sequence = [WaitingForResults, Results]