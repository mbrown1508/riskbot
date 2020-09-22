import pygame
import random

import const

from queue import Queue, Empty

from game_thread import GameThread
from ai_thread import AiThread
from player import Player, MockQueue
from ai import Ai
from state import State
from objects.button import Button

from const_ui import TERRITORY_DATA
from objects.territory import Territory
from objects.map import Map
from gui_scaler import GuiScaler
from fontloader import FontLoader


class Gui:
    def __init__(self, screen, player_input, font_loader, player_count, ai_count):
        self.screen = screen
        self.player_input = player_input
        self.font_loader = font_loader
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
        self.screen_x, self.screen_y = info_object.current_w, info_object.current_h
        self.scaler = GuiScaler(self.screen_x, self.screen_y)
        self.scale, self.x_mod, self.y_mod = 5, 5, 5

        # Objects
        self.map = Map(self.screen)
        self.territorys = [Territory(self.screen, x['name'], x['coords'], x['center'], p[0], p[1], self.font_loader) for x, p in zip(TERRITORY_DATA, self.game_state.player_pieces)]
        self.buttons = [
            # stage buttons
            Button(screen, font_loader, 50, self.screen_y//2, 300, 50, value='Generate Armies', method=None)
        ]

        self.gui_state = ''



        self.set_new_game_state()



    def create_game(self):
        # Create the Queues
        player_to_game_queue = Queue()
        self.game_to_ui_queue = Queue()

        game_to_player_queues = []
        self.players = []

        create_queue = ['player' for _ in range(self.player_count)] + ['ai' for _ in range(self.ai_count)]
        random.shuffle(create_queue)

        for x, player_type in enumerate(create_queue):
            if player_type == 'player':
                game_to_player_queues.append(MockQueue())
                player = Player(player_to_game_queue, const.PLAYER_NAMES[x])
                self.ui_players.append(player)
                self.players.append(player)
            elif player_type == 'ai':
                game_to_player_queues.append(Queue())
                ai = Ai()
                ai_thread = AiThread(ai, player_to_game_queue, game_to_player_queues[x], name=const.AI_NAMES[x])
                self.ai_threads.append(ai_thread)
                self.players.append(ai_thread)
            else:
                raise Exception('invalid player type')

        self.game_thread = GameThread(player_to_game_queue, game_to_player_queues, self.game_to_ui_queue)

        state = self.game_to_ui_queue.get()
        self.game_state = State(state=state)

    def draw_ui(self):
        # Draw the ui that always has to be drawn
        self.draw_player_ui()

    def draw_player_ui(self):
        # Show ui specific to the player

        self.draw_left_panel()
        self.draw_right_panel()
        self.draw_current_player()

        self.draw_army_sizes()

        for button in self.buttons:
            button.draw(scale=1)

    def draw_army_sizes(self):
        army_sizes = self.count_army_sizes()

        font_size = int(self.screen_y // 24 / 1.4)
        modifier = font_size // 24

        for x, player in enumerate(self.players):
            if player.type == 'player':
                player_string = f"Player {x+1}: {army_sizes[x]}"
            else:
                player_string = f"AI Player {x+1}: {army_sizes[x]}"

            text = self.font_loader.create_text(player_string, font_size, const.PLAYER_COLOURS[x])
            text_x, text_y = text.get_size()
            self.screen.blit(text, (((self.screen_x - 200) - text_x // 2), ((self.screen_y // 20) - text_y // 2 + modifier + ((self.screen_y // 28)*(x+1)))))

    def count_army_sizes(self):
        counts = [0 for _ in range(self.player_count+self.ai_count)]
        for player, pieces in self.game_state.player_pieces:
            counts[player] += pieces
        return counts

    def draw_left_panel(self):
        ## Show left pannel ##
        # alpha fill
        s = pygame.Surface((400, self.screen_y))  # the size of your rect
        s.set_alpha(200)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates
        # Line
        pygame.draw.line(self.screen, (255,255,255),(400,0),(400,self.screen_y),5)

    def draw_right_panel(self):
        ## Show right pannel ##
        # alpha fill
        s = pygame.Surface((400, self.screen_y))  # the size of your rect
        s.set_alpha(200)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (self.screen_x-400, 0))  # (0,0) are the top-left coordinates
        # Line
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_x - 400, 0), (self.screen_x - 400, self.screen_y), 5)
        # Horizontals
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_x - 400, self.screen_y//3), (self.screen_x, self.screen_y//3), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_x - 400, (self.screen_y*2)//3), (self.screen_x, (self.screen_y*2)//3), 5)

    def draw_current_player(self):
        # Current Player & Type
        current_player = self.game_state.player_turn
        type = self.players[current_player].type
        colour = const.PLAYER_COLOURS[current_player]
        current_player += 1

        if type == 'player':
            text_str = f"Player {current_player}"
        else:
            text_str = f"AI Player {current_player}"

        font_size = int(self.screen_y//20 / 1.4)
        modifier = font_size//16

        text = self.font_loader.create_text(text_str, font_size, colour)
        text_x, text_y = text.get_size()
        self.screen.blit(text, (((self.screen_x-200)-text_x//2), ((self.screen_y//50)-text_y//2+modifier)))

    def draw_board(self):
        # Draw the screen
        self.screen.fill(const.BLACK)
        self.map.draw(self.scale, self.x_mod, self.y_mod)
        for territory in self.territorys:
            territory.draw(self.scale, self.x_mod, self.y_mod)

    def handle_button_presses(self, point):
        for button in self.buttons:
            if not button.hidden and not button.hidden:
                if button.collide(point):
                    # if not button.pressed_last_round:
                    button.pressed = True
                    # button.pressed_last_round = True
                # else:
                #     button.pressed_last_round = False

    def handle_territory_presses(self, pos):
        if self.game_state is not None:
            for territory in self.territorys:
                if territory.collide(pos, self.scale, self.x_mod, self.y_mod):
                    # if not territory.pressed_last_round:
                    territory.pressed = True
                    # territory.pressed_last_round = True
                # else:
                #     territory.pressed_last_round = False

    def generate_armies(self):
        pass

    def update_ui_after_state(self):
        last_state_update = self.game_state

    def set_new_game_state(self):
        # This is for the ui
        self.gui_state = None

        for button in self.buttons:
            button.disable()
            button.hide()

    def handle_inputs(self, inputs):
        # Handle KEYDOWN
        if inputs['equals']:
            self.scaler.scale_up()
        if inputs['minus']:
            self.scaler.scale_down()
        if inputs['up']:
            self.scaler.y_down()
        if inputs['down']:
            self.scaler.y_up()
        if inputs['right']:
            self.scaler.x_up()
        if inputs['left']:
            self.scaler.x_down()

        # Handle Key Clicks
        if inputs['mouse_button_up']:
            pos = inputs['mouse_pos']

            # print(self.scaler.scale_point(pos))

            self.handle_territory_presses(pos)
            self.handle_button_presses(pos)

    def get_state_update(self):
        try:
            state = self.game_to_ui_queue.get(block=False)
            self.game_state = State(state=state)
            return True
        except Empty:
            return False

    def loop(self, dt):
        # Get the map scaling
        self.scale, self.x_mod, self.y_mod = self.scaler.get_scalers()

        # Update game state if it exists
        if self.get_state_update():
            self.update_ui_after_state()
            print(f"New State: {self.game_state}")

        # Handle Player Inputs
        inputs = self.player_input.get_inputs()
        if inputs['exit']:
            return const.LOAD_GAME_SELECT, None
        self.handle_inputs(inputs)

        # Start Changes

        if self.players[self.game_state.player_turn].type == 'player':
            if self.gui_state is None and \
                    (self.game_state.last_action == const.NEW_GAME or self.game_state.last_action == const.NEXT_TURN):
                # We have just got a state update but not selected the next action
                self.enable_buttons(['Generate Armies'])
                self.gui_state = 'wait_for_selection'
                self.clear_pressed_buttons()
                print(f"New GUI State: {self.gui_state}")

                # TODO: Show the units available

            elif self.gui_state == 'wait_for_selection':
                for button in self.buttons:
                    if button.value == 'Generate Armies':
                        if button.pressed:
                            self.gui_state = 'select_reinforce_territory'
                            print(f"New GUI State: {self.gui_state}")
                            self.enable_buttons([])
                            self.clear_pressed_territories()
                            button.pressed = False

            elif self.gui_state == 'select_reinforce_territory':
                for territory in self.territorys:
                    if territory.pressed:
                        self.clear_highlighted_territories()
                        territory.highlight()
                        territory.pressed = False

                        # TODO: Show the number selector

                        # TODO: Update the number selector

                        # TODO: If all units placed, show accept button








        # End Changes

        self.draw_board()
        self.draw_ui()

        pygame.display.flip()

        return const.CONTINUE, None

    def enable_buttons(self, buttons):
        for button in self.buttons:
            if button.value in buttons:
                button.enable()
                button.unhide()
            else:
                button.disable()
                button.hide()

    def clear_pressed_buttons(self):
        for button in self.buttons:
            button.pressed = False

    def clear_pressed_territories(self):
        for territory in self.territorys:
            territory.pressed = False

    def clear_highlighted_territories(self):
        for territory in self.territorys:
            territory.highlighted = False
