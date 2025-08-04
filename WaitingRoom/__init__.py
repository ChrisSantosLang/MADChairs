
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'WaitingRoom'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def init_skill_rankings(group: Group):
    import trueskill
    for p in group.get_players(): 
        p.participant.skill_rating = trueskill.Rating()
        p.participant.disconnected = False
class Player(BasePlayer):
    pass
class Information(Page):
    form_model = 'player'
class Instructions(Page):
    form_model = 'player'
class WaitingToBegin(WaitPage):
    after_all_players_arrive = init_skill_rankings
    title_text = 'Waiting for all five players to join...'
    body_text = 'If you click on any other window or tab, you must click back here to be considered "available".'
page_sequence = [Information, Instructions, WaitingToBegin]