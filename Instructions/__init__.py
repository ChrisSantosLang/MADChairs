
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    instruction_seconds = models.FloatField()
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
        import trueskill
        player.instruction_seconds = time.time() - participant.time
        participant.time = time.time()
        participant.skill_rating = trueskill.Rating()
        participant.disconnected = False
page_sequence = [Information, Instructions]