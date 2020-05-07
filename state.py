import random
import const

# 30 Singles
# 15 Triples
# 75 max army size

# minimum armies is 3 per turn
# horse=4, catapult=5, castle=6, mix=7
# 2 bonus troops if the territories match
# if you eleminate someone you take their cards


class State:
    def __init__(self, players=None, state=None):
        self.turn = 0
        self.player_turn = 0
        self.player_pieces = []
        self.player_cards = []
        self.player_card_counts = []
        self.deck = []
        self.last_action = const.NEW_GAME
        self.last_action_details = []

        if state is None:
            self.players = players
            self.player_turn = random.randint(0,players)
            self.set_starting_board()
            self.shuffle_deck()
            self.player_cards = [[] for _ in range(players)]
            self.player_card_counts = [0 for _ in range(self.players)]
        else:
            self.set_state(state)

    def set_state(self, state):
        # This will set the state based on a list passed to the class
        self.players = state[1]
        self.player_turn = state[2]
        self.turn = state[3]
        self.player_pieces = [[x, y] for x, y in (zip(state[4:const.TOTAL_LOCATIONS+4],
                                                      state[const.TOTAL_LOCATIONS+4: const.TOTAL_LOCATIONS*2+4]))]
        self.player_card_counts = state[const.TOTAL_LOCATIONS * 2 + 4:const.TOTAL_LOCATIONS * 2 + 4 + self.players]
        if state[0] == const.PLAYER_STATE:
            start = const.TOTAL_LOCATIONS*2+4+self.players
            card_count = state[start]
            self.player_cards = state[start+1:start+1+card_count]
            self.last_action = state[start+1+card_count]
            self.last_action_details = state[start+1+card_count+1:]

        elif state[0] == const.GAME_STATE:
            start = const.TOTAL_LOCATIONS*2+4+self.players
            self.player_cards = []
            rolling_total = 0
            for x in self.player_card_counts:
                self.player_cards.append(state[start+rolling_total:start+x])
                rolling_total += x

            card_totals = state[start+rolling_total]
            self.deck = state[start+rolling_total+1:start+rolling_total+1+card_totals]

            start = start+rolling_total+1+card_totals
            self.last_action = state[start]
            self.last_action_details = state[start+1:]

    def player_state(self, player_number):
        # This will return the state based in a list that can be used to recreate the class

        # How many players is there 1 place
        # Current Player (1 place)
        # Turn Number (1 place)
        # Who owns each square 48 places
        # How many troops is on each square 48 places
        # How many cards each player has (#players places)
        # Player Cards (territory, symbol) - 2 * #player cards (from last section)

        # last action type (1 position) - THIS WILL DETERMINE THE STATE RETURNED

        # card awarded (who, territory, symbol) (3 positions)
        # battle result (attacking_territory, defending_territory, attacking_dead, defending_dead, a1, a2, a3, d1, d2)
        # move result (battle) (x_remain, x_move_to_territory)
        # move result (reenforce) (from_territory, to_territory, number)
        # place armies (number placed, (location, amouont) * for_each)
        # cards played (amount increased)
        # Generate armies (amount increased)
        # ended attack (from_territory, to_territory)
        # New player
        return [const.PLAYER_STATE, self.players, self.player_turn, self.turn] + \
               [x[0] for x in self.player_pieces] + \
               [x[1] for x in self.player_pieces] + \
               self.player_card_counts + \
               [len(self.player_cards[player_number])] + self.player_cards[player_number] + \
               [self.last_action] + self.last_action_details

    def generate_armies(self, player, total, territories, castles, regions):
        self.last_action = const.GENERATE_ARMIES
        self.last_action_details = [player, total, territories, castles, regions]

    def set_last_action(self, action, action_details):
        self.last_action = action
        self.last_action_details = action_details

    def game_state(self):
        return [const.GAME_STATE, self.players, self.player_turn, self.turn] + \
               [x[0] for x in self.player_pieces] + \
               [x[1] for x in self.player_pieces] + \
               self.player_card_counts + \
               [item for sublist in self.player_cards for item in sublist] + \
               [len(self.deck)] + self.deck + \
               [self.last_action] + self.last_action_details

    def shuffle_deck(self):
        # End card shuffled in bottom half
        deck = list(range(48))
        random.shuffle(deck)

        first_half = deck[:24]
        second_half = deck[24:]

        second_half += [49]
        random.shuffle(second_half)

        self.deck = first_half + second_half

    def set_starting_board(self):
        # All cards are dealt out in 3-6 players
        # 2 individual armies on each territory
        if self.players == 3:
            self.player_pieces = [[0, 2] for _ in range(const.TOTAL_LOCATIONS//3)] + \
                                 [[1, 2] for _ in range(const.TOTAL_LOCATIONS//3)] + \
                                 [[2, 2] for _ in range(const.TOTAL_LOCATIONS//3)]
        elif self.players == 4:
            self.player_pieces = [[0, 2] for _ in range(const.TOTAL_LOCATIONS // 4)] + \
                                 [[1, 2] for _ in range(const.TOTAL_LOCATIONS // 4)] + \
                                 [[2, 2] for _ in range(const.TOTAL_LOCATIONS // 4)] + \
                                 [[3, 2] for _ in range(const.TOTAL_LOCATIONS // 4)]
        elif self.players == 5:
            self.player_pieces = [[0, 2] for _ in range(const.TOTAL_LOCATIONS // 5)] + \
                                 [[1, 2] for _ in range(const.TOTAL_LOCATIONS // 5)] + \
                                 [[2, 2] for _ in range(const.TOTAL_LOCATIONS // 5+1)] + \
                                 [[3, 2] for _ in range(const.TOTAL_LOCATIONS // 5+1)] + \
                                 [[4, 2] for _ in range(const.TOTAL_LOCATIONS // 5+1)]
        elif self.players == 6:
            self.player_pieces = [[0, 2] for _ in range(const.TOTAL_LOCATIONS // 6)] + \
                                 [[1, 2] for _ in range(const.TOTAL_LOCATIONS // 6)] + \
                                 [[2, 2] for _ in range(const.TOTAL_LOCATIONS // 6)] + \
                                 [[3, 2] for _ in range(const.TOTAL_LOCATIONS // 6)] + \
                                 [[4, 2] for _ in range(const.TOTAL_LOCATIONS // 6)] + \
                                 [[5, 2] for _ in range(const.TOTAL_LOCATIONS // 6)]
        else:
            raise Exception('Invalid player count')

        random.shuffle(self.player_pieces)


if __name__ == '__main__':
    state = State(players=5)
    print(state)
    base_state = state.game_state()
    print(base_state)
    state_2 = State(state=base_state)
    base_state_2 = state_2.game_state()
    print(base_state_2)
    player_state = state_2.player_state(0)
    print(player_state)
