"""
The Hodgepodge Machine
"""

import colorsys

import numpy as np
import pygame as pg
import pygame.locals as lcls

from pygame import surfarray as sf

import grid

SIZE = 300
ZOOM = 1000 // SIZE
HILL = 50


SICK_LEVELS = 100
MAX_INITIAL_SICK = 2
COLORS = {lvl: 255 * np.array(colorsys.hsv_to_rgb(lvl / (SICK_LEVELS + 2),
                                                  1., 1.))
          for lvl in range(1, SICK_LEVELS + 1)}

K1 = 2.
K2 = 3.
RATE = 20
LAMBDA = 1.


def _update(sick, infected, colors):
    """
    sick are sick cells
    infected are infected cells
    """
    infected_sum = grid.sum_8(infected)
    sick_near = grid.sum_8(sick)

    # Infected cells progress towards sickness
    infected_near = grid.nonzero_8(infected)
    infected_near[infected_near == 0] = 1  # avoid dvision by zero
    infected += (infected > 0) * \
        (RATE + np.floor(LAMBDA * infected_sum / infected_near))

    # Healthy cells may become infected
    healthy = (infected == 0) & (sick == 0)
    infected += healthy * np.floor(infected_near / K1 + sick_near / K2)

    # ...and some become sick (old sick are healthy now)
    sick[:] = (infected > SICK_LEVELS) * 1.0
    infected[infected > SICK_LEVELS] = 0.0

    grid.color_with(infected, colors, (255., 255., 255.), COLORS)

    colors[sick > 0] = (0., 0., 0.)


def main(size, hill, zoom, max_initial_sick):
    """Entry point."""
    # pylint:disable=no-member
    pg.init()

    infected = np.floor(np.random.rand(size, size) * max_initial_sick)
    hsize = size // 2
    hhill = hill // 2
    hmin = hsize - hhill
    hmax = hsize + hhill
    infected[:hmin, :] = 0
    infected[hmax:, :] = 0
    infected[:, :hmin] = 0
    infected[:, hmax:] = 0

    sick = np.zeros_like(infected)
    colors = np.zeros((size, size, 3), dtype=float)

    screen = pg.display.set_mode((size * zoom, size * zoom), 0, 24)
    # pylint:disable=too-many-function-args
    surface = pg.Surface((size, size))
    while True:
        evt = pg.event.poll()
        if evt.type == lcls.QUIT:
            pg.image.save(screen, "out.png")
            raise SystemExit()
        _update(sick, infected, colors)

        sf.blit_array(surface, colors)
        pg.transform.smoothscale(surface, (size * zoom, size * zoom), screen)
        pg.display.flip()


if __name__ == '__main__':
    main(SIZE, HILL, ZOOM, MAX_INITIAL_SICK)
