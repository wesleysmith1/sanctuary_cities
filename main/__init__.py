from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class RoundStartWait(WaitPage):
    pass


class WorkingStage(Page):
    pass


class WorkingStageWait(WaitPage):
    pass


class StealingStage(Page):
    pass


class StealingStageWait(WaitPage):
    pass


class ReportingStage(Page):
    pass


page_sequence = [RoundStartWait, WorkingStage, WorkingStageWait, StealingStage, StealingStageWait, ReportingStage]
