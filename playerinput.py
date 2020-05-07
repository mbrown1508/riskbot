import pygame
import const


class PlayerInput:
    def __init__(self):
        pass

    def get_inputs(self):
        return_values = {
            'exit': False,
            'reset': False,
            'key_input': '',
            'backspace': False,
            'return': False,
            'equals': False,
            'minus': False,
            'up': False,
            'down': False,
            'right': False,
            'left': False,
            'mouse_button_up': False,
            'mouse_pos': -1,
        }

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_values['exit'] = True
                elif event.key == pygame.K_SPACE:
                    return_values['reset'] = True

                # Key Input
                if event.unicode.isalpha():
                    return_values['key_input'] += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    return_values['backspace'] = True
                elif event.key == pygame.K_RETURN:
                    return_values['return'] = True

                # Handle KEYDOWN
                if event.key == pygame.K_EQUALS:
                    return_values['equals'] = True
                elif event.key == pygame.K_MINUS:
                    return_values['minus'] = True
                elif event.key == pygame.K_UP:
                    return_values['up'] = True
                elif event.key == pygame.K_DOWN:
                    return_values['down'] = True
                elif event.key == pygame.K_RIGHT:
                    return_values['right'] = True
                elif event.key == pygame.K_LEFT:
                    return_values['left'] = True

            elif event.type == pygame.QUIT:
                return_values['exit'] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                return_values['mouse_button_up'] = True
                return_values['mouse_pos'] = pygame.mouse.get_pos()

        return return_values
