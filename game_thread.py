import threading
from queue import Queue
import time
from game import RiskGame
import const


class GameWorker(threading.Thread):
    def __init__(self, player_to_game_queue, game_to_player_queues, game_to_ui_queue):
        threading.Thread.__init__(self)

        self.player_to_game_queue = player_to_game_queue
        self.game_to_player_queues = game_to_player_queues
        self.game_to_ui_queue = game_to_ui_queue

        self.risk_game = RiskGame(players=len(self.game_to_player_queues))

        for x, queue in enumerate(self.game_to_player_queues):
            base_state = self.risk_game.state.player_state(x)
            base_state.append(x)
            queue.put(base_state)

        self.game_to_ui_queue.put(self.risk_game.state.game_state())

    def run(self):
        while True:
            request = self.player_to_game_queue.get()
            if request == 'kill':
                break
            result = self.risk_game.action(request)

            # Add the state to the correct queues
            self.game_to_player_queues[self.risk_game.current_player()].put(result)
            self.game_to_ui_queue.put(self.risk_game.state.game_state())


class GameThread:
    def __init__(self, player_to_game_queue, game_to_player_queues, game_to_ui_queue):
        self.player_to_game_queue = player_to_game_queue

        self.worker = GameWorker(player_to_game_queue, game_to_player_queues, game_to_ui_queue)
        self.worker.start()

    def close(self):
        self.player_to_game_queue.put('kill')

    def __del__(self):
        self.close()


if __name__ == '__main__':
    PLAYERS = 5

    player_to_game_queue = Queue()
    game_to_player_queues = [Queue() for x in range(PLAYERS)]
    game_to_ui_queue = Queue()

    game_thread = GameThread(player_to_game_queue, game_to_player_queues, game_to_ui_queue)

    try:
        print('game_to_player_queues')
        for queue in game_to_player_queues:
            print(queue.get())
        print('game_to_ui_queue')
        print(game_to_ui_queue.get())

        # Put in a dummy action
        player_to_game_queue.put('Test')

        x = 0
        while x < PLAYERS:
            try:
                print(f'Player {x} state:')
                result = game_to_player_queues[x].get(timeout=2)
                print(result)
            except:
                print('None')
                pass
            x += 1

        print('Game State')
        result = game_to_ui_queue.get(timeout=2)
        print(result)

    except:
        game_thread.close()
    finally:
        game_thread.close()
