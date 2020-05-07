import const


# This is passed to the game as the player makes use of the UI queue in the shared gui mode
class MockQueue:
    def __init__(self):
        pass

    def put(self, data):
        return


class Player:
    def __init__(self, player_to_game_queue):
        self.type = 'player'

        self.player_to_game_queue = player_to_game_queue
