import pygame
import const


class StartGameScreen:
    def __init__(self, screen, player_input):
        self.screen = screen
        self.player_input = player_input
        self.dt = 0

    def loop(self, dt):
        inputs = self.player_input.get_inputs()
        if inputs['exit']:
            return const.EXIT, None
        elif inputs['return']:
            return const.LOAD_GAME_GUI, None
        self.dt += dt

        self.screen.fill([225, 225, 225])

        pygame.display.update()

        return const.CONTINUE, None
