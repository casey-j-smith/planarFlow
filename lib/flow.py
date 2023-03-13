"""
Flow class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from matplotlib import patches
import numpy as np

from .pixel_conversions import x_to_pixel, pixel_to_x, y_to_pixel, pixel_to_y


class Flow:
    def __init__(self, x0, y0, dxdt, dydt, tmax, dt):
        self.x0 = x0
        self.y0 = y0
        self.dxdt = dxdt
        self.dydt = dydt
        self.tmax = tmax
        self.dt = dt

        self.t_values = None
        self.x_values = None
        self.y_values = None

        self.trajectory = None
        self.circle = None
        self.arrowhead = None

        self.is_equilibrium = (np.abs(self.dxdt(0, self.x0, self.y0)) < 1E-15 and
                               np.abs(self.dydt(0, self.x0, self.y0)) < 1E-15)

    def integrate(self, method, method_dict):
        integrator = method_dict[method]
        self.t_values, self.x_values, self.y_values = integrator(self.dxdt, self.dydt, self.x0, self.y0, self.tmax,
                                                                 self.dt)

    def create_trajectory(self):
        self.trajectory = np.column_stack([self.x_values, self.y_values])  # Will be used in LineCollection

    def create_circle(self, diameter, fig_width, fig_height, xmin, xmax, ymin, ymax):
        x_diameter = pixel_to_x(diameter, fig_width, xmin, xmax)
        y_diameter = pixel_to_y(diameter, fig_height, ymin, ymax)
        self.circle = patches.Ellipse((self.x0, self.y0), width=x_diameter, height=y_diameter)

    def update_circle_radius(self, diameter, fig_width, fig_height, xmin, xmax, ymin, ymax):
        self.circle.width = pixel_to_x(diameter, fig_width, xmin, xmax)
        self.circle.height = pixel_to_y(diameter, fig_height, ymin, ymax)

    # Creating and updating arrowheads will be contingent on whether the flow is an equilibrium point or not. If the
    # flow is not equilibrium, then a triangle will be formed and drawn and will be modified as the axes limits are
    # changed. Otherwise, a copy of the flows circle will take its place. The number of artists in each collection needs
    # to be the same for the highlighting function to work.
    def create_arrowhead(self, arrowhead_size, fig_width, fig_height, xmin, xmax, ymin, ymax):
        if self.is_equilibrium:
            self.arrowhead = self.circle
        else:
            self.arrowhead = patches.Polygon(self.get_arrowhead_points(arrowhead_size, fig_width, fig_height,
                                                                       xmin, xmax, ymin, ymax))

    def get_arrowhead_points(self, arrowhead_size, fig_width, fig_height, xmin, xmax, ymin, ymax):
        # Tangent vector at end of flow (determines direction of the arrow).
        tan = np.array([self.dxdt(self.t_values[-1], self.x_values[-1], self.y_values[-1]),
                        self.dydt(self.t_values[-1], self.x_values[-1], self.y_values[-1])])

        # Convergent tangent vector components to pixel units (to get direction relative to display).
        tan[0] = x_to_pixel(tan[0], fig_width, xmin, xmax)
        tan[1] = y_to_pixel(tan[1], fig_height, ymin, ymax)

        # Normalizing.
        u = tan / np.linalg.norm(tan)

        # Setting x-/y-pixel coordinates of vertices of the triangle.
        x_coords_p = np.array([x_to_pixel(self.x_values[-1], fig_width, xmin, xmax) + arrowhead_size * (-u[0] - u[1]),
                               x_to_pixel(self.x_values[-1], fig_width, xmin, xmax) + arrowhead_size * (-u[0] + u[1]),
                               x_to_pixel(self.x_values[-1], fig_width, xmin, xmax) + arrowhead_size * u[0]])

        y_coords_p = np.array([y_to_pixel(self.y_values[-1], fig_height, ymin, ymax) + arrowhead_size * (u[0] - u[1]),
                               y_to_pixel(self.y_values[-1], fig_height, ymin, ymax) + arrowhead_size * (-u[0] - u[1]),
                               y_to_pixel(self.y_values[-1], fig_height, ymin, ymax) + arrowhead_size * u[1]])

        # Converting back from pixel units.
        x_coords = pixel_to_x(x_coords_p, fig_width, xmin, xmax)
        y_coords = pixel_to_y(y_coords_p, fig_height, ymin, ymax)

        return np.column_stack((x_coords, y_coords))

    def update_arrowhead_points(self, arrowhead_size, fig_width, fig_height, xmin, xmax, ymin, ymax):
        if not self.is_equilibrium:
            self.arrowhead.set(xy=self.get_arrowhead_points(arrowhead_size, fig_width, fig_height, xmin, xmax, ymin,
                                                            ymax))
