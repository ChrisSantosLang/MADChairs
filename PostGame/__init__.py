
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'PostGame'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    perceived_aim = models.LongStringField(label='What do you think this experiment was about? ')
    final_strategy = models.LongStringField(label='What were your strategies in the game?  (If you had different strategies, please briefly describe them). ')
    instruction_difficulty = models.IntegerField(choices=[[0, '0 (Very easy)'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10 (Very difficult)']], label='How difficult were the instructions of the game?', max=10, min=0, widget=widgets.RadioSelectHorizontal)
    risk_proclivity = models.IntegerField(choices=[[0, '0 (Not willing at all)'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10 (Very willing)']], label='Please tell us, in general, how willing or unwilling are you to take risks', max=10, min=0, widget=widgets.RadioSelectHorizontal)
class Results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
class Page1(Page):
    form_model = 'player'
    form_fields = ['perceived_aim']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
class Page2(Page):
    form_model = 'player'
    form_fields = ['final_strategy']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
class Page3(Page):
    form_model = 'player'
    form_fields = ['instruction_difficulty', 'risk_proclivity']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
class End(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            total=participant.payoff + 4,
            wins=int(participant.payoff / 0.2),
        )
page_sequence = [Results, Page1, Page2, Page3, End]