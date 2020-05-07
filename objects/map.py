import pygame


class Map:
    def __init__(self, screen):
        self.screen = screen

        self.map_surface = pygame.image.load('images/risk-board.jpg')
        self.map_x, self.map_y = 10000, 14880

        self.cached_scaled_map = {}

    def draw(self, scale, x_mod, y_mod):

        if scale in self.cached_scaled_map:
            scaled_map = self.cached_scaled_map[scale]
        else:
            scaled_map =  pygame.transform.scale(self.map_surface, (int(self.map_x / scale), int(self.map_y / scale)))
            self.cached_scaled_map[scale] = scaled_map

        self.screen.blit(scaled_map, (int(x_mod), int(y_mod)), area=None, special_flags=0)
