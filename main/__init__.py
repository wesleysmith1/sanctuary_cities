from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 15
    
    INCOME = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    work_completed = models.IntegerField(initial=0)
    earnings = models.IntegerField(initial=0)
    selected_to_steal = models.IntegerField(blank=True)
    steal_from = models.IntegerField()
    report = models.BooleanField(label="Would you like to report the player that stole from you?")


# PAGES
class RoundStartWait(WaitPage):
    pass


class WorkingStage(Page):
    timeout_seconds = 60
    
    @staticmethod
    def live_method(player, data):
        print('received a bid from', player.id_in_group, ':', data)
        if data == True:
            player.work_completed += 1
            player.earnings += C.INCOME


class WorkingStageWait(WaitPage):
    pass


class StealingStage(Page):
    form_model = 'player'
    form_fields = ['selected_to_steal']


class StealingStageWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            print(player.id_in_group)
            players = [p for p in player.get_others_in_group() if p.field_maybe_none('selected_to_steal') == player.id_in_group]
                        
            if len(players) > 1:
                # randomly select who to steal from
                rand_player = random.choose(players)
                rand_player.steal_from = player.id_in_group
                print(f"The selected player to steal from {player.id_in_group} is {rand_player.id_in_group}.")
                pass
            elif len(players) == 1:
                # assign final steal
                players[0].steal_from = player.id_in_group
                print(f"Only {players[0].id_in_group} selected to steal from {player.id_in_group}.")
                pass
            else:
                # player chose not to steal
                print(f"Nobody stole from {player.id_in_group}")
                continue

def get_stealing_player(player):
    for p in player.get_others_in_group():
        if p.steal_from == player.id_in_group:
            return p.id_in_group
    return None

class ReportingStage(Page):
    form_model = "player"
    form_fields = ["report"]
    
    @staticmethod
    def is_displayed(player: Player):
        return len([p for p in player.get_others_in_group() if p.field_maybe_none('steal_from') == player.id_in_group]) > 0
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            stealing_player=get_stealing_player(player),
        )


page_sequence = [RoundStartWait, WorkingStage, WorkingStageWait, StealingStage, StealingStageWait, ReportingStage]
