import threading
import requests
from queue import Queue
import time
URL = 'homeserver'

class TransportThread(threading.Thread):
    def __init__(self, input, output):
        threading.Thread.__init__(self)
        self.input = input
        self.output = output

    def run(self):
        while True:
            request = self.input.get()
            if request == 'kill':
                self.output.put('dead')
                break
            result = requests.post(URL, data=request)
            self.output.put([request, result])


class TransportApi:
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
    transport = TransportApi()
    transport.put([5, 6, 3, 4])
    transport.put([8, 4])

    while True:
        result = transport.get()
        if result:
            print(result)
        else:
            time.sleep(0.1)
