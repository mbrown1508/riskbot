import threading
from queue import Queue
import time
from ai import Ai
import const


class AiWorker(threading.Thread):
    def __init__(self, ai, player_to_game_queue, game_to_player_queue):
        threading.Thread.__init__(self)

        self.player_to_game_queue = player_to_game_queue
        self.game_to_player_queue = game_to_player_queue

        self.ai = ai

    def run(self):
        while True:
            state = self.game_to_player_queue.get()
            if state == 'kill':
                break
            result = self.ai.action(state)

            # Add the state to the correct queues
            self.player_to_game_queue.put(result)


class AiThread:
    def __init__(self, ai, player_to_game_queue, game_to_player_queue, name='AI'):
        self.type = 'ai_thread'
        self.name = name
        self.game_to_player_queue = game_to_player_queue

        self.worker = AiWorker(ai, player_to_game_queue, game_to_player_queue)
        self.worker.start()

    def close(self):
        self.game_to_player_queue.put('kill')

    def __del__(self):
        self.close()


if __name__ == '__main__':
    PLAYERS = 5

    player_to_game_queue = Queue()
    game_to_player_queue = Queue()

    ai = Ai(player_to_game_queue, game_to_player_queue)

    ai_thread = AiThread(ai, player_to_game_queue, game_to_player_queue)

    try:
        for x in range(10):
            pass

    except Exception as e:
        ai_thread.close()
    finally:
        ai_thread.close()
