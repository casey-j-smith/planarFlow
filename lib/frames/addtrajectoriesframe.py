"""
AddTrajectoriesFrame class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from tkinter import ttk, CENTER, messagebox
import numpy as np
import sympy as sp

from ..flow import Flow


class AddTrajectoriesFrame(ttk.Frame):
    def __init__(self, top):
        super().__init__()

        self.error_messages = []

        for i in range(4):
            self.columnconfigure(i, weight=1)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        # title
        add_trajectories_frame_title = ttk.Label(self, text="Add Trajectories", font=top.title_font)
        add_trajectories_frame_title.configure(anchor=CENTER)
        add_trajectories_frame_title.grid(row=0, column=0, columnspan=4)

        # x0
        x0_label = ttk.Label(self, text="x0 = ", font=top.widget_font)
        x0_label.grid(row=1, column=0, sticky="e")
        x0_entry = ttk.Entry(self, width=top.large_entry_width, font=top.widget_font)
        x0_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        # y0
        y0_label = ttk.Label(self, text="y0 = ", font=top.widget_font)
        y0_label.grid(row=2, column=0, sticky="e")
        y0_entry = ttk.Entry(self, width=top.large_entry_width, font=top.widget_font)
        y0_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        # function definition for add trajectory button.
        def add_trajectories():
            self.error_messages = []

            x0 = None
            y0 = None

            if top.differential_equations.is_configured and top.figure_settings.is_configured:
                # Checking if there is the correct number of arguments that are comma separated. If "rand" is entered,
                # then a random array of 10 values within the x-/y-domain will be generated. If there is a single
                # value entered for x0 and y0, then only one flow will be created with that initial condition. If either
                # are arrays with three arguments of the form (begin, end, inc) (following numpy arange syntax), then
                # a meshgrid of initial conditions will be used except for the case when both are "rand."
                if x0_entry.get().strip() and y0_entry.get().strip():  # If there is a user input
                    if x0_entry.get().strip() == "rand":
                        x0 = np.random.uniform(top.figure_settings.xmin, top.figure_settings.xmax, 10)
                    else:
                        if len(x0_entry.get().split(",")) == 1:
                            try:
                                x0 = np.array([float(sp.N(x0_entry.get()))])
                            except (TypeError, ValueError):
                                self.error_messages.append("Invalid entry for x0.")
                        elif len(x0_entry.get().split(",")) == 3:
                            try:
                                x_start = float(sp.N(x0_entry.get().split(",")[0]))
                                x_end = float(sp.N(x0_entry.get().split(",")[1]))
                                x_inc = float(sp.N(x0_entry.get().split(",")[2]))
                                x0 = np.arange(x_start, x_end + x_inc, x_inc)
                            except (TypeError, ValueError, ZeroDivisionError):
                                self.error_messages.append("Invalid entry for x0.")
                        else:
                            self.error_messages.append("Incorrect number of inputs for x0. This should be either a  \
                                                        single value, three comma-separated values, or rand.")

                    if y0_entry.get().strip() == "rand":
                        y0 = np.random.uniform(top.figure_settings.ymin, top.figure_settings.ymax, 10)
                    else:
                        if len(y0_entry.get().split(",")) == 1:
                            try:
                                y0 = np.array([float(sp.N(y0_entry.get()))])
                            except (TypeError, ValueError):
                                self.error_messages.append("Invalid entry for y0.")
                        elif len(y0_entry.get().split(",")) == 3:
                            try:
                                y_start = float(sp.N(y0_entry.get().split(",")[0]))
                                y_end = float(sp.N(y0_entry.get().split(",")[1]))
                                y_inc = float(sp.N(y0_entry.get().split(",")[2]))
                                y0 = np.arange(y_start, y_end + y_inc, y_inc)
                            except (TypeError, ValueError, ZeroDivisionError):
                                self.error_messages.append("Invalid entry for y0.")
                        else:
                            self.error_messages.append("Incorrect number of inputs for y0. This should be either a  \
                                                        single value, three comma-separated values, or rand.")

                if (not x0_entry.get().strip()) ^ (not y0_entry.get().strip()):  # If only one entry has values
                    self.error_messages.append("Both x0 and y0 must have valid entries.")

                if self.error_messages:
                    messagebox.showerror("Error", "\n".join(self.error_messages))
                elif not (x0 is None or y0 is None):
                    for x in x0:
                        for y in y0:
                            # If both x0 and y0 entries are rand, then use a new random value for x and y in each
                            # iteration. This avoids a grid-like array of initial conditions, which isn't what the
                            # user is expecting when they want to see the evolution of "random" initial conditions.
                            if x0_entry.get().strip() == "rand" and y0_entry.get().strip() == "rand":
                                x = np.random.uniform(top.figure_settings.xmin, top.figure_settings.xmax)
                                y = np.random.uniform(top.figure_settings.ymin, top.figure_settings.ymax)

                            # Avoid repeated flow calculations and any initial points where the differential equations
                            # are undefined.
                            if not any((np.abs(x - flow.x0) < 1E-15) and (np.abs(y - flow.y0) < 1E-15)
                                       for flow in top.flows):
                                if not (np.isnan(top.differential_equations.dxdt(0, x, y)) or
                                        np.isinf(top.differential_equations.dxdt(0, x, y)) or
                                        np.isnan(top.differential_equations.dydt(0, x, y)) or
                                        np.isinf(top.differential_equations.dydt(0, x, y))):

                                    top.flows.append(Flow(x, y, top.differential_equations.dxdt,
                                                          top.differential_equations.dydt,
                                                          top.differential_equations.tmax,
                                                          top.differential_equations.dt))
                                    top.flows[-1].integrate(top.numerical_method, top.numerical_method_dict)
                                    top.flows[-1].create_trajectory()
                                    top.flows[-1].create_circle(top.flow_circle_diameter, top.figure_width,
                                                                top.figure_height, top.figure_settings.xmin,
                                                                top.figure_settings.xmax, top.figure_settings.ymin,
                                                                top.figure_settings.ymax)
                                    top.flows[-1].create_arrowhead(top.flow_arrowhead_size, top.figure_width,
                                                                   top.figure_height, top.figure_settings.xmin,
                                                                   top.figure_settings.xmax,
                                                                   top.figure_settings.ymin,
                                                                   top.figure_settings.ymax)

                                    top.flow_trajectory_collection.lines.append(top.flows[-1].trajectory)
                                    top.flow_circle_collection.patches.append(top.flows[-1].circle)
                                    top.flow_arrowhead_collection.patches.append(top.flows[-1].arrowhead)

                    top.collection_colors = [top.flow_color] * len(top.flows)
                    top.flow_circle_collection.set_facecolors(top.collection_colors)
                    top.flow_trajectory_collection.set_color(top.collection_colors)
                    top.flow_arrowhead_collection.set_facecolors(top.collection_colors)

                    top.fig.canvas.draw()

        # add trajectories button
        add_trajectories_button = ttk.Button(self, width=top.small_button_width, style="Accent.TButton", text="Add",
                                             command=add_trajectories)
        add_trajectories_button.grid(row=2, column=3, sticky="w")
