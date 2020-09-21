import pygame
import const

from playerinput import PlayerInput
from logoscreen import LogoScreen
from start_game_screen import StartGameScreen
from gui import Gui
from fontloader import FontLoader

pygame.init()

screen_info = pygame.display.Info()
x = screen_info.current_w
y = screen_info.current_h

depth = pygame.display.mode_ok((x, y), pygame.FULLSCREEN)
if depth == 0:
    raise(Exception('Invalid display mode'))

screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN, depth)
pygame.display.set_caption("Risk : Game of Thrones")

font_loader = FontLoader()


player_input = PlayerInput()
active = LogoScreen(screen, player_input)

run = True
clock = pygame.time.Clock()
while run:
    dt = clock.tick()

    result, args = active.loop(dt)

    if result == const.EXIT:
        run = False
    elif result == const.LOAD_GAME_SELECT:
        active = StartGameScreen(screen, player_input, font_loader)
    elif result == const.LOAD_GAME_GUI:
        active = Gui(screen, player_input, font_loader, args[0], args[1])

pygame.quit()
