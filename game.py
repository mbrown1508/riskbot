import random
import const
from state import State
from dice import Dice

# 30 Singles
# 15 Triples
# 75 max army size

# minimum armies is 3 per turn
# horse=4, catapult=5, castle=6, mix=7
# 2 bonus troops if the territories match
# if you eleminate someone you take their cards


class RiskGame:
    def __init__(self, players=None, state=None):
        if state is None and players is not None:
            self.state = State(players=players)
        elif state is not None:
            self.state = State(state=state)
        else:
            self.state = None
            self.assigned_players = []

        self.dice = Dice()


    # Place Army x amount
    # Play cards
    # Attack - normal or blitz
    # reinforce
    # Draw card
    # Next Player

    def current_player(self):
        return self.state.player_turn

    def action(self, data):
        # currently returns the current players data
        return self.state.player_state(self.current_player())

    def create_game(self, players):
        self.state = State(players=players)
        return self.add_player()

    def add_player(self):
        remaining_numbers = []
        for x in range(self.state.players):
            if x not in self.assigned_players:
                remaining_numbers.append(x)

        player_number = random.choice(remaining_numbers)
        self.assigned_players.append(player_number)

        if len(remaining_numbers) == 1:
            self.state.set_last_action(const.ADD_PLAYER, [player_number, 1])
        else:
            self.state.set_last_action(const.ADD_PLAYER, [player_number, 0])
        return self.state.player_state(player_number)

    def generate_armies(self, player):
        if self.state.player_turn != player:
            return const.INVALID_MOVE, self.state.player_state(player)

        # Count territories
        # Count castles
        # Count regions
        owned_territories = []
        territories = 0
        castles = 0
        regions = 0
        for region, player_pieces in enumerate(self.state.player_pieces):
            if player_pieces[0] == player:
                owned_territories.append(region)
                territories += 1
                if const.TERRITORIES[region]['castle'] == True:
                    castles += 1

        for region in const.REGIONS:
            all_territories = True
            for territory in region['territories']:
                if territory not in owned_territories:
                    all_territories = False

            if all_territories:
                regions += region['bonus']

        total = territories + castles + regions
        self.state.generate_armies(player, total, territories, castles, regions)

        return const.SUCCESS, self.state.player_state(player)
