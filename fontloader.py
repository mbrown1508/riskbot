import pygame


class FontLoader:
    def __init__(self):
        self.cached_fonts = {}
        self.cached_text = {}

        self.font_preferences = [
            "Open Sans",
        ]

    def make_font(self, fonts, size):
        available = pygame.font.get_fonts()
        # get_fonts() returns a list of lowercase spaceless font names
        choices = map(lambda x: x.lower().replace(' ', ''), fonts)
        for choice in choices:
            if choice in available:
                return pygame.font.SysFont(choice, size)
        return pygame.font.Font(None, size)

    def get_font(self, font_preferences, size):
        key = str(font_preferences) + '|' + str(size)
        font = self.cached_fonts.get(key, None)
        if font is None:
            font = self.make_font(font_preferences, size)
            self.cached_fonts[key] = font
        return font

    def create_text(self, text, size, color, font_preferences=None):
        if font_preferences is None:
            font_preferences = self.font_preferences
        key = '|'.join(map(str, (font_preferences, size, color, text)))
        image = self.cached_text.get(key, None)
        if image is None:
            font = self.get_font(font_preferences, size)
            image = font.render(text, True, color)
            self.cached_text[key] = image
        return image
