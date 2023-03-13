"""
Graph class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
import numpy as np


class Graph:
    def __init__(self, eqn, x_low, x_upp, y_low, y_upp, color, linewidth):
        self.eqn = eqn
        self.x_low = x_low
        self.x_upp = x_upp
        self.y_low = y_low
        self.y_upp = y_upp
        self.color = color
        self.linewidth = linewidth

        self.X = None
        self.Y = None
        self.contours = []

    def create_meshgrid(self, xmin, xmax, ymin, ymax, n=200):
        x_array = np.linspace(np.amax((self.x_low, xmin)), np.amin((self.x_upp, xmax)), n)

        y_array = np.linspace(np.amax((self.y_low, ymin)), np.amin((self.y_upp, ymax)), n)

        self.X, self.Y = np.meshgrid(x_array, y_array)

    def create_contours(self, fig, ax):
        self.contours = ax.contour(self.X, self.Y, self.eqn(self.X, self.Y), [0.], colors=(self.color, ),
                                   linewidths=self.linewidth, zorder=-4)
        fig.canvas.draw()

    def delete_contours(self):
        for collection in self.contours.collections:
            collection.remove()

    def update_linewidth(self, new_linewidth):
        self.linewidth = new_linewidth
        for collection in self.contours.collections:
            collection.set(linewidths=self.linewidth)

    def update_contours(self, fig, ax, xmin, xmax, ymin, ymax):
        self.create_meshgrid(xmin, xmax, ymin, ymax)
        self.delete_contours()
        self.create_contours(fig, ax)
