"""
Set of functions that convert Cartesian (x, y) coordinates to and from pixel coordinates (x_p, y_p) on screen. The
arguments x, y, xmin/xmax, and ymin/ymax are Cartesian values. xp, yp, fig_width, and fig_height are in pixel units.
The pixel coordinate system is as follows: the bottom-left corner is the origin (0, 0), and the top-right is the
ordered pair (figure_width, figure_height).

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
    return (x - xmin) * fig_width / (xmax - xmin)


def y_to_pixel(y, fig_height, ymin, ymax):
    return (y - ymin) * fig_height / (ymax - ymin)


def pixel_to_x(xp, fig_width, xmin, xmax):
    return xp * (xmax - xmin) / fig_width + xmin


def pixel_to_y(yp, fig_height, ymin, ymax):
    return yp * (ymax - ymin) / fig_height + ymin
