"""
The Hodgepodge Machine
"""

import colorsys

import numpy as np
import pygame as pg
import pygame.locals as lcls

from pygame import surfarray as sf

SIZE = 250
ZOOM = 1000 // SIZE


SICK_LEVELS = 100
COLORS = {lvl: 255 * np.array(colorsys.hsv_to_rgb(lvl / (SICK_LEVELS + 2),
                                                  1., 1.))
          for lvl in range(1, SICK_LEVELS + 1)}

K1 = 2.
K2 = 3.
RATE = 10


def _sum(src):
    dst = np.zeros_like(src)
    dst[1:, :] += src[:-1, :]
    dst[:-1, :] += src[1:, :]
    dst[:, 1:] += src[:, :-1]
    dst[:, :-1] += src[:, 1:]
    dst[1:, 1:] += src[:-1, :-1]
    dst[1:, :-1] += src[:-1, 1:]
    dst[:-1, 1:] += src[1:, :-1]
    dst[:-1, :-1] += src[1:, 1:]
    return dst


def _update(sick, infected, colors):
    """
    sick are sick cells
    infected are infected cells
    """
    infected_sum = _sum(infected)
    sick_near = _sum(sick)

    infected_near = _sum((infected != 0) * 1.0)
    # Infected cells progress towards sickness
    infected_near[infected_near == 0] = 1
    infected += (infected > 0) * \
        (RATE + np.floor(infected_sum / infected_near))
    # Healthy cells may become infected
    healthy = (infected == 0) & (sick == 0)
    infected += healthy * np.floor(infected_near / K1 + sick_near / K2)
    # ...and some become sick (old sick are healthy now)
    sick = (infected > SICK_LEVELS) * 1.0
    infected[infected > SICK_LEVELS] = 0.0

    colors.fill(255.)
    for lvl in range(1, SICK_LEVELS + 1):
        colors[infected == lvl] = COLORS[lvl]
    colors[sick > 0] = (0., 0., 0.)


def main(size, zoom):
    """Entry point."""
    # pylint:disable=no-member
    pg.init()

    infected = np.floor(np.random.rand(size, size) * SICK_LEVELS)
    sick = np.zeros_like(infected)
    colors = np.zeros((size, size, 3), dtype=float)

    screen = pg.display.set_mode((size * zoom, size * zoom), 0, 24)
    # pylint:disable=too-many-function-args
    surface = pg.Surface((size, size))
    while True:
        evt = pg.event.poll()
        if evt.type == lcls.QUIT:
            raise SystemExit()
        _update(sick, infected, colors)

        sf.blit_array(surface, colors)
        pg.transform.smoothscale(surface,
                                 (size * zoom, size * zoom), screen)
        pg.display.flip()


if __name__ == '__main__':
    main(SIZE, ZOOM)
