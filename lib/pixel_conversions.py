"""
Set of functions that convert Cartesian (x, y) coordinates to and from pixel coordinates (x_p, y_p) on screen. The
arguments x, y, xmin/xmax, and ymin/ymax are Cartesian values. xp, yp, fig_width, and fig_height are in pixel units.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""


def x_to_pixel(x, fig_width, xmin, xmax):
    return x * fig_width / (xmax - xmin)


def y_to_pixel(y, fig_height, ymin, ymax):
    return y * fig_height / (ymax - ymin)


def pixel_to_x(xp, fig_width, xmin, xmax):
    return (xmax - xmin) * xp / fig_width


def pixel_to_y(yp, fig_height, ymin, ymax):
    return (ymax - ymin) * yp / fig_height
