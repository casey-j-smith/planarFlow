"""
Main program for the planarFlow app.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
import sys
import os
import platform
import inspect
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.backend_pdf

from lib.configureplot import (set_figure_properties, set_figure_colors, set_figure_axes, set_figure_ticks,
                               set_figure_ticklabels, set_figure_grid)
from lib.updatablecollections import UpdatableLineCollection, UpdatablePatchCollection
from lib.pixel_conversions import pixel_to_x, pixel_to_y
from lib.app_setters import set_fullscreen, set_icon
import lib.numerical_methods

from lib.frames.differentialequationsframe import DifferentialEquationsFrame
from lib.frames.figuresettingsframe import FigureSettingsFrame
from lib.frames.addgraphsframe import AddGraphsFrame
from lib.frames.addtrajectoriesframe import AddTrajectoriesFrame
from lib.frames.useractionsframe import UserActionsFrame


# Top level window
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.root_dir = os.path.dirname(__file__)
        self.platform_type = platform.system()

        self.title("planarFlow")
        self.resizable(False, False)
        set_fullscreen(self, self.platform_type)
        set_icon(self, os.path.join(self.root_dir, "lib", "logo.ico"), self.platform_type)

        self.mode = "dark"
        self.tk.call("source", os.path.join(self.root_dir, "Azure-ttk-theme-gif-based", "azure.tcl"))

        # Fonts for widgets and title labels
        self.title_font = tk.font.Font(family="DejaVu Sans", size=11, underline=True)
        self.widget_font = tk.font.Font(family="DejaVu Sans", size=10)

        # Options for colors and numerical method
        self.color_options = ("black", "gray", "white", "blue", "green", "red", "cyan", "magenta", "yellow")
        self.numerical_method_dict = dict(inspect.getmembers(lib.numerical_methods, lambda x: inspect.isfunction(x) and
                                                             x.__module__ == lib.numerical_methods.__name__))
        self.numerical_method_options = list(self.numerical_method_dict.keys())
        self.numerical_method = "RK2"  # default

        # Geometry of the top frame and UI frame dimensions
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.UI_frame_width = self.widget_font.measure("0" * 45)
        self.UI_row_height = 50  # Height of each row of widgets in UI frame

        # Widget dimensions
        self.small_button_width = 5
        self.large_button_width = 15
        self.small_entry_width = 5
        self.large_entry_width = 15

        # Figure linewidths, linestyles, and fonts, and margin width. Figure colors will be set depending on the mode
        # selected by set_figure_colors in configureplot.
        self.figure_axes_linewidth = 2
        self.figure_tick_length = 8
        self.figure_tick_fontsize = 10
        self.figure_grid_linewidth = 1
        self.figure_grid_style = ":"
        self.figure_grid_alpha = 0.5
        self.figure_width = None  # Pixel width of figure
        self.figure_height = None  # Pixel height of figure

        # Initializing figure colors. These will change as the user selects between light/dark mode.
        self.figure_background_color = None
        self.figure_axes_color = None

        # Setting size of time-series windows
        self.time_series_window_width = 800
        self.time_series_window_height = 500
        self.time_series_fontsize = 11

        # Setting size of settings window
        self.settings_window_width = 1200
        self.settings_window_height = 400

        # Initializing other attributes, such as numerical parameters and the equations to integrate.
        self.dxdt = None
        self.dydt = None
        self.dt = None
        self.tmax = None

        # Flow colors and attribute sizes
        self.flow_color = "white"
        self.flow_highlight_color = "cyan"
        self.flow_linewidth = 1
        self.flow_circle_diameter = 10  # In pixel units
        self.flow_arrowhead_size = 8  # In pixel units

        # Setting graph properties and initializing array of Graph objects.
        self.graph_linewidth = 2
        self.graphs = []

        # Animation settings.
        self.is_animating = False
        self.animation_interval = 1
        self.animation_repeat_delay = 1000

        self.set_GUI_theme(self.mode)

        # Initializing array of flow objects and collection arrays for plotting.
        self.flows = []
        self.flow_trajectory_collection = UpdatableLineCollection(lines=[], linewidths=self.flow_linewidth,
                                                                  colors=self.flow_color, zorder=-3)
        self.flow_circle_collection = UpdatablePatchCollection(patches=[], facecolors=self.flow_color, zorder=-1)
        self.flow_arrowhead_collection = UpdatablePatchCollection(patches=[], facecolors=self.flow_color, zorder=-2)
        self.collection_colors = []  # Used for coloring each collection above, in particular when they are highlighted.

        # Initializing matplotlib figure and axes.
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        # Setting default properties for the figure.
        set_figure_properties(self.fig, self.ax, self.figure_tick_length,
                              self.figure_tick_fontsize, self.figure_axes_linewidth, self.figure_grid_style,
                              self.figure_grid_linewidth, self.figure_grid_alpha)
        set_figure_colors(self.fig, self.ax, self.figure_background_color, self.figure_axes_color)

        # Binding the flow_circle_collection and flow_arrowhead_collection to the top's figure axes. These will be
        # automatically updated when the number of patches and their attributes are changed.
        self.ax.add_collection(self.flow_trajectory_collection)
        self.ax.add_collection(self.flow_circle_collection)
        self.ax.add_collection(self.flow_arrowhead_collection)

        # Initializing annotation box for when the mouse is hovering over an initial point (flow object's circle).
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(0, 0), textcoords="offset points",
                                      color=self.figure_axes_color,
                                      bbox=dict(boxstyle="round", facecolor=self.figure_background_color,
                                                edgecolor=self.flow_highlight_color), zorder=2)

        self.annot.set_visible(False)

        # Setting up child frames, which will include a frame to contain the FigureCanvas and differential_equations,
        # figure_settings, graph_equations, add_trajectories, and user_action frames.
        plotting_frame = ttk.Frame()
        plotting_frame.config(width=self.width - self.UI_frame_width, height=self.height)
        plotting_frame.pack(side="right")
        plotting_frame.pack_propagate(False)
        self.update_idletasks()
        self.figure_width = plotting_frame.winfo_width()
        self.figure_height = plotting_frame.winfo_height()

        # Top-level's FigureCanvas
        self.canvas = FigureCanvasTkAgg(self.fig, plotting_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # differential_equations frame
        self.differential_equations = DifferentialEquationsFrame(self)
        self.differential_equations.config(width=self.UI_frame_width, height=3 * self.UI_row_height)
        self.differential_equations.pack(expand=True)
        self.differential_equations.grid_propagate(False)

        # figure_settings frame
        self.figure_settings = FigureSettingsFrame(self)
        self.figure_settings.config(width=self.UI_frame_width, height=6 * self.UI_row_height)
        self.figure_settings.pack(expand=True)
        self.figure_settings.grid_propagate(False)

        # additional_graphs frame
        self.additional_graphs = AddGraphsFrame(self)
        self.additional_graphs.config(width=self.UI_frame_width, height=3 * self.UI_row_height)
        self.additional_graphs.pack(expand=True)
        self.additional_graphs.grid_propagate(False)

        # additional_trajectories frame
        self.additional_trajectories = AddTrajectoriesFrame(self)
        self.additional_trajectories.config(width=self.UI_frame_width, height=3 * self.UI_row_height)
        self.additional_trajectories.pack(expand=True)
        self.additional_trajectories.grid_propagate(False)

        # user_actions frame
        self.user_actions = UserActionsFrame(self)
        self.user_actions.config(width=self.UI_frame_width, height=2 * self.UI_row_height)
        self.user_actions.pack(expand=True)
        self.user_actions.grid_propagate(False)

        set_figure_axes(self.fig, self.ax, self.figure_settings.xmin, self.figure_settings.xmax,
                        self.figure_settings.ymin, self.figure_settings.ymax, self.figure_axes_color)
        set_figure_ticks(self.fig, self.ax, self.figure_settings.xtick_spacing,
                         self.figure_settings.xmin, self.figure_settings.xmax,
                         self.figure_settings.ytick_spacing, self.figure_settings.ymin,
                         self.figure_settings.ymax)
        set_figure_ticklabels(self.fig, self.ax, self.figure_settings.show_x_ticklabels.get(),
                              self.figure_settings.xmin, self.figure_settings.xmax,
                              self.figure_settings.show_y_ticklabels.get(), self.figure_settings.ymin,
                              self.figure_settings.ymax)
        set_figure_grid(self.fig, self.ax, self.figure_settings.show_grid.get(),
                        self.figure_settings.xtick_spacing, self.figure_settings.ytick_spacing)

        # Mouse hover event for flow circles. The flow color will change and an annotation box specifying the initial
        # conditions of that flow will be displayed.
        def on_hover(event):
            if event.inaxes == self.ax:
                cont, ind = self.flow_circle_collection.contains(event)
                if cont:
                    idx = ind['ind'][0]
                    # Change color of circle hovered over.
                    self.collection_colors[idx] = self.flow_highlight_color
                    self.flow_circle_collection.set_facecolors(self.collection_colors)
                    self.flow_trajectory_collection.set_color(self.collection_colors)
                    self.flow_arrowhead_collection.set_facecolors(self.collection_colors)

                    # Show annotation box which includes the initial condition of that flow.
                    x, y = self.flow_circle_collection.patches[idx].center
                    offset = 10

                    if x <= (self.figure_settings.xmax + self.figure_settings.xmin) / 2:  # if x is in left half
                        if y <= (self.figure_settings.ymax + self.figure_settings.ymin) / 2:  # if y is in bottom half
                            self.annot.xy = (x + pixel_to_x(offset, self.figure_width, self.figure_settings.xmin,
                                                            self.figure_settings.xmax),
                                             y + pixel_to_y(offset, self.figure_height, self.figure_settings.ymin,
                                                            self.figure_settings.ymax))
                            self.annot.set_horizontalalignment("left")
                            self.annot.set_verticalalignment("bottom")
                        else:
                            self.annot.xy = (x + pixel_to_x(offset, self.figure_width, self.figure_settings.xmin,
                                                            self.figure_settings.xmax),
                                             y - pixel_to_y(offset, self.figure_height, self.figure_settings.ymin,
                                                            self.figure_settings.ymax))
                            self.annot.set_horizontalalignment("left")
                            self.annot.set_verticalalignment("top")
                    else:
                        if y <= (self.figure_settings.ymax + self.figure_settings.ymin) / 2:
                            self.annot.xy = (x - pixel_to_x(offset, self.figure_width, self.figure_settings.xmin,
                                                            self.figure_settings.xmax),
                                             y + pixel_to_y(offset, self.figure_height, self.figure_settings.ymin,
                                                            self.figure_settings.ymax))
                            self.annot.set_horizontalalignment("right")
                            self.annot.set_verticalalignment("bottom")
                        else:
                            self.annot.xy = (x - pixel_to_x(offset, self.figure_width, self.figure_settings.xmin,
                                                            self.figure_settings.xmax),
                                             y - pixel_to_y(offset, self.figure_height, self.figure_settings.ymin,
                                                            self.figure_settings.ymax))
                            self.annot.set_horizontalalignment("right")
                            self.annot.set_verticalalignment("top")

                    text = "x0 = " + "{:+.2f}".format(x) + "\ny0 = " + "{:+.2f}".format(y)
                    self.annot.set_text(text)
                    self.annot.set_visible(True)
                else:
                    self.collection_colors = [self.flow_color] * len(self.flows)
                    self.flow_circle_collection.set_facecolors(self.collection_colors)
                    self.flow_trajectory_collection.set_color(self.collection_colors)
                    self.flow_arrowhead_collection.set_facecolors(self.collection_colors)

                    self.annot.set_visible(False)

            self.fig.canvas.draw()

        # Mouse click event for flow circles. A new window showing the time series of x(t) and y(t) for that flow
        # will be generated.
        def on_click(event):
            if event.inaxes == self.ax:
                cont, ind = self.flow_circle_collection.contains(event)
                if cont:
                    idx = ind['ind'][0]
                    x, y = self.flow_circle_collection.patches[idx].center
                    selected_flow = None

                    for flow in self.flows:
                        if flow.x0 == x and flow.y0 == y:
                            selected_flow = flow

                    if selected_flow:
                        time_series_window = tk.Toplevel(self)
                        time_series_window.attributes("-topmost", True)
                        time_series_window.resizable(True, True)
                        time_series_window.configure(height=self.time_series_window_height,
                                                     width=self.time_series_window_width)
                        time_series_window.title("Time series")
                        set_icon(time_series_window, os.path.join(self.root_dir, "lib", "logo.ico"), self.platform_type)

                        time_series_fig = plt.figure()

                        x_plot = time_series_fig.add_subplot(211)
                        x_plot.plot(selected_flow.t_values, selected_flow.x_values, color=self.flow_color,
                                    linewidth=self.flow_linewidth)
                        x_plot.set_ylabel("x(t)", color=self.figure_axes_color, fontsize=self.time_series_fontsize)
                        x_plot.autoscale(enable=True, axis="x", tight=True)

                        y_plot = time_series_fig.add_subplot(212)
                        y_plot.plot(selected_flow.t_values, selected_flow.y_values, color=self.flow_color,
                                    linewidth=self.flow_linewidth)
                        y_plot.set_ylabel("y(t)", color=self.figure_axes_color, fontsize=self.time_series_fontsize)
                        y_plot.set_xlabel("t", color=self.figure_axes_color, fontsize=self.time_series_fontsize)
                        y_plot.autoscale(enable=True, axis="x", tight=True)

                        title_str = "($x_0$, $y_0$) = (" + "{:+.2f}".format(selected_flow.x0) + ", " + \
                                    "{:+.2f}".format(selected_flow.y0) + ")"
                        x_plot.set_title(title_str, color=self.figure_axes_color, fontsize=self.time_series_fontsize)

                        # Matching style/colors to top level's figure canvas.
                        time_series_fig.set_facecolor(self.figure_background_color)

                        for tseries in (x_plot, y_plot):
                            tseries.set_facecolor(self.figure_background_color)
                            tseries.tick_params(axis="both", which="both", color=self.figure_axes_color, direction="in",
                                                labelcolor=self.figure_axes_color, labelsize=self.time_series_fontsize)

                            for spine in tseries.spines.values():
                                spine.set_edgecolor(self.figure_axes_color)
                                spine.set_linewidth(1)

                            if self.figure_settings.show_grid.get():
                                tseries.grid(linestyle=self.figure_grid_style, color=self.figure_axes_color,
                                             alpha=self.figure_grid_alpha)

                        time_series_canvas = FigureCanvasTkAgg(time_series_fig, time_series_window)
                        time_series_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                        def on_closing():
                            plt.close(time_series_fig)
                            time_series_window.destroy()

                        time_series_window.protocol("WM_DELETE_WINDOW", on_closing)

        self.fig.canvas.mpl_connect("motion_notify_event", on_hover)
        self.fig.canvas.mpl_connect("button_press_event", on_click)

        def save_image(event):
            if not self.is_animating:
                pdf_filename = filedialog.asksaveasfilename(parent=self, defaultextension=".pdf",
                                                            filetypes=(("pdf", ".pdf"),))
                if pdf_filename:
                    self.fig.savefig(pdf_filename, format="pdf", dpi=1000)

        self.bind("<Control-s>", save_image)

    def set_GUI_theme(self, mode):
        if mode == "dark":
            self.tk.call("set_theme", "dark")
            self.figure_background_color = "#404040"
            self.figure_axes_color = "white"
        elif mode == "light":
            self.tk.call("set_theme", "light")
            self.figure_background_color = "#E4E4E4"
            self.figure_axes_color = "black"


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", sys.exit)
    app.mainloop()
