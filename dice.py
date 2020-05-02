import random
import logging
from helper_functions import load_obj, save_obj


class Dice:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed = seed
        self.simulation_data = {}
        self.simulation_data_available = False

    def roll(self, dice_count=1):
        return [random.randint(1,6) for _ in range(dice_count)]

    def _determine_individual_roll_result(self, attacker_dice, defender_dice):
        attackers_rolls = self.roll(attacker_dice)
        defenders_rolls = self.roll(defender_dice)

        sorted(attackers_rolls, reverse=True)
        sorted(defenders_rolls, reverse=True)

        # attacker/defender
        deaths = [0, 0]

        if attackers_rolls[0] > defenders_rolls[0]:
            deaths[1] += 1
        else:
            deaths[0] += 1

        if attacker_dice > 1 and defender_dice > 1:
            if attackers_rolls[1] > defenders_rolls[1]:
                deaths[1] += 1
            else:
                deaths[0] += 1

        return deaths

    def determine_attack_result(self, attacker_dice, defender_dice, interactive=False):
        dice = [attacker_dice, defender_dice]
        while True:
            deaths = self._determine_individual_roll_result(
                3 if dice[0] > 2 else dice[0],
                2 if dice[1] > 1 else dice[1]
            )

            dice[0] -= deaths[0]
            dice[1] -= deaths[1]

            if min(dice) == 0:
                return dice

    def monticarlo_simulate_result(self, attacker_dice, defender_dice, simulations=1000, percentage=True):
        if self.simulation_data_available and percentage and attacker_dice <= 200 and defender_dice <=200:
            return self.simulation_data[(attacker_dice, defender_dice)]

        results = {**{(x, 0): 0 for x in range(1, attacker_dice+1)},
                   **{(0, x): 0 for x in range(1, defender_dice+1)}}

        for _ in range(simulations):
            result = self.determine_attack_result(attacker_dice, defender_dice)
            result = tuple(result)

            results[result] += 1

        if percentage:
            return_set = {}
            for x, y in results.items():
                return_set[x] = y/simulations
            return return_set
        else:
            return results

    def pretty_print_monticarlo_result(self, result):
        total_attacking, total_defending = 0, 0
        for x in result:
            if x[0] > total_attacking:
                total_attacking = x[0]
            if x[1] > total_defending:
                total_defending = x[1]

        attacker_percentage = 0
        defender_percentage = 0
        for x, y in result.items():
            if x[0] == 0:
                defender_percentage += y
            else:
                attacker_percentage += y

        print('Attacker Wins: {:2.2f}% : Defender Wins {:2.2f}%'.format(
            attacker_percentage*100,
            defender_percentage*100)
        )

        print('Attacker Wins By:')
        for x in range(total_attacking, 0, -1):
            print('{:4} : {:2.2f}%'.format(x, result[(x, 0)]*100))

        print('Defender Wins By:')
        for x in range(1, total_defending+1):
            print('{:4} : {:2.2f}%'.format(x, result[(0, x)] * 100))

    def create_simulation_data(self, max_attacker_dice, max_defender_dice, simulations,
                                filename='simulation-data', save=False):
        self.simulation_data = {}
        for attacker_dice in range(1, max_attacker_dice+1):
            for defender_dice in range(1, max_defender_dice+1):
                self.simulation_data[(attacker_dice, defender_dice)] = dice.monticarlo_simulate_result(attacker_dice,
                                                                                          defender_dice,
                                                                                          simulations=simulations,
                                                                                          percentage=True)
                print('Created ({}, {})'.format(attacker_dice, defender_dice))

        if save:
            save_obj(self.simulation_data, filename)

        self.simulation_data_available = True

    def load_simulation_data(self, filename='simulation-data'):
        self.simulation_data = load_obj(filename)
        self.simulation_data_available = True


if __name__ == '__main__':
    dice = Dice()
    dice.load_simulation_data('simulation-data-100000')

    #dice.create_simulation_data(100, 100, 100000, save=True)
    #dice.load_simulation_data()

    result = dice.monticarlo_simulate_result(5, 3, simulations=100000, percentage=True)
    dice.pretty_print_monticarlo_result(result)