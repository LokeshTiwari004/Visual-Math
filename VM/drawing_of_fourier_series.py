
# function math draw draw the fourier animation when given list of frequencies and radius
# if no frequency and radius values are given than it draws the standard animation


import pygame

from VisualMath import *

screen = Screen(width=1080, height=720)
screen.initialise()
win1 = Window(screen.screen, screen.s_w, screen.s_h, (screen.s_w/2, screen.s_h/2))
win1.scaling = (1, 1)



def draw_fourier(win, frequency=None, radius=None, angle=None):
    frame = 1002
    f = 0.99
    u = 0
    i = -1
    k = 0

    x = np.array([], dtype='float32')
    y = np.array([], dtype='float32')

    if frequency is None:
        i = 31
        frequency = np.array(list(range(i - 31, i)))
    if radius is None:
        k = 31
        radius = np.array(list(range(k - 31, k)), dtype='float32')

    omega = frequency * (2*np.pi)/1000

    if angle is None:
        angle = np.zeros(len(frequency), dtype='float32')

    junction = np.array([(1.0, 1.0)]*(len(frequency)))
    junction_real_cord = np.array([(1.0, 1.0)]*len(frequency))

    p = 255
    while True:
        screen.reset(save_frame=True, make_movie=True)
        win.draw_grid(c=(10, 50, 75), lw=1)
        win.draw_axis(lw=2, c=(p, p, p))

        if frame > 0:
            angle += omega

            for e in range(len(junction)):
                junction[e] = win.polar_to_cart((radius[e], angle[e]))


            junction_real_cord[0] = junction[0]
            for e in range(1, len(junction_real_cord)):
                junction_real_cord[e] = win.true_cord(junction[e], junction_real_cord[e-1])


            win.draw_circle((0,0), radius[0],lw=1, c=(p, p, p))
            win.c_draw((0,0), junction[0],lw=1, c=(p, p, p))
            for e in range(1, len(radius)):
                win.draw_circle(junction_real_cord[e-1], radius[e],lw=1, c=(p, p, p))
                win.c_draw(junction_real_cord[e-1], junction_real_cord[e],lw=1, c=(p, p, p))


            x = np.append(x, [junction_real_cord[-1][0]])
            y = np.append(y, [junction_real_cord[-1][1]])

            win.draw(x, y, lw=1, c=(30, 200, 200))
            if frame < 255:
                p = frame
            frame -= 1
        else:
            if i == -1:
                if u < 100:
                    win.scaling = win.scaling[0] * f, win.scaling[1] * f
                    f -= 0.01
                    win.draw(x, y, lw=2, c=(30, 200, 200))
                    screen.refresh()
                    u += 1
                else:
                    screen.mm.make_movie()
                    screen.mm.del_img_seq()
                    pygame.quit()
                    sys.exit()
                    return
            else:
                while k != -1:
                    radius = np.array(list(range(k - 31, k)))

                    if k % 2:
                        i = 0
                        t = 0
                    else:
                        i = 31
                        t = 31

                    while 32 > i > -1:
                        screen.reset(save_frame=True)
                        win.draw_grid(c=(10, 50, 75), lw=1)
                        x1 = np.array([], dtype='float32')
                        y1 = np.array([], dtype='float32')

                        frequency = np.array(list(range(i - 31, i)))
                        omega = frequency * (2 * np.pi) / 1000

                        angle = np.zeros(len(omega), dtype='float32')

                        for j in range(1002):
                            angle += omega
                            x1 = np.append(x1, [(radius * np.cos(angle)).sum()])
                            y1 = np.append(y1, [(radius * np.sin(angle)).sum()])

                        win1.draw(x1, y1, lw=2, c=(30, 200, 200))
                        screen.refresh()
                        if k % 2:
                            i += 1
                        else:
                            i -= 1
                    k -= 1

                screen.mm.make_movie()
                pygame.time.delay(100)
                screen.mm.del_img_seq()
                pygame.quit()
                sys.exit()
        screen.refresh()



draw_fourier(win1)