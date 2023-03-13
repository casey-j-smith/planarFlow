"""
UserActionsFrame class file.

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from tkinter import ttk, PhotoImage, Toplevel, TOP, BOTH
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..configureplot import (set_figure_properties, set_figure_colors, set_figure_axes, set_figure_ticks,
                             set_figure_ticklabels, set_figure_grid)
from ..updatablecollections import UpdatablePatchCollection, UpdatableLineCollection
from .settingsframe import SettingsFrame
from ..makefullscreen import make_fullscreen


class UserActionsFrame(ttk.Frame):
    def __init__(self, top):
        super().__init__()

        self.settings_icon = PhotoImage(file="lib/settings_icon.png")

        for i in range(4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)

        # Function definition for starting flow animation.
        def animate_flow():
            top.is_animating = True

            ani_window = Toplevel(top)
            make_fullscreen(ani_window)

            ani_window.resizable(False, False)
            ani_window.title("")

            ani_frame = ttk.Frame(ani_window, width=top.figure_width, height=top.figure_height)
            ani_frame.pack(anchor="center")
            ani_frame.pack_propagate(False)

            ani_fig = plt.figure()
            ani_ax = ani_fig.add_subplot(1, 1, 1)

            ani_canvas = FigureCanvasTkAgg(ani_fig, ani_frame)
            ani_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

            # Initializing
            set_figure_properties(ani_fig, ani_ax, top.figure_tick_length,
                                  top.figure_tick_fontsize, top.figure_axes_linewidth, top.figure_grid_style,
                                  top.figure_grid_linewidth, top.figure_grid_alpha)

            set_figure_colors(ani_fig, ani_ax, top.figure_background_color, top.figure_axes_color)

            set_figure_axes(ani_fig, ani_ax, top.figure_settings.xmin, top.figure_settings.xmax,
                            top.figure_settings.ymin, top.figure_settings.ymax, top.figure_axes_color)

            set_figure_ticks(ani_fig, ani_ax, top.figure_settings.xtick_spacing,
                             top.figure_settings.xmin,
                             top.figure_settings.xmax, top.figure_settings.ytick_spacing,
                             top.figure_settings.ymin, top.figure_settings.ymax)

            set_figure_ticklabels(ani_fig, ani_ax, top.figure_settings.show_x_ticklabels.get(),
                                  top.figure_settings.xmin, top.figure_settings.xmax,
                                  top.figure_settings.show_y_ticklabels.get(), top.figure_settings.ymin,
                                  top.figure_settings.ymax)

            set_figure_grid(ani_fig, ani_ax, top.figure_settings.show_grid.get(),
                            top.figure_settings.xtick_spacing, top.figure_settings.ytick_spacing)

            ani_flow_trajectory_collection = UpdatableLineCollection(lines=[], linewidths=top.flow_linewidth,
                                                                     colors=top.flow_color, zorder=-3)
            ani_flow_circle_collection = UpdatablePatchCollection(patches=[], facecolors=top.flow_color, zorder=-1)
            ani_flow_arrowhead_collection = UpdatablePatchCollection(patches=[], facecolors=top.flow_color, zorder=-2)

            for flow in top.flows:
                ani_flow_trajectory_collection.lines.append(flow.trajectory)
                ani_flow_circle_collection.patches.append(flow.circle)
                ani_flow_arrowhead_collection.patches.append(flow.arrowhead)

            ani_ax.add_collection(ani_flow_trajectory_collection)
            ani_ax.add_collection(ani_flow_circle_collection)
            ani_ax.add_collection(ani_flow_arrowhead_collection)

            # Redrawing all graphs to the animation canvas.
            for graph in top.graphs:
                for collection in graph.contours.collections:
                    for path in collection.get_paths():
                        ani_ax.plot(path.vertices[:, 0], path.vertices[:, 1], color=graph.color,
                                    linewidth=top.graph_linewidth, zorder=-4)

            # Animation procedure. Each Flow's circle moves along the trajectory based on the values calculated when
            # integrating. The animation ends with all the circles at their initial conditions.
            def init_animation():
                return ani_flow_circle_collection,

            def animate(frame):
                for idx in range(len(top.flows)):
                    if frame < len(top.flows[0].t_values):
                        top.flows[idx].circle.center = (top.flows[idx].x_values[frame], top.flows[idx].y_values[frame])
                    else:
                        top.flows[idx].circle.center = (top.flows[idx].x0, top.flows[idx].y0)

                return ani_flow_circle_collection,

            if top.flows:
                anim = animation.FuncAnimation(ani_fig, init_func=init_animation, func=animate,
                                               frames=len(top.flows[0].t_values) + 1, interval=top.animation_interval,
                                               repeat_delay=top.animation_repeat_delay, blit=True,
                                               cache_frame_data=False)
            ani_fig.canvas.draw()

            def on_closing():
                # Place all flow circles back to their starting position after closing animation.
                for idx in range(len(top.flows)):
                    top.flows[idx].circle.center = (top.flows[idx].x0, top.flows[idx].y0)

                top.is_animating = False
                plt.close(ani_fig)
                ani_window.destroy()

            ani_window.protocol("WM_DELETE_WINDOW", on_closing)

        # Animate flow button
        animate_flow_button = ttk.Button(self, width=top.large_button_width, style="Accent.TButton",
                                         text="Animate Flow", command=animate_flow)
        animate_flow_button.grid(row=0, column=0, columnspan=3)

        def open_settings():
            settings_window = Toplevel(top)
            settings_window.resizable(False, False)
            settings_window.title("")

            settings_frame = SettingsFrame(settings_window, top)
            settings_frame.config(width=top.settings_window_width, height=top.settings_window_height)
            settings_frame.pack()
            settings_frame.grid_propagate(False)

        settings_button = ttk.Button(self, image=self.settings_icon, width=1, command=open_settings)
        settings_button.grid(row=0, column=3)
