import pygame

import const

from queue import Queue

from game_thread import GameThread
from ai_thread import AiThread
from player import Player, MockQueue
from ai import Ai
from state import State

from territory_data import TERRITORY_DATA
from objects.territory import Territory
from objects.map import Map
from gui_scaler import GuiScaler
from fontloader import FontLoader


class Gui:
    def __init__(self, screen, player_input, player_count, ai_count):
        self.screen = screen
        self.player_input = player_input
        self.player_count = player_count
        self.ai_count = ai_count

        # Create the game elements
        self.game_state = None

        self.players = []
        self.ui_players = []
        self.ai_threads = []
        self.game_thread = None
        self.game_to_ui_queue = None

        self.create_game()

        # Create the image elements
        self.font_loader = FontLoader()

        self.map_surface = pygame.image.load('images/risk-board.jpg')
        self.map_x, self.map_y = 10000, 14880

        info_object = pygame.display.Info()
        screen_x, screen_y = info_object.current_w, info_object.current_h
        self.scaler = GuiScaler(screen_x, screen_y)
        self.scale, self.x_mod, self.y_mod = 5, 5, 5

        # Objects
        self.map = Map(self.screen)
        self.territorys = [Territory(self.screen, x['name'], x['coords'], x['center'], p[0], p[1], self.font_loader) for x, p in zip(TERRITORY_DATA, self.game_state.player_pieces)]

    def create_game(self):
        # Create the Queues
        player_to_game_queue = Queue()
        self.game_to_ui_queue = Queue()

        # We need to add in mock queues for the players
        game_to_player_queues = [MockQueue() for x in range(self.player_count)]
        game_to_player_queues += [Queue() for x in range(self.player_count, self.player_count+self.ai_count)]

        self.game_thread = GameThread(player_to_game_queue, game_to_player_queues, self.game_to_ui_queue)

        for x in range(self.player_count):
            player = Player(player_to_game_queue)
            self.ui_players.append(player)

        for x in range(self.player_count, self.player_count+self.ai_count):
            ai = Ai()
            ai_thread = AiThread(ai, player_to_game_queue, game_to_player_queues[x])
            self.ai_threads.append(ai_thread)

        self.players = self.ui_players + self.ai_threads

        state = self.game_to_ui_queue.get()
        self.game_state = State(state=state)

    def handle_inputs(self, inputs):
        # Handle KEYDOWN
        if inputs['equals']:
            self.scaler.scale_up()
        if inputs['minus']:
            self.scaler.scale_down()
        if inputs['up']:
            self.scaler.y_down()
        if  inputs['down']:
            self.scaler.y_up()
        if inputs['right']:
            self.scaler.x_up()
        if inputs['left']:
            self.scaler.x_down()

        # Handle Key Clicks
        if inputs['mouse_button_up']:
            pos = inputs['mouse_pos']

            print(self.scaler.scale_point(pos))

            if self.game_state is not None:
                for territory in self.territorys:
                    if territory.collide(pos, self.scale, self.x_mod, self.y_mod):
                        # print('Territory Clicked: {}'.format(territory.name))
                        territory.select()

    def loop(self, dt):
        # Get the map scaling
        self.scale, self.x_mod, self.y_mod = self.scaler.get_scalers()

        # Handle Player Inputs
        inputs = self.player_input.get_inputs()
        if inputs['exit']:
            return const.LOAD_GAME_SELECT, None
        self.handle_inputs(inputs)

        # Draw the screen
        self.screen.fill(const.BLACK)
        self.map.draw(self.scale, self.x_mod, self.y_mod)
        for territory in self.territorys:
            territory.draw(self.scale, self.x_mod, self.y_mod)

        pygame.display.flip()

        return const.CONTINUE, None

