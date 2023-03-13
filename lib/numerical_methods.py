"""
Module that contains the different numerical methods that can be used to integrate flow trajectories. Feel free to add
other methods below, so long as the input arguments and the order of return variables are the same.

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


def RK2(dxdt, dydt, x0, y0, tmax, dt):
    t = np.arange(0., tmax + dt, dt)
    x = np.zeros(len(t))
    y = np.zeros(len(t))

    t[0] = 0.
    x[0] = x0
    y[0] = y0

    for k in range(len(t) - 1):
        k1_x = dt * dxdt(t[k], x[k], y[k])
        k1_y = dt * dydt(t[k], x[k], y[k])

        k2_x = dt * dxdt(t[k] + dt, x[k] + k1_x, y[k] + k1_y)
        k2_y = dt * dydt(t[k] + dt, x[k] + k1_x, y[k] + k1_y)

        x[k + 1] = x[k] + (k1_x + k2_x) / 2
        y[k + 1] = y[k] + (k1_y + k2_y) / 2

    return t, x, y


def RK4(dxdt, dydt, x0, y0, tmax, dt):
    t = np.arange(0., tmax + dt, dt)
    x = np.zeros(len(t))
    y = np.zeros(len(t))

    t[0] = 0.
    x[0] = x0
    y[0] = y0

    for k in range(len(t) - 1):
        k1_x = dt * dxdt(t[k], x[k], y[k])
        k1_y = dt * dydt(t[k], x[k], y[k])

        k2_x = dt * dxdt(t[k] + dt / 2, x[k] + k1_x / 2, y[k] + k1_y / 2)
        k2_y = dt * dydt(t[k] + dt / 2, x[k] + k1_x / 2, y[k] + k1_y / 2)

        k3_x = dt * dxdt(t[k] + dt / 2, x[k] + k2_x / 2, y[k] + k2_y / 2)
        k3_y = dt * dydt(t[k] + dt / 2, x[k] + k2_x / 2, y[k] + k2_y / 2)

        k4_x = dt * dxdt(t[k] + dt, x[k] + k3_x, y[k] + k3_y)
        k4_y = dt * dydt(t[k] + dt, x[k] + k3_x, y[k] + k3_y)

        x[k + 1] = x[k] + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y[k + 1] = y[k] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

    return t, x, y


def Euler(dxdt, dydt, x0, y0, tmax, dt):
    t = np.arange(0., tmax + dt, dt)
    x = np.zeros(len(t))
    y = np.zeros(len(t))

    t[0] = 0.
    x[0] = x0
    y[0] = y0

    for k in range(len(t) - 1):
        x[k + 1] = x[k] + dt * dxdt(t[k], x[k], y[k])
        y[k + 1] = y[k] + dt * dydt(t[k], x[k], y[k])

    return t, x, y
