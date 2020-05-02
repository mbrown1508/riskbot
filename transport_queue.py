import threading
from queue import Queue
import time
from game import RiskGame
import const


class TransportThread(threading.Thread):
    def __init__(self, input, output):
        threading.Thread.__init__(self)
        self.input = input
        self.output = output
        # self.risk_game = RiskGame()

    def run(self):
        while True:
            request = self.input.get()
            if request == 'kill':
                self.output.put('dead')
                break
            result = self.risk_game.action(request)
            self.output.put(result)


class TransportQueue:
    def __init__(self):
        self.input = Queue()
        self.output = Queue()

        self.queue = TransportThread(self.input, self.output)
        self.queue.start()

    def put(self, data):
        self.input.put(data)

    def get(self):
        try:
            return self.output.get(block=False)
        except Exception as e:
            return False

    def close(self):
        while True:
            self.input.put('kill')
            result = self.output.get(block=True)
            if result == 'dead':
                break


if __name__ == '__main__':
    transport = TransportQueue()

    try:
        transport.put([const.CREATE_GAME, 4])

        while True:
            result = transport.get()
            if result:
                print(result)
            else:
                time.sleep(0.1)
    except:
        transport.close()