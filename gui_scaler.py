import math


class GuiScaler:
    def __init__(self, screen_x, screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y

        self.map_x = 10000
        self.map_y = 14880

        self.scale = 0
        self.x_position = 3
        self.y_position = 5

        self.scaler = None
        self.x_offset = None
        self.y_offset = None

        self.recalculate()

    def get_scalers(self):
        return self.scaler, self.x_offset, self.y_offset

    def scale_point(self, point):
        return ((point[0]-self.x_offset)*self.scaler, (point[1]-self.y_offset)*self.scaler)

    def recalculate(self):
        if self.scale == 0:
            self.scaler = 14880 / self.screen_y
            self.x_offset = self.screen_x / 2 - (self.map_x/self.scaler) / 2
            self.y_offset = 0
        elif self.scale == 1:
            self.scaler = self.map_x / (self.screen_x)
            self.x_offset = 0
            if self.y_position == 0:
                temp_y_position = 0
            elif self.y_position == 9:
                temp_y_position = 9
            else:
                temp_y_position = self.y_position
            scaled_map_y = self.map_y / self.scaler
            movable_section = scaled_map_y - self.screen_y
            self.y_offset = -(movable_section / 10) * temp_y_position
        elif self.scale == 2:
            self.scaler = self.map_x / (self.screen_x * 1.5)

            scaled_map_x = self.map_x / self.scaler
            movable_section = scaled_map_x - self.screen_x
            self.x_offset = -movable_section / 6 * self.x_position

            scaled_map_y = self.map_y / self.scaler
            movable_section = scaled_map_y - self.screen_y
            self.y_offset = -movable_section / 10 * self.y_position

    def scale_up(self):
        if self.scale != 2:
            self.scale += 1
            self.recalculate()

    def scale_down(self):
        if self.scale != 0:
            self.scale -= 1
            self.recalculate()

    def x_up(self):
        if self.scale == 0 or self.scale == 1:
            return
        else:
            if self.x_position != 6:
                self.x_position += 1
        self.recalculate()

    def x_down(self):
        if self.scale == 0 or self.scale == 1:
            return
        else:
            if self.x_position != 0:
                self.x_position -= 1
        self.recalculate()

    def y_up(self):
        if self.scale == 0:
            return
        elif self.scale == 1:
            self.x_position = 3
            # if self.y_position == 0:
            #     self.y_position = 1
            # elif self.y_position == 9:
            #     self.y_position = 8

            if self.y_position != 10:
                self.y_position += 1
        elif self.scale == 2:
            if self.y_position != 10:
                self.y_position += 1
        self.recalculate()

    def y_down(self):
        if self.scale == 0:
            return
        elif self.scale == 1:
            self.x_position = 3
            # if self.y_position == 0:
            #     self.y_position = 1
            # elif self.y_position == 9:
            #     self.y_position = 8

            if self.y_position != 0:
                self.y_position -= 1
        elif self.scale == 2:
            if self.y_position != 0:
                self.y_position -= 1
        self.recalculate()
