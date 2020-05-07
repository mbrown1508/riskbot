import pygame
import const


class LogoScreen:
    def __init__(self, screen, player_input):
        self.screen = screen
        self.player_input = player_input

        self.img = pygame.image.load('images/logo.png')

        self.position = ((self.screen.get_width() // 2) - (self.img.get_width() // 2),
                         (self.screen.get_height() // 2) - (self.img.get_height() // 2))

        self.dt = 0

    def loop(self, dt):
        inputs = self.player_input.get_inputs()

        if inputs['exit']:
            return const.LOAD_GAME_SELECT, None

        self.screen.fill([225, 225, 225])

        self.dt += dt

        if self.dt > 5000:
            return const.LOAD_GAME_SELECT, None

        self.screen.blit(self.img, self.position)

        pygame.display.update()

        return const.CONTINUE, None
