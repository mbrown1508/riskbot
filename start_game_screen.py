import pygame
import const
from fontloader import FontLoader
from objects.button import Button


class SelectBox:
    def __init__(self, screen, font_loader, x, y, size, key, value):
        self.screen = screen
        self.font_loader = font_loader

        self.x = x
        self.y = y
        self.size = size
        self.key = key
        self.value = value
        self.font_size = int(self.size / 1.4)
        self.modifier = self.font_size//16
        self.font_colour = (0, 0, 0)

        self.selected_fill = (255, 0, 255)
        self.selected_outline = (0, 0, 0)

        self.deselected_fill = (255, 255, 255)
        self.deselected_outline = (0, 0, 0)

        self.selected = False

        self.rectangle = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        if self.selected:
            pygame.draw.rect(self.screen, self.selected_fill, self.rectangle, 0)
            pygame.draw.rect(self.screen, self.selected_outline, self.rectangle, 3)
        else:
            pygame.draw.rect(self.screen, self.deselected_fill, self.rectangle, 0)
            pygame.draw.rect(self.screen, self.deselected_outline, self.rectangle, 3)

        center = (self.x + self.size//2, self.y + self.size//2)

        text = self.font_loader.create_text(str(self.value), self.font_size, self.font_colour)
        text_x, text_y = text.get_size()
        self.screen.blit(text, ((center[0]-text_x//2), (center[1]-text_y//2+self.modifier)))

    def collide(self, point):
        if self.rectangle.collidepoint(point[0], point[1]) == 1:
            return True
        else:
            return False

    def deselect(self):
        self.selected = False

    def select(self):
        self.selected = True

    def xor_select(self):
        self.selected = not self.selected


class SelectBoxes:
    def __init__(self, screen, font_loader, x, y, select_size, width, keys, values, label=None, value=None):
        self.screen = screen
        self.font_loader = font_loader

        self.x, self.y = x, y
        self.select_size = select_size
        self.width = width
        self.keys = keys
        self.values = values

        self.font_colour = (255, 255, 255)

        self.value = value
        self.label = label

        self.create_selects()

        if self.label is not None:
            self.text = self.font_loader.create_text(str(self.label), self.select_size, self.font_colour)
            text_x, text_y = self.text.get_size()

            y_middle = (self.select_size // 2) + self.y
            self.y_start = y_middle - (text_y // 2)
            self.x_start = self.x - text_x

            self.total_width = text_x + self.width

        self.select_value()

    def select_value(self):
        if self.value is not None:
            for select in self.selects:
                if select.key == self.value:
                    select.select()

    def create_selects(self):
        spacing = self.width // (len(self.keys)-1)

        self.selects = [
            SelectBox(self.screen, self.font_loader, self.x + (spacing * n), self.y, self.select_size, key, value) for
            n, (key, value) in enumerate(zip(self.keys, self.values))]

    def draw(self):
        for select in self.selects:
            select.draw()

        if self.label is not None:
            self.screen.blit(self.text, (self.x_start, self.y_start))

    def clicked(self, point):
        change_select = -1
        for x, select in enumerate(self.selects):
            if select.collide(point):
                change_select = x
                break

        if change_select > -1:
            self.value = self.selects[change_select].key
            for x, select in enumerate(self.selects):
                if x == change_select:
                    select.select()
                else:
                    select.deselect()

    def modify_x(self, modifier):
        self.x = self.x + modifier
        self.x_start = self.x_start + modifier

        self.create_selects()
        self.select_value()


class StartGameScreen:
    def __init__(self, screen, player_input, font_loader):
        self.screen = screen
        self.font_loader = font_loader
        self.player_input = player_input
        self.dt = 0

        screen_x, screen_y = self.screen.get_width(), self.screen.get_height()

        self.player_count_select = SelectBoxes(self.screen,
                                               self.font_loader,
                                               screen_x // 2,
                                               screen_y // 2 - 50,
                                               60,
                                               450,
                                               [0, 1, 2, 3, 4, 5, 6],
                                               [0, 1, 2, 3, 4, 5, 6],
                                               'Player Count: ',
                                               value=0)

        self.ai_count_select = SelectBoxes(self.screen,
                                           self.font_loader,
                                           screen_x // 2,
                                           screen_y // 2 + 50,
                                           60,
                                           450,
                                           [0, 1, 2, 3, 4, 5, 6],
                                           [0, 1, 2, 3, 4, 5, 6],
                                           'AI Count: ',
                                           value=0)

        self.start_button = Button(self.screen, self.font_loader, (screen_x-200) // 2, screen_y // 2 + 200, 200, 80, 0, 'START')

        modifier = (self.player_count_select.total_width - self.player_count_select.width) // 2
        self.player_count_select.modify_x(-modifier)
        self.ai_count_select.modify_x(-modifier)

        background = pygame.image.load('images/background.jpg')

        self.background = pygame.transform.scale(background, (screen_x, screen_y))

        self.title = self.font_loader.create_text('START GAME', 150, (255, 255, 255))
        text_x, text_y = self.title.get_size()
        self.title_x, self.title_y = (screen_x - text_x) // 2, screen_y // 2 - 250

    def draw_screen(self):
        pass

    def check_for_clicks(self):
        pass

    def loop(self, dt):
        inputs = self.player_input.get_inputs()
        if inputs['exit']:
            return const.EXIT, None
        self.dt += dt

        if inputs['mouse_button_up']:
            self.player_count_select.clicked(inputs['mouse_pos'])
            self.ai_count_select.clicked(inputs['mouse_pos'])

            if self.start_button.enabled:
                if self.start_button.collide(inputs['mouse_pos']):
                    return const.LOAD_GAME_GUI, [self.player_count_select.value, self.ai_count_select.value]

        if 2 <= (self.player_count_select.value + self.ai_count_select.value) <= 6:
            self.start_button.enable()
        else:
            self.start_button.disable()

        # self.screen.fill([225, 225, 225])
        self.screen.blit(self.background, (0, 0), area=None, special_flags=0)

        self.player_count_select.draw()
        self.ai_count_select.draw()
        self.start_button.draw(scale=1)

        self.screen.blit(self.title, (self.title_x, self.title_y))

        pygame.display.update()

        return const.CONTINUE, None
