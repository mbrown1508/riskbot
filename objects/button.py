import pygame
import const
from fontloader import FontLoader


class Button:
    def __init__(self, screen, font_loader, x, y, width, height, key=None, value=None, method=None):
        self.screen = screen
        self.font_loader = font_loader

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.key = key
        self.value = value
        self.method = method

        self.font_size = int(self.height / 1.4)
        self.modifier = self.font_size//16
        self.font_colour = (0, 0, 0)

        self.enabled_fill = (0, 255, 0)
        self.enabled_outline = (0, 0, 0)

        self.disabled_fill = (60, 60, 60)
        self.disabled_outline = (0, 0, 0)

        self.enabled = False
        self.hidden = False

        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        if self.enabled:
            pygame.draw.rect(self.screen, self.enabled_fill, self.rectangle, 0)
            pygame.draw.rect(self.screen, self.enabled_outline, self.rectangle, 3)
        elif not self.hidden:
            pygame.draw.rect(self.screen, self.disabled_fill, self.rectangle, 0)
            pygame.draw.rect(self.screen, self.disabled_outline, self.rectangle, 3)
        else:
            return

        center = (self.x + self.width//2, self.y + self.height//2)

        text = self.font_loader.create_text(str(self.value), self.font_size, self.font_colour)
        text_x, text_y = text.get_size()
        self.screen.blit(text, ((center[0]-text_x//2), (center[1]-text_y//2+self.modifier)))

    def collide(self, point):
        if self.rectangle.collidepoint(point[0], point[1]) == 1:
            return True
        else:
            return False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def xor_enable(self):
        self.enabled = not self.enabled

    def hide(self):
        self.hidden = True

    def unhide(self):
        self.hidden = False

    def xor_hide(self):
        self.hidden = not self.hidden
