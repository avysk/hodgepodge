"""
The Hodgepodge Machine
"""

import argparse
import colorsys
import sys

import numpy as np
import pygame as pg
import pygame.locals as lcls

from pygame import surfarray as sf

import grid


# pylint:disable=invalid-name
def _update(opt, sick, infected):
    """
    Update sick and infected cells.
    """
    infected_sum = grid.sum_8(infected)
    sick_near = grid.sum_8(sick)

    # Infected cells progress towards sickness
    infected_near = grid.nonzero_8(infected)
    infected_near[infected_near == 0] = 1  # avoid dvision by zero
    infected += (infected > 0) * \
        (opt.rate + np.floor(opt.multiplier * infected_sum / infected_near))

    # Healthy cells may become infected
    healthy = (infected == 0) & (sick == 0)
    infected += healthy * np.floor(infected_near / opt.kfirst +
                                   sick_near / opt.ksecond)

    # ...and some become sick (old sick are healthy now)
    sick[:] = (infected > opt.levels) * 1.0
    infected[infected > opt.levels] = 0.0


def _palette(num_levels):
    return {lvl:
            255 * np.array(colorsys.hsv_to_rgb(lvl / (num_levels + 2), 1., 1.))
            for lvl in range(1, num_levels + 1)}


def main(opt):
    """Entry point."""

    # pylint:disable=no-member
    pg.init()

    size = opt.size
    zoom = opt.window // opt.size
    screen = pg.display.set_mode((size * zoom, size * zoom), 0, 24)
    # pylint:disable=too-many-function-args
    surface = pg.Surface((size, size))

    maxlevel = min(opt.levels, opt.maxlevel)
    infected = np.floor(np.random.rand(size, size) * maxlevel)
    hsize = size // 2
    hhill = opt.hill // 2
    hmin = hsize - hhill
    hmax = hsize + hhill
    infected[:hmin, :] = 0
    infected[hmax:, :] = 0
    infected[:, :hmin] = 0
    infected[:, hmax:] = 0

    sick = np.zeros_like(infected)
    colors = np.zeros((size, size, 3), dtype=float)
    palette = _palette(options.levels)

    while True:
        evt = pg.event.poll()
        if evt.type == lcls.QUIT:
            if opt.saveto:
                pg.image.save(screen, opt.saveto)
            raise SystemExit()
        _update(options, sick, infected)
        grid.color_with(infected, colors, (255., 255., 255.), palette)
        colors[sick > 0] = (0., 0., 0.)

        sf.blit_array(surface, colors)
        pg.transform.smoothscale(surface, (size * zoom, size * zoom), screen)
        pg.display.flip()


def _parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="size of the grid [300]",
                        type=int, default=300)
    parser.add_argument("-w", "--window",
                        help="window size limit [1000]",
                        type=int, default=1000)
    parser.add_argument("--hill",
                        help="size of initial square to seed randomly [30]",
                        type=int, default=30)
    parser.add_argument("-l", "--levels",
                        help="the number of possible infection levels [100]",
                        type=int, default=100)
    parser.add_argument("-m", "--maxlevel",
                        help="the maximum infection level of "
                             "initial random seed [20]",
                        type=int, default=20)
    parser.add_argument("--kfirst", help="Hodgepodge K1 [2]",
                        type=int, default=2)
    parser.add_argument("--ksecond", help="Hodgepodge K2 [3]",
                        type=int, default=3)
    parser.add_argument("-r", "--rate",
                        help="Rate of constant infection growth [20]",
                        type=int, default=20)
    parser.add_argument("--multiplier",
                        help="Multiplier for contribution to infection "
                             "growth of neighbour cells [1.0]",
                        type=float, default=1.0)
    parser.add_argument("--saveto",
                        help="Name of the file to save picture at exit",
                        type=str)

    return parser.parse_args(args=args)


if __name__ == '__main__':
    options = _parse(sys.argv[1:])
    main(options)
