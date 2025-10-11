
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
    final_strategy = models.LongStringField(label='Considering the final rounds, explain briefly the thoughts behind your choices: ')
    instruction_difficulty = models.IntegerField(choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10']], label='How hard were the instructions of the game? (0 = Very easy, 10 = Very hard)', max=10, min=0, widget=widgets.RadioSelectHorizontal)
    risk_proclivity = models.IntegerField(choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10']], label='Please tell us, in general, how willing or unwilling are you to take risks. (0 = Not willing at all, 10 = Very willing)', max=10, min=0, widget=widgets.RadioSelectHorizontal)
    survey_a_seconds = models.FloatField()
    survey_b_seconds = models.FloatField()
    survey_c_seconds = models.FloatField()
    survey_d_seconds = models.FloatField()
    survey_e_seconds = models.FloatField()
    tokens_passed = models.StringField(choices=[['None', 'None, so I get £60 and the other player gets £0'], ['20', '20, so I get £40 and the other player gets £40'], ['30', '30, so I get £30 and the other player gets £60'], ['60', 'All 60, so I get £0 and the other player gets 120£'], ['Other', 'An amount different from above']], label='Imagine you have 60 tokens to distribute between a player of your group and yourself. Imagine further that the token is worth 1£ to you and 2£ to the other player. How many tokens would you give the other player?', widget=widgets.RadioSelect)
    CRT2_1 = models.IntegerField(label='If you’re running a race and you pass the person in second place, what place are you in? (Enter the number)', min=0)
    CRT_1 = models.CurrencyField(label='A bat and a ball cost £1.10 in total. The bat costs £1.00 more than the ball. How much does the ball cost? (Enter the number of £)', min=0)
    CRT2_2 = models.IntegerField(label='A farmer had 15 sheep and all but 8 died. How many are left? (Enter the number of sheep)', min=0)
    CRT_2 = models.FloatField(label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets? (Enter the number of minutes)', min=0)
    CRT2_3 = models.StringField(label='Emily’s father has three daughters. The first two are named April and May. What is the third daughter’s name?')
    CRT_3 = models.FloatField(label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake? (Enter the number of days)', min=0)
    CRT2_4 = models.FloatField(label='How many cubic feet of dirt are there in a hole that is 3’ deep x 3’ wide x 3’ long? (Enter the number of cubic feet)', min=0)
    social_utility_explanation = models.LongStringField(label='In no more than three sentences, why do you think that happened?')
    social_utility_affect = models.StringField(label='In a few words, how do you feel about it?')
    social_utility_plan = models.LongStringField(label='If you would prefer a different result, describe in no more than three sentences what result and how could it be achieved (or type “No change”).')
    disparity_explanation = models.LongStringField(label='In no more than three sentences, why do you think that happened?')
    disparity_affect = models.StringField(label='In a few words, how do you feel about it?')
    disparity_plan = models.LongStringField(label='If you would prefer a different result, describe in no more than three sentences what result and how could it be achieved (or type “No change”).')
    disparity_unity = models.IntegerField(choices=[[0, '0%'], [25, '25%'], [50, '50%'], [75, '75%'], [100, '100%']], label='What percentage of other players do you think would share your goal?', widget=widgets.RadioSelectHorizontal)
    social_utility_unity = models.IntegerField(choices=[[0, '0%'], [25, '25%'], [50, '50%'], [75, '75%'], [100, '100%']], label='What percentage of other players do you think would share your goal?', widget=widgets.RadioSelectHorizontal)
    percieved_aim = models.StringField(label='In two to three words, what do you think this experiment was about? ')
    survey_f_seconds = models.FloatField()
    Big5_1 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...is reserved. ', widget=widgets.RadioSelectHorizontal)
    Big5_2 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label=' ...is generally trusting.', widget=widgets.RadioSelectHorizontal)
    Big5_3 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...tends to be lazy.', widget=widgets.RadioSelectHorizontal)
    Big5_4 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...is relaxed, handles stress well.', widget=widgets.RadioSelectHorizontal)
    Big5_5 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...has few artistic interests.', widget=widgets.RadioSelectHorizontal)
    Big5_6 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...is outgoing, sociable.', widget=widgets.RadioSelectHorizontal)
    Big5_7 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...tends to find fault with others.', widget=widgets.RadioSelectHorizontal)
    Big5_8 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...does a thorough job.', widget=widgets.RadioSelectHorizontal)
    Big5_9 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...gets nervous easily.', widget=widgets.RadioSelectHorizontal)
    Big5_10 = models.IntegerField(choices=[[1, 'Strongly disagree'], [2, 'Disagree'], [3, 'Neither agree nor disagree'], [4, 'Agree'], [5, 'Strongly agree']], label='...has an active imagination.', widget=widgets.RadioSelectHorizontal)
class Page1(Page):
    form_model = 'player'
    form_fields = ['percieved_aim', 'instruction_difficulty']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_a_seconds = time.time() - participant.time
        participant.time = time.time()
class Page2(Page):
    form_model = 'player'
    form_fields = ['final_strategy', 'tokens_passed']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_b_seconds = time.time() - participant.time
        participant.time = time.time()
class Page3(Page):
    form_model = 'player'
    form_fields = ['CRT2_1', 'CRT_1', 'CRT2_2', 'CRT_2', 'CRT2_3', 'CRT_3', 'CRT2_4', 'risk_proclivity']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_c_seconds = time.time() - participant.time
        participant.time = time.time()
class Page4(Page):
    form_model = 'player'
    form_fields = ['Big5_1', 'Big5_2', 'Big5_3', 'Big5_4', 'Big5_5', 'Big5_6', 'Big5_7', 'Big5_8', 'Big5_9', 'Big5_10']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_f_seconds = time.time() - participant.time
        participant.time = time.time()
class Page5(Page):
    form_model = 'player'
    form_fields = ['social_utility_explanation', 'social_utility_affect', 'social_utility_plan', 'social_utility_unity']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        participant = player.participant
        socialUtility = sum([p.participant.payoff for p in group.get_players() if p.participant.id_in_session in participant.ids_in_group])
        return dict(
            utility = socialUtility,
            shortfall = session.max_social - socialUtility,
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_d_seconds = time.time() - participant.time
        participant.time = time.time()
class Page6(Page):
    form_model = 'player'
    form_fields = ['disparity_explanation', 'disparity_affect', 'disparity_plan', 'disparity_unity']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        participant = player.participant
        payoffs = [p.participant.payoff for p in group.get_players() if p.participant.id_in_session in participant.ids_in_group]
        return dict(
            highest = max(payoffs),
            lowest = min(payoffs),
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        player.survey_e_seconds = time.time() - participant.time
        participant.time = time.time()
class End(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.disconnected
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        participant = player.participant
        from os import environ
        participant.finished = True
        return dict(
            total=participant.payoff + session.config.get("participation_fee"),
            wins=int(participant.payoff / session.prize),
            completion_url=environ.get('OTREE_COMPLETION_URL'), 
        )
page_sequence = [Page1, Page2, Page3, Page4, Page5, Page6, End]