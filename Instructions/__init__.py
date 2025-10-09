
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SKIP_PREGAME = False
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    instruction_seconds = models.FloatField()
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        import trueskill
        import time
        for player in subsession.get_players():
            part = player.participant
            part.time = time.time()
            part.robot = ""
            part.skill_rating = trueskill.Rating(mu=25, sigma=2)
            part.disconnected = False
            part.overwaited = False
class Start(Page):
    form_model = 'player'
    timeout_seconds = 0.1
class Robot(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.robot != ""
class Information(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return not C.SKIP_PREGAME
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return not C.SKIP_PREGAME
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.instruction_seconds = time.time() - participant.time
        participant.time = time.time() 
class Ready(Page):
    form_model = 'player'
    timeout_seconds = 0.1
    @staticmethod
    def is_displayed(player: Player):
        return C.SKIP_PREGAME
page_sequence = [Start, Robot, Information, Instructions, Ready]