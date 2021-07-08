import sys
import numpy as np
import pygame

from VisualMath import Screen, Window
import moviemaker


x = np.linspace(0, np.pi * 6, 600)

y1 = np.sin(x)
y2 = np.sin(x) + np.sin(np.pi * x) / 2

r1x = np.zeros(len(x))
r1y = np.zeros(len(x))

r2x = np.zeros(len(x))
r2y = np.zeros(len(x))

screen = Screen()

first = Window(screen.screen, screen.s_w - 40, 100, (screen.s_w / 2, 100))
second = Window(screen.screen, screen.s_w - 40, 100, (screen.s_w / 2, 250))
third = Window(screen.screen, 440, 320, (screen.s_w / 4, 520))
fourth = Window(screen.screen, 440, 320, (3 * screen.s_w / 4, 520))

rotation_frequency = 0.001
rf = "{:.3f}".format(rotation_frequency)

scene = moviemaker.FrameHandler(screen.screen)
mm = moviemaker.MovieMaker(scene.frame_sequence, 'wrapping_wave_function')

j = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            mm.make_movie()
            pygame.time.delay(5)
            mm.del_img_seq()
            sys.exit()

    screen.set_back()

    first.draw_grid(c=(3, 148, 146), lw=1)
    second.draw_grid(c=(3, 148, 146), lw=1)
    third.draw_grid()
    fourth.draw_grid()

    first.draw_axis(c=(255, 214, 214), lw=2)
    second.draw_axis(c=(255, 214, 214), lw=2)
    third.draw_axis(lw=2)
    fourth.draw_axis(lw=2)

    first.draw(x, y1, lw=1)
    first.mention_grid_scale(bg=(252, 225, 225), test_color=(13, 11, 11))
    second.draw(x, y2, lw=1)
    second.mention_grid_scale(bg=(252, 225, 225), test_color=(13, 11, 11))

    screen.display_text(f'rotation_frequency = {rf}', (screen.s_w / 2, 340))

    third.adjust_wscale_to((150, 150))
    for e in range(len(x)):
        r1x[e] = y1[e] * np.cos(rotation_frequency * x[e])
        r1y[e] = y1[e] * np.sin(rotation_frequency * x[e])
    third.draw(r1x, r1y, c=(92, 94, 12), x_scaled=False, y_scaled=False)

    fourth.adjust_wscale_to((100, 100))
    for e in range(len(x)):
        r2x[e] = y2[e] * np.cos(rotation_frequency * x[e])
        r2y[e] = y2[e] * np.sin(rotation_frequency * x[e])
    fourth.draw(r2x, r2y, c=(92, 94, 12), x_scaled=False, y_scaled=False)

    pygame.display.update()

    scene.save_frame()

    rotation_frequency += 0.001
    rf = "{:.3f}".format(rotation_frequency)

    if j == 9999:
        pygame.quit()
        mm.make_movie()
        pygame.time.delay(5)
        mm.del_img_seq()
        sys.exit()

    j += 1
