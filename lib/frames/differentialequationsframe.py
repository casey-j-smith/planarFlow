"""
DifferentialEquationsFrame class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from tkinter import ttk, messagebox
import sympy as sp


class DifferentialEquationsFrame(ttk.Frame):
    def __init__(self, top):
        super().__init__()

        self.dxdt = None
        self.dydt = None
        self.tmax = None
        self.dt = None

        self.error_messages = []
        self.is_configured = False

        for i in range(5):
            self.columnconfigure(i, weight=1)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        # dx/dt
        dxdt_label = ttk.Label(self, text="dx/dt = ", font=top.widget_font)
        dxdt_label.grid(row=0, column=0, sticky="e")
        dxdt_entry = ttk.Entry(self, width=top.large_entry_width, font=top.widget_font)
        dxdt_entry.grid(row=0, column=1, columnspan=3)

        # dy/dt
        dydt_label = ttk.Label(self, text="dy/dt = ", font=top.widget_font)
        dydt_label.grid(row=1, column=0, sticky="e")
        dydt_entry = ttk.Entry(self, width=top.large_entry_width, font=top.widget_font)
        dydt_entry.grid(row=1, column=1, columnspan=3)

        # tmax
        tmax_label = ttk.Label(self, text="tmax = ", font=top.widget_font)
        tmax_label.grid(row=2, column=0, sticky="e")
        tmax_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        tmax_entry.grid(row=2, column=1, sticky="w")

        # dt
        dt_label = ttk.Label(self, text="\u0394t = ", font=top.widget_font)
        dt_label.grid(row=2, column=2, sticky="e")
        dt_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        dt_entry.grid(row=2, column=3, sticky="w")

        # Function definition for set equations button click. Error handling for the inputs to dx/dt, dy/dt, tmin,
        # tmax, and dt will be done here.
        def set_equations():
            self.error_messages = []
            self.is_configured = False

            t, x, y = sp.symbols("t x y")

            if dxdt_entry.get().strip():
                try:
                    self.dxdt = sp.lambdify((t, x, y), dxdt_entry.get(), "numpy")
                    self.dxdt(0., 0., 0.)  # test with values set to zero to catch errors
                except ZeroDivisionError:
                    pass
                except (TypeError, NameError, SyntaxError, ValueError):
                    self.error_messages.append("Invalid/missing input for dx/dt.")
            else:
                self.error_messages.append("Invalid/missing input for dx/dt.")

            if dydt_entry.get().strip():
                try:
                    self.dydt = sp.lambdify((t, x, y), dydt_entry.get(), "numpy")
                    self.dydt(0., 0., 0.)
                except ZeroDivisionError:
                    pass
                except(TypeError, NameError, SyntaxError, ValueError):
                    self.error_messages.append("Invalid/missing input for dy/dt.")
            else:
                self.error_messages.append("Invalid/missing input for dy/dt.")

            if tmax_entry.get().strip():
                try:
                    self.tmax = float(sp.N(tmax_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for tmax.")
                else:
                    if self.tmax <= 0:
                        self.error_messages.append("tmax must be positive.")
            else:
                self.error_messages.append("Missing input for tmax.")

            if dt_entry.get().strip():
                try:
                    self.dt = float(sp.N(dt_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for dt.")
                else:
                    if self.dt <= 0:
                        self.error_messages.append("dt must be positive.")
            else:
                self.error_messages.append("Missing input for dt.")

            if (self.tmax is not None) and (self.dt is not None):
                if self.tmax < self.dt:
                    self.error_messages.append("tmax must be greater than or equal to dt.")

            # Displaying error messages if there are any.
            if self.error_messages:
                messagebox.showerror("Error", "\n".join(self.error_messages))
            else:
                # If the equations are valid, then reset everything.
                if top.flows:
                    top.flow_trajectory_collection.lines.clear()
                    top.flow_circle_collection.patches.clear()
                    top.flow_arrowhead_collection.patches.clear()

                for graph in top.graphs:
                    graph.delete_contours()

                top.flows.clear()
                top.graphs.clear()

                top.fig.canvas.draw()
                self.is_configured = True

        # set equations button
        set_differential_equations_button = ttk.Button(self, width=top.small_button_width, style="Accent.TButton",
                                                       text="Set", command=set_equations)
        set_differential_equations_button.grid(row=2, column=4, sticky="w")
