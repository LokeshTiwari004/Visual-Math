import sys

import pygame


class Screen:
    def __init__(self, width=1080, height=720):

        pygame.init()
        self.s_w, self.s_h = width, height
        self.screen = pygame.display.set_mode([width, height])

    def set_back(self):
        self.screen.fill((0, 0, 0))


class Window:
    def __init__(self, screen=None, width=None, height=None, center=None, scaling=(20, 20)):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if center is not None:
            self.center = center
        if screen is not None:
            self.screen = screen

        self.scaling = scaling
        self.window_scale = "X: 1U = 20p" + "\n" + "Y: 1U = 20p"
        self.grid_scale = "Grid Scale:\n" + "X: 1U = 20p" + "\n" + "Y: 1U = 20p"

        self.origin = (0, 0)

    def true_coordinate(self, co_ordinate=None, wrt="center"):
        if wrt == "center":
            return self.center[0] + co_ordinate[0], self.center[1] - co_ordinate[1]
        elif wrt == "origin":
            return self.center[0] + self.origin[0] + co_ordinate[0], self.center[1] - self.origin[1] - co_ordinate[1]

    def draw_axis(self, c=(200, 200, 200), lw=1):

        pygame.draw.line(self.screen, c,
                         (self.origin[0] + self.center[0], self.center[1] - self.height/2),
                         (self.origin[0] + self.center[0], self.center[1] + self.height/2), lw)

        pygame.draw.line(self.screen, c,
                         (self.center[0] - self.width / 2, self.center[1] - self.origin[1]),
                         (self.center[0] + self.width / 2, self.center[1] - self.origin[1]), lw)

    def draw_grid(self, c=(11, 72, 99), lw=1):

        x_scale, y_scale = self.scaling

        X = f"X:1U = " + "{:.3f}".format(x_scale) + 'p'
        Y = f"Y:1U = " + "{:.3f}".format(y_scale) + 'p'

        if 20 <= x_scale < 40:
            x = x_scale
        elif x_scale < 20:
            x = 20
            X = f"X: " + "{:.3f}".format(20 / x_scale) + "U = 20p"
        else:
            x = 40
            X = f"X: " + "{:.3f}".format(40 / x_scale) + "U = 40p"

        if 20 <= y_scale < 40:
            y = y_scale
        elif y_scale < 20:
            y = 20
            Y = f"Y: " + "{:.3f}".format(20 / y_scale) + "U = 20p"
        else:
            y = 40
            Y = f"Y: " + "{:.3f}".format(40 / y_scale) + "U = 40p"

        self.grid_scale = "Grid Scale--> " + X + " " + Y


        for i in range(int((self.origin[0] + self.width/2)/x)+1):
            pygame.draw.line(self.screen, c,
                             (self.center[0] + self.origin[0] - x * i, self.center[1] - self.height / 2),
                             (self.center[0] + self.origin[0] - x * i, self.center[1] + self.height / 2), lw)
        for i in range(int((self.width/2-self.origin[0])/x)+1):
            pygame.draw.line(self.screen, c,
                             (self.center[0] + self.origin[0] + x * i, self.center[1] - self.height / 2),
                             (self.center[0] + self.origin[0] + x * i, self.center[1] + self.height / 2), lw)
        for i in range(int((self.origin[1] + self.height/2)/y)+1):
            pygame.draw.line(self.screen, c,
                             (self.center[0] - self.width / 2, self.center[1] - self.origin[1] + y * i),
                             (self.center[0] + self.width / 2, self.center[1] - self.origin[1] + y * i), lw)
        for i in range(int((self.height/2 - self.origin[1])/y)+1):
            pygame.draw.line(self.screen, c,
                             (self.center[0] - self.width / 2, self.center[1] - self.origin[1] - y * i),
                             (self.center[0] + self.width / 2, self.center[1] - self.origin[1] - y * i), lw)

    def adjust_wscale_to(self, new_scale):
        self.scaling = new_scale

    def relocate_win_to(self, co_ordinates):
        self.center = co_ordinates

    def mention_wscale(self): # mentions the window_scale
        x_scale, y_scale = self.scaling

        self.window_scale = "Window Scale--> " + f"X:1U = " + "{:.2f}".format(x_scale) + f"p Y:1U =" + "{:.3f}".format(y_scale)+'p'

        v = pygame.font.SysFont('monospace', 15).render(self.window_scale, False, (255, 10, 10), (0, 0, 0))
        f = v.get_rect()
        x, y = v.get_size()
        f.center = (self.center[0]-int(self.width/2-x/2), self.center[1]-int(self.height/2-y/2))
        self.screen.blit(v, f)

    def mention_grid_scale(self, font_style='monospace', test_color=(0, 199, 126), bg=(0, 0, 0)):
        v = pygame.font.SysFont(font_style, 15).render(self.grid_scale, False, test_color, bg)
        f = v.get_rect()
        x, y = v.get_size()
        f.center = (self.center[0] - int(self.width / 2 - x / 2), self.center[1] - int(self.height / 2 - y / 2) - 20)
        self.screen.blit(v, f)

    def relocate_origin_to(self, x, y):
        x = self.origin[0] + x
        y = self.origin[1] + y

        if abs(x) <= self.width/2:
            self.origin = x, self.origin[1]
        elif self.width/2 < x:
            self.origin = self.width / 2, self.origin[1]
        else:
            self.origin = -self.width / 2, self.origin[1]

        if abs(y) <= self.height/2:
            self.origin = self.origin[0], y
        elif self.height/2 < y:
            self.origin = self.origin[0], self.height / 2
        else:
            self.origin = self.origin[0], -self.height / 2

    def draw(self, x_cords=None, y_cords=None, c=(255, 255, 0), lw=2, x_scaled=True, y_scaled=True):
        if y_scaled:
            self.scaling = self.scaling[0], self.height/(max(y_cords) - min(y_cords))

            self.origin = self.origin[0], -self.height / 2 + self.scaling[1] * (0 - min(y_cords))

        if x_scaled:
            self.scaling = self.width/(max(x_cords) - min(x_cords)), self.scaling[1]

            self.origin = -self.width / 2 + self.scaling[0] * (0 - min(x_cords)), self.origin[1]

        e = self.scaling[0]
        f = self.scaling[1]

        start_point = self.true_coordinate((e * x_cords[0], f * y_cords[0]), wrt="origin")

        for i in range(len(x_cords)-1):
            stop_point = self.true_coordinate((e * x_cords[i + 1], f * y_cords[i + 1]), wrt="origin")
            pygame.draw.line(self.screen, c,
                             start_point, stop_point, lw)
            start_point = stop_point


if __name__=="__main__":
    screen = Screen()
    g = Window(screen.screen, 500, 500, (400, 300))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        g.draw([-1, 0, 1, 2, 3], [-1, 0, 1, 2, 3])
        g.draw_grid()
        g.draw_axis()
        # g.mention_wscale()
        g.mention_grid_scale()
        pygame.display.update()
        screen.set_back()
