import pygame
import const


class Territory:
    def __init__(self, screen, name, points, center, owner=-1, pieces=-1, font_loader=None):
        self.screen = screen
        self.name = name
        self.points = points
        self.center = center
        self.owner = owner
        self.pieces = pieces
        self.font_loader = font_loader

        self.selected = True

        x_points = [x[0] for x in points]
        y_points = [x[1] for x in points]
        self.x, self.y = min(x_points), min(y_points)
        self.x_max, self.y_max = max(x_points), max(y_points)
        self.width, self.height = self.x_max - self.x, self.y_max - self.y

        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_rect(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rectangle, 3)

    def draw_lines(self):
        pygame.draw.lines(self.screen, (255, 255, 255), True, self.points, 3)

    def draw(self, scale, x_mod, y_mod):
        points = [(x/scale+x_mod, y/scale+y_mod) for x,y in self.points]
        if self.selected:
            pygame.draw.lines(self.screen, (255, 255, 255), True, points, 3)

        self.draw_armies(scale, x_mod, y_mod)

    def draw_armies(self, scale, x_mod, y_mod):
        font_size = int(250 / scale)
        modifier = int(16/scale)

        center = (int(self.center[0] / scale + x_mod), int(self.center[1] / scale + y_mod))

        pygame.draw.circle(self.screen, const.PLAYER_COLOURS[self.owner], center, int(180 / scale))

        text = self.font_loader.create_text(str(self.pieces), font_size, (255, 255, 255))
        text_x, text_y = text.get_size()
        self.screen.blit(text, ((center[0]-text_x//2), (center[1]-text_y//2+modifier)))

    def select(self):
        self.selected = not self.selected

    def collide(self, point, scale, x_mod, y_mod):
        self.rectangle = pygame.Rect(self.x/scale+x_mod, self.y/scale+y_mod, self.width/scale, self.height/scale)
        if self.collide_rect(point):
            # print('Square: {}'.format(self.name))
            if self.collide_points(point, scale, x_mod, y_mod):
                # print('Lines: {}'.format(self.name))
                return True
        return False

    def collide_rect(self, point):
        return self.rectangle.collidepoint(point[0], point[1]) == 1

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])
        return A, B, -C

    def intersection(self, a, b, c, d):
        #print(a, b, c, d)
        L1 = self.line(a, b)
        L2 = self.line(c, d)

        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            if ((a[0]-3 <= x <= b[0]+3) or (a[0]+3 >= x >= b[0]-3)) and \
                    ((a[1]-3 <= y <= b[1]+3) or (a[1]+3 >= y >= b[1]-3)) and \
                    ((c[0]-3 <= x <= d[0]+3) or (c[0]+3 >= x >= d[0]-3)) and \
                    ((c[1]-3 <= y <= d[1]+3) or (c[1]+3 >= y >= d[1]-3)):
                return x, y
            else:
                return False
        else:
            return False

    def collide_points(self, point, scale, x_mod, y_mod):
        # print(point, scale, x_mod, y_mod)

        point = ((point[0]-x_mod)*scale, (point[1]-y_mod)*scale)

        # main_line
        x1, y1, x2, y2 = point[0], point[1], self.x_max+1, point[1]

        #print(x1, y1, x2, y2)
        intersections_count = 0
        intersections = []
        for a, b in zip(self.points, self.points[-1:] + self.points[:-1]):
            intersection_point = self.intersection((x1, y1),(x2, y2), (a[0], a[1]),(b[0], b[1]))
            if intersection_point:
                intersections_count += 1
                intersections.append([(round(intersection_point[0]/5), round(intersection_point[1]/5)),
                                      (round(a[0]/5), round(a[1]/5)), (round(b[0]/5), round(b[1]/5))])

        # Determine intersect on point edge case
        ignore = [] # There may be more than one
        while True:
            found_point = False
            active_point = None
            resolved_edge_case = False

            for intersection_point, p1, p2 in intersections:
                if found_point and intersection_point == active_point:
                    if p1 == intersection_point:
                        other_point2 = p2
                    else:
                        other_point2 = p1

                    resolved_edge_case = True
                    ignore.append(intersection_point)

                    if other_point[1] > intersection_point[1] and other_point2[1] < intersection_point[1]:
                        intersections_count -= 1
                    elif other_point[1] < intersection_point[1] and other_point2[1] > intersection_point[1]:
                        intersections_count -= 1
                    break

                if not found_point and intersection_point not in ignore and (self.matching_point(p1, intersection_point) or self.matching_point(p2, intersection_point)):
                    active_point = intersection_point
                    found_point = True
                    if p1 == intersection_point:
                        other_point = p2
                    else:
                        other_point = p1

            if not resolved_edge_case:
                break

        return (intersections_count % 2) == 1

    def matching_point(self, p1, p2):
        if p1[0]+2 >= p2[0] >= p1[0]-2 and \
                p1[1] + 2 >= p2[1] >= p1[1] - 2:
            return True
        return False

if __name__ == '__main__':
    # These test cases test the edge case for end of line intersections
    # no_points = [(12, 15), (15, 10), (17, 15)]
    # yes_points = [(5, 10), (12, 15), (15, 10), (12, 5)]
    # square_points = [(5,5), (15,5), (15,15), (5,15)]
    # click = ((10,10))
    #
    # territory = GuiTerritory('screen', 'skagos', no_points)
    # print(False, territory.collide_points((click)))
    #
    # territory = GuiTerritory('screen', 'skagos', yes_points)
    # print(True, territory.collide_points((click)))
    #
    # territory = GuiTerritory('screen', 'skagos', square_points)
    # print(True, territory.collide_points((click)))


    from territory_coords import skagos
    territory = GuiTerritory('screen', 'scags', skagos)
    #print(territory.collide_points((700, 56), 16.533333333333335, 237.58064516129036, 0))
    #print(territory.collide_points((697, 58), 16.533333333333335, 237.58064516129036, 0))
    print(territory.collide_points((952, 36), 4.62962962962963, - 720.0, - 231.408))



    a, b = (7645.333333333333, 925.8666666666668), (7954.703703703704, 925.8666666666668)
    c, d = (7837.9629629629635, 861.1111111111111), (7847.222222222223, 958.3333333333334)

    territory.intersection(a, b, d, c)
