"""
FigureSettingsFrame class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from tkinter import ttk, IntVar, CENTER, messagebox
import sympy as sp

from ..configureplot import set_figure_axes, set_figure_ticks, set_figure_ticklabels, set_figure_grid


class FigureSettingsFrame(ttk.Frame):
    def __init__(self, top):
        super().__init__()

        # Setting default settings of the figure.
        self.xmin = -1
        self.xmax = 1
        self.xtick_spacing = 0.25
        self.show_x_ticklabels = IntVar(value=1)

        self.ymin = -1
        self.ymax = 1
        self.ytick_spacing = 0.25
        self.show_y_ticklabels = IntVar(value=1)

        self.show_grid = IntVar(value=1)

        self.error_messages = []
        self.is_configured = True

        for i in range(4):
            self.columnconfigure(i, weight=1)

        for i in range(5):
            self.rowconfigure(i, weight=1)

        # title
        figure_settings_frame_title = ttk.Label(self, text="Plot Configuration", font=top.title_font)
        figure_settings_frame_title.configure(anchor=CENTER)
        figure_settings_frame_title.grid(row=0, column=0, columnspan=4)

        # xmin
        xmin_label = ttk.Label(self, text="xmin = ", font=top.widget_font)
        xmin_label.grid(row=1, column=0, sticky="e")
        xmin_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        xmin_entry.grid(row=1, column=1, sticky="w")
        xmin_entry.insert(0, str(self.xmin))

        # xmax
        xmax_label = ttk.Label(self, text="xmax = ", font=top.widget_font)
        xmax_label.grid(row=1, column=2, sticky="e")
        xmax_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        xmax_entry.grid(row=1, column=3, sticky="w")
        xmax_entry.insert(0, str(self.xmax))

        # x-tick spacing
        xtick_spacing_label = ttk.Label(self, text="\u0394x = ", font=top.widget_font)
        xtick_spacing_label.grid(row=2, column=0, sticky="e")
        xtick_spacing_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        xtick_spacing_entry.grid(row=2, column=1, stick="w")
        xtick_spacing_entry.insert(0, str(self.xtick_spacing))

        # label x-axis
        show_xlabels_checkbutton = ttk.Checkbutton(self, variable=self.show_x_ticklabels, onvalue=True,
                                                   text="Label x-ticks")
        show_xlabels_checkbutton.grid(row=2, column=2, columnspan=2)

        # ymin
        ymin_label = ttk.Label(self, text="ymin = ", font=top.widget_font)
        ymin_label.grid(row=3, column=0, sticky="e")
        ymin_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        ymin_entry.grid(row=3, column=1, sticky="w")
        ymin_entry.insert(0, str(self.ymin))

        # ymax
        ymax_label = ttk.Label(self, text="ymax = ", font=top.widget_font)
        ymax_label.grid(row=3, column=2, sticky="e")
        ymax_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        ymax_entry.grid(row=3, column=3, sticky="w")
        ymax_entry.insert(0, str(self.ymax))

        # y-tick spacing
        ytick_spacing_label = ttk.Label(self, text="\u0394y = ", font=top.widget_font)
        ytick_spacing_label.grid(row=4, column=0, sticky="e")
        ytick_spacing_entry = ttk.Entry(self, width=top.small_entry_width, font=top.widget_font)
        ytick_spacing_entry.grid(row=4, column=1, sticky="w")
        ytick_spacing_entry.insert(0, str(self.ytick_spacing))

        # label y-axis
        show_ylabels_checkbutton = ttk.Checkbutton(self, variable=self.show_y_ticklabels, onvalue=True,
                                                   text="Label y-ticks")
        show_ylabels_checkbutton.grid(row=4, column=2, columnspan=2)

        # show grid
        show_grid_checkbutton = ttk.Checkbutton(self, variable=self.show_grid, onvalue=True, text="show grid")
        show_grid_checkbutton.grid(row=5, column=0, columnspan=2)

        # Function definition for configuring plot.
        def configure_plot():
            self.error_messages = []
            self.is_configured = False

            # Checking for errors in xmix/xmax/ymin/ymax.
            if xmin_entry.get().strip():
                try:
                    self.xmin = float(sp.N(xmin_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for xmin.")
            else:
                self.xmin = None

            if xmax_entry.get().strip():
                try:
                    self.xmax = float(sp.N(xmax_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for xmax.")
            else:
                self.xmax = None

            if (self.xmin is not None) and (self.xmax is not None):
                if self.xmin >= self.xmax:
                    self.error_messages.append("xmin must be less than xmax.")

            if ymin_entry.get().strip():
                try:
                    self.ymin = float(sp.N(ymin_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for ymin.")
            else:
                self.ymin = None

            if ymax_entry.get().strip():
                try:
                    self.ymax = float(sp.N(ymax_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for ymax.")
            else:
                self.ymax = None

            if (self.ymin is not None) and (self.ymax is not None):
                if self.ymin >= self.ymax:
                    self.error_messages.append("ymin must be less than ymax.")

            # Checking to see if there are enough input arguments for xmin/xmax/ymin/ymax.
            if [self.xmin, self.xmax, self.ymin, self.ymax].count(None) >= 3:
                self.error_messages.append("Not enough arguments for xmin/xmax/ymin/ymax.")
            elif [self.xmin, self.xmax, self.ymin, self.ymax].count(None) == 2:
                if (self.xmin is None) or (self.xmax is None):
                    if (self.ymin is None) or (self.ymax is None):
                        self.error_messages.append("Not enough arguments for xmin/xmax/ymin/ymax.")

            # Checking for errors in xtick/ytick_spacing.
            if xtick_spacing_entry.get().strip():
                try:
                    self.xtick_spacing = float(sp.N(xtick_spacing_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid input for x-tick spacing.")
                else:
                    if self.xtick_spacing < 0:
                        self.error_messages.append("x-tick spacing must be positive.")
            else:
                self.xtick_spacing = 0

            if ytick_spacing_entry.get().strip():
                try:
                    self.ytick_spacing = float(sp.N(ytick_spacing_entry.get()))
                except (TypeError, ValueError):
                    self.error_messages.append("Invalid  input for y-tick spacing.")
                else:
                    if self.ytick_spacing < 0:
                        self.error_messages.append("y-tick spacing must be positive.")
            else:
                self.ytick_spacing = 0

            # Proceed with configuring the plot if there are no error messages. If there are errors, display them.
            if self.error_messages:
                messagebox.showerror("Error", "\n".join(self.error_messages))
            else:
                # If we have to calculate xmin/xmax or ymin/ymax to maintain equal axes scales.
                if [self.xmin, self.xmax, self.ymin, self.ymax].count(None) > 0:
                    if (self.xmin is not None) and (self.xmax is not None):
                        pixels_per_unit = top.figure_width / (self.xmax - self.xmin)
                        if (self.ymin is None) and (self.ymax is None):
                            self.ymax = top.figure_height / (2 * pixels_per_unit)
                            self.ymin = -self.ymax
                        elif self.ymin is None:
                            self.ymin = self.ymax - top.figure_height / pixels_per_unit
                        else:
                            self.ymax = self.ymin + top.figure_height / pixels_per_unit

                    if (self.ymin is not None) and (self.ymax is not None):
                        pixels_per_unit = top.figure_height / (self.ymax - self.ymin)
                        if (self.xmin is None) and (self.xmax is None):
                            self.xmax = top.figure_width / (2 * pixels_per_unit)
                            self.xmin = -self.xmax
                        elif self.xmin is None:
                            self.xmin = self.xmax - top.figure_width / pixels_per_unit
                        else:
                            self.xmax = self.xmin + top.figure_width / pixels_per_unit

                set_figure_axes(top.fig, top.ax, self.xmin, self.xmax, self.ymin, self.ymax,
                                top.figure_axes_color)

                set_figure_ticks(top.fig, top.ax, self.xtick_spacing, self.xmin, self.xmax,
                                 self.ytick_spacing, self.ymin, self.ymax)

                set_figure_ticklabels(top.fig, top.ax, self.show_x_ticklabels.get(), self.xmin,
                                      self.xmax, self.show_y_ticklabels.get(), self.ymin, self.ymax)

                set_figure_grid(top.fig, top.ax, self.show_grid.get(), self.xtick_spacing,
                                self.ytick_spacing)

                # If there are already trajectories plotted, update the circle and arrowhead for each flow so the
                # appearance is maintained.
                for flow in top.flows:
                    flow.update_circle_radius(top.flow_circle_diameter, top.figure_width, top.figure_height,
                                              self.xmin, self.xmax, self.ymin, self.ymax)
                    flow.update_arrowhead_points(top.flow_arrowhead_size, top.figure_width, top.figure_height,
                                                 self.xmin, self.xmax, self.ymin, self.ymax)

                # If there are already graphs plotted, update the X-/Y-meshgrids and the contours plotted.
                for graph in top.graphs:
                    graph.update_contours(top.fig, top.ax, self.xmin, self.xmax, self.ymin, self.ymax)

                top.fig.canvas.draw()
                self.is_configured = True

        # configure plot
        configure_plot_button = ttk.Button(self, style="Accent.TButton", width=top.large_button_width,
                                           text="Configure Plot", command=configure_plot)
        configure_plot_button.grid(row=5, column=2, columnspan=2)
