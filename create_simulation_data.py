from multiprocessing import Process, Queue
from dice import Dice
from helper_functions import save_obj, load_obj
import time


def dice_worker(work_queue, result_queue, worker_number):
    print(f'Worker {worker_number} started')
    dice = Dice()
    attempt = 0
    while True:
        try:
            work = work_queue.get(timeout=1)
        except Exception as e:
            if attempt < 5:
                attempt += 1
                time.sleep(0.1)
                # print(f'Found Exception: {e}')
                continue
            else:
                return

        print('Starting ({}, {})'.format(work[0], work[1]))
        result = dice.monticarlo_simulate_result(work[0], work[1], simulations=work[2], percentage=True)

        result_queue.put([(work[0], work[1]), result])


def save_entry(filename, result):
    try:
        data = load_obj(filename)
    except:
        data = {}

    data[result[0]] = result[1]

    save_obj(data, filename)


if __name__ == '__main__':
    max_attacker_dice = 25
    max_defender_dice = 25
    simulations = 100000
    filename = 'simulation-data-100000'
    save = True
    workers = 10

    result_queue = Queue()
    work_queue = Queue()

    previous_data = load_obj(filename)

    for attacker_dice in range(1, max_attacker_dice + 1):
        for defender_dice in range(1, max_defender_dice + 1):
            if (attacker_dice, defender_dice) in previous_data:
                print('Skipping ({}, {})'.format(attacker_dice, defender_dice))
                continue
            work_queue.put([attacker_dice, defender_dice, simulations])
            print('Added ({}, {}) to Queue'.format(attacker_dice, defender_dice))

    processes = []
    for x in range(workers):
        processes.append(Process(target=dice_worker, args=(work_queue, result_queue, x)))
        print(f'Created Worker {x}')

    for x, process in enumerate(processes):
        process.start()
        print(f'Started Worker {x}')

    no_results = 0
    while no_results < 60:
        try:
            result = result_queue.get(timeout=1)
            save_entry(filename, result)
            print('Created ({}, {})'.format(result[0], result[1]))
            no_results = 0
        except:
            print('No results, waiting 1sec, timeout in {}sec'.format((60-no_results)))
            no_results += 1
            time.sleep(1)

    print('Process timed out')
