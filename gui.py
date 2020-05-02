import pygame

import const

from gui_player import GuiPlayer
from territory_data import TERRITORY_DATA
from objects.territory import Territory
from objects.map import Map
from transport_queue import TransportQueue
from gui_scaler import GuiScaler
from fontloader import FontLoader


class Gui:
    def __init__(self):
        self.game_transport = TransportQueue()
        self.ui_transport = TransportQueue()
        self.font_loader = FontLoader()
        self.game_state = None

        self.players = [GuiPlayer(self.game_transport, self.game_state) for _ in range(6)]

        self.map_surface = pygame.image.load('risk-board.jpg')
        self.map_x, self.map_y = 10000, 14880

        pygame.init()

        info_object = pygame.display.Info()
        screen_x, screen_y = info_object.current_w, info_object.current_h
        self.scaler = GuiScaler(screen_x, screen_y)

        self.screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)

        pygame.display.set_caption('Risk : Game of Thrones')

        # Objects
        self.map = Map(self.screen)
        self.territorys = [Territory(self.screen, x['name'], x['coords'], x['center'], p[0], p[1], self.font_loader) for x, p in zip(TERRITORY_DATA, self.game_state.player_pieces)]

        try:
            self.main_loop()
        finally:
            self.ui_transport.close()
            self.game_transport.close()

            pygame.quit()

    def main_loop(self):
        running = True
        while running:
            scale, x_mod, y_mod = self.scaler.get_scalers()
            # This will be any web call results we have to make, should always just be state

            result = self.game_transport.get()
            if result:
                print(result)
                self.game_state = result

            for event in pygame.event.get():
                # Handle QUIT
                if event.type == pygame.QUIT:
                    running = False
                    break

                # Handle KEYDOWN
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_EQUALS:
                        self.scaler.scale_up()
                    elif event.key == pygame.K_MINUS:
                        self.scaler.scale_down()
                    elif event.key == pygame.K_UP:
                        self.scaler.y_down()
                    elif event.key == pygame.K_DOWN:
                        self.scaler.y_up()
                    elif event.key == pygame.K_RIGHT:
                        self.scaler.x_up()
                    elif event.key == pygame.K_LEFT:
                        self.scaler.x_down()

                # Handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(self.scaler.scale_point(pos))

                    if self.game_state is not None:
                        for territory in self.territorys:
                            if territory.collide(pos, scale, x_mod, y_mod):
                                # print('Territory Clicked: {}'.format(territory.name))
                                territory.select()

            self.screen.fill(const.BLACK)

            self.map.draw(scale, x_mod, y_mod)
            for territory in self.territorys:
                territory.draw(scale, x_mod, y_mod)

            pygame.display.flip()
