"""
AddGraphsFrame class file.

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
import sympy as sp
from matplotlib import colors

from ..graph import Graph


class AddGraphsFrame(ttk.Frame):
    def __init__(self, top):
        super().__init__()

        self.error_messages = []

        for i in range(5):
            self.columnconfigure(i, weight=1)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        # title
        add_graphs_frame_title = ttk.Label(self, text="Add Graphs", font=top.title_font)
        add_graphs_frame_title.configure(anchor=CENTER)
        add_graphs_frame_title.grid(row=0, column=0, columnspan=5)

        # equation
        equation_label = ttk.Label(self, text="Equation:", font=top.widget_font)
        equation_label.grid(row=1, column=0, sticky="e")
        equation_entry = ttk.Entry(self, width=top.large_entry_width, font=top.widget_font)
        equation_entry.grid(row=1, column=1, columnspan=3)

        # x domain
        x_domain_label = ttk.Label(self, text="x \u2208 ", font=top.widget_font)
        x_domain_label.grid(row=2, column=0, sticky="e")
        x_domain_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        x_domain_entry.grid(row=2, column=1, sticky="w")

        # y domain
        y_domain_label = ttk.Label(self, text="y \u2208 ", font=top.widget_font)
        y_domain_label.grid(row=2, column=2, sticky="e")
        y_domain_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        y_domain_entry.grid(row=2, column=3, sticky="w")

        # Function definition for plotting equation.
        def plot_equation():
            self.error_messages = []
            eqn = None
            color = top.flow_color  # If no color is further specified, have the graphs match the flow colors.
            x_low = None
            x_upp = None
            y_low = None
            y_upp = None

            # Verifying that the input is a valid explicit or implicit function equation. The equation entry should be
            # either of the form "<equation to graph>" or "<equation to graph>, <color>".
            x, y = sp.symbols("x y")
            equation = equation_entry.get().split(",")

            if len(equation) <= 2:
                if not equation[0].count("=") == 1:
                    self.error_messages.append("Equation must be y = f(x), x = f(y), or f(x, y) = C.")
                else:
                    eqn_string = equation[0].split("=")[0] + "-" + equation[0].split("=")[1]
                    try:
                        eqn = sp.lambdify((x, y), eqn_string, "numpy")
                        eqn(0, 0)
                    except ZeroDivisionError:
                        pass
                    except (NameError, SyntaxError, ValueError):
                        self.error_messages.append("Invalid expression for equation.")

                if len(equation) == 2:
                    if not equation[1].strip() in list(colors.BASE_COLORS.keys()):
                        self.error_messages.append("Invalid color argument.")
                    else:
                        color = equation[1].strip()
            else:
                self.error_messages.append("Invalid expression for equation and/or color argument.")

            # Verifying x domain is valid.
            x_domain = x_domain_entry.get().strip()

            if len(x_domain) == 0:
                x_low = float("-inf")
                x_upp = float("inf")
            elif (x_domain[0] == "(") and (x_domain[-1] == ")") and (x_domain.count(",") == 1):
                try:
                    x_low_input = x_domain[1:-1].split(",")[0].strip()
                    x_upp_input = x_domain[1:-1].split(",")[1].strip()

                    if x_low_input in ("-inf", "inf"):
                        x_low = float(x_low_input)
                    else:
                        x_low = float(sp.N(x_low_input))

                    if x_upp_input in ("-inf", "inf"):
                        x_upp = float(x_upp_input)
                    else:
                        x_upp = float(sp.N(x_upp_input))

                    if x_upp <= x_low:
                        self.error_messages.append("Lower bound for x must be less than its upper bound.")
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid entry for x-domain.")
            else:
                self.error_messages.append("Invalid entry for x-domain.")

            # Verifying y domain is valid.
            y_domain = y_domain_entry.get().strip()

            if len(y_domain) == 0:
                y_low = float("-inf")
                y_upp = float("inf")
            elif (y_domain[0] == "(") and (y_domain[-1] == ")") and (y_domain.count(",") == 1):
                try:
                    y_low_input = y_domain[1:-1].split(",")[0].strip()
                    y_upp_input = y_domain[1:-1].split(",")[1].strip()

                    if y_low_input in ("-inf", "inf"):
                        y_low = float(y_low_input)
                    else:
                        y_low = float(sp.N(y_low_input))

                    if y_upp_input in ("-inf", "inf"):
                        y_upp = float(y_upp_input)
                    else:
                        y_upp = float(sp.N(y_upp_input))

                    if y_upp <= y_low:
                        self.error_messages.append("Lower bound for y must be less than its upper bound.")
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid entry for y-domain.")
            else:
                self.error_messages.append("Invalid entry for y-domain.")

            if self.error_messages:
                messagebox.showerror("Error", "\n".join(self.error_messages))
            else:
                top.graphs.append(Graph(eqn, x_low, x_upp, y_low, y_upp, color, top.graph_linewidth))
                top.graphs[-1].create_meshgrid(top.figure_settings.xmin, top.figure_settings.xmax,
                                               top.figure_settings.ymin, top.figure_settings.ymax)
                top.graphs[-1].create_contours(top.fig, top.ax)

                top.fig.canvas.draw()

        # plot equation button
        plot_equation_button = ttk.Button(self, width=top.small_button_width, style="Accent.TButton", text="Plot",
                                          command=plot_equation)
        plot_equation_button.grid(row=2, column=4, sticky="w")
