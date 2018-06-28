"""
Misc utilities for working with square grid.
"""

import numpy as np


def sum_8(src):
    """
    Return numpy array containing the sum of 8-neighbours from the source
    array.
    """
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


def nonzero_8(src):
    """
    Return numpy array containing the number of non-zero 8-neighbours from the
    source array.
    """
    return sum_8((src != 0) * 1.0)


def color_with(src, colors, background, palette):
    """
    Using color palette, fill colors array according to color indices from the
    source array.
    """
    colors[:] = background
    for idx, color in palette.items():
        colors[src == idx] = color
