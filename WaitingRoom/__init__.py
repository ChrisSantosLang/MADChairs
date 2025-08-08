
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'WaitingRoom'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def init_skill_rankings(group: Group):
    import trueskill
    import time
    for p in group.get_players(): 
        p.participant.skill_rating = trueskill.Rating()
        p.participant.disconnected = False
        p.wait_seconds = time.time() - p.participant.time
class Player(BasePlayer):
    instruction_seconds = models.FloatField()
    wait_seconds = models.FloatField()
class Information(Page):
    form_model = 'player'
    @staticmethod
    def js_vars(player: Player):
        participant = player.participant
        import time
        participant.time = time.time()
        return dict()
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.instruction_seconds = time.time() - participant.time
        participant.time = time.time()
class WaitingToBegin(WaitPage):
    after_all_players_arrive = init_skill_rankings
    title_text = 'Waiting for all five players to join...'
    body_text = 'If you click on any other window or tab, you must click back here to be considered "available".'
page_sequence = [Information, Instructions, WaitingToBegin]