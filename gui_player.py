import const


class GuiPlayer:
    def __init__(self, transport, game_state):
        self.transport = transport
        self.game_state = game_state

    def check_actions(self):
        if self.gui_state.create_game:
            if self.gui_state.players_input in [2,3,4,5,6]:
                self.transport.put([const.CREATE_GAME, self.gui_state.players_input])
