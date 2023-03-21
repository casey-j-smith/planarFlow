"""
SettingsFrame class file.

Copyright (C) 2023 Casey Smith <casey.junpei.smith@gmail.com>

This file is part of planarFlow.

planarFlow is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

planarFlow is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with planarFlow. If not, see
<https://www.gnu.org/licenses/>.
"""
from tkinter import ttk, StringVar, IntVar, HORIZONTAL

from ..configureplot import (set_figure_properties, set_figure_colors, set_figure_axes, set_figure_ticklabels,
                             set_figure_grid)


class SettingsFrame(ttk.Frame):
    def __init__(self, settings_window, top):
        super().__init__(settings_window)

        self.light_mode = IntVar()
        self.dark_mode = IntVar()
        self.flow_color_selection = StringVar(value=top.flow_color)
        self.flow_highlight_color_selection = StringVar(value=top.flow_highlight_color)
        self.flow_linewidth_value = IntVar(value=top.flow_linewidth)
        self.flow_circle_diameter_value = IntVar(value=top.flow_circle_diameter)
        self.flow_arrowhead_size_value = IntVar(value=top.flow_arrowhead_size)
        self.numerical_method_selection = StringVar(value=top.numerical_method)
        self.figure_axes_color_selection = StringVar(value=top.figure_axes_color)
        self.figure_axes_linewidth_value = IntVar(value=top.figure_axes_linewidth)
        self.figure_grid_linewidth_value = IntVar(value=top.figure_grid_linewidth)
        self.figure_grid_alpha_value = IntVar(value=top.figure_grid_alpha * 100)
        self.figure_tick_fontsize_value = IntVar(value=top.figure_tick_fontsize)
        self.graph_linewidth_value = IntVar(value=top.graph_linewidth)

        for i in range(6):
            self.columnconfigure(i, weight=1)

        for i in range(8):
            self.rowconfigure(i, weight=1)

        if top.mode == "dark":
            self.light_mode.set(0)
            self.dark_mode.set(1)
        elif top.mode == "light":
            self.light_mode.set(1)
            self.dark_mode.set(0)

        # flow color
        flow_color_label = ttk.Label(self, text="Flow color: ", font=top.widget_font)
        flow_color_label.grid(row=1, column=0, sticky="e")
        flow_color_spinbox = ttk.Spinbox(self, textvariable=self.flow_color_selection, state="readonly",
                                         values=top.color_options)
        flow_color_spinbox.grid(row=1, column=1, columnspan=2, sticky="w")

        # highlighted flow color
        flow_highlight_color_label = ttk.Label(self, text="Highlight color: ", font=top.widget_font)
        flow_highlight_color_label.grid(row=2, column=0, sticky="e")
        flow_highlight_color_spinbox = ttk.Spinbox(self, textvariable=self.flow_highlight_color_selection,
                                                   state="readonly", values=top.color_options)
        flow_highlight_color_spinbox.grid(row=2, column=1, columnspan=2, sticky="w")

        # flow linewidth
        flow_linewidth_label = ttk.Label(self, text="Flow linewidth: ", font=top.widget_font)
        flow_linewidth_label.grid(row=3, column=0, sticky="e")
        flow_linewidth_viewer = ttk.Label(self, text=str(self.flow_linewidth_value.get()), font=top.widget_font,
                                          width=top.small_entry_width)
        flow_linewidth_viewer.grid(row=3, column=2)
        flow_linewidth_scale = ttk.Scale(self, from_=1, to=10, orient=HORIZONTAL, variable=self.flow_linewidth_value,
                                         style="Tick.TScale",
                                         command=lambda x: flow_linewidth_viewer.config(
                                             text=str(self.flow_linewidth_value.get())
                                         ))
        flow_linewidth_scale.grid(row=3, column=1, sticky="ew")

        # flow circle diameter
        flow_circle_diameter_label = ttk.Label(self, text="Circle diameter: ", font=top.widget_font)
        flow_circle_diameter_label.grid(row=4, column=0, sticky="e")
        flow_circle_diameter_viewer = ttk.Label(self, text=str(self.flow_circle_diameter_value.get()),
                                                font=top.widget_font, width=top.small_entry_width)
        flow_circle_diameter_viewer.grid(row=4, column=2)
        flow_circle_diameter_scale = ttk.Scale(self, from_=1, to=25, orient=HORIZONTAL,
                                               variable=self.flow_circle_diameter_value, style="Tick.TScale",
                                               command=lambda x: flow_circle_diameter_viewer.config(
                                                   text=str(self.flow_circle_diameter_value.get())
                                               ))
        flow_circle_diameter_scale.grid(row=4, column=1, sticky="ew")

        # flow arrowhead size
        flow_arrowhead_size_label = ttk.Label(self, text="Arrowhead size: ", font=top.widget_font)
        flow_arrowhead_size_label.grid(row=5, column=0, sticky="e")
        flow_arrowhead_size_viewer = ttk.Label(self, text=str(self.flow_arrowhead_size_value.get()),
                                               font=top.widget_font, width=top.small_entry_width)
        flow_arrowhead_size_viewer.grid(row=5, column=2)
        flow_arrowhead_size_scale = ttk.Scale(self, from_=1, to=25, orient=HORIZONTAL,
                                              variable=self.flow_arrowhead_size_value, style="Tick.TScale",
                                              command=lambda x: flow_arrowhead_size_viewer.config(
                                                  text=str(self.flow_arrowhead_size_value.get())
                                              ))
        flow_arrowhead_size_scale.grid(row=5, column=1, sticky="ew")

        # numerical method
        numerical_method_label = ttk.Label(self, text="Numerical method: ", font=top.widget_font)
        numerical_method_label.grid(row=6, column=0, sticky="e")
        numerical_method_spinbox = ttk.Spinbox(self, textvariable=self.numerical_method_selection, state="readonly",
                                               values=top.numerical_method_options)
        numerical_method_spinbox.grid(row=6, column=1, columnspan=2, sticky="w")

        # axes color
        axes_color_label = ttk.Label(self, text="Axes color: ", font=top.widget_font)
        axes_color_label.grid(row=1, column=3, sticky="e")
        axes_color_spinbox = ttk.Spinbox(self, textvariable=self.figure_axes_color_selection, state="readonly",
                                         values=top.color_options)
        axes_color_spinbox.grid(row=1, column=4, columnspan=2, sticky="w")

        # axis linewidth
        axes_linewidth_label = ttk.Label(self, text="Axis linewidth: ", font=top.widget_font)
        axes_linewidth_label.grid(row=2, column=3, sticky="e")
        axes_linewidth_viewer = ttk.Label(self, text=str(self.figure_axes_linewidth_value.get()), font=top.widget_font,
                                          width=top.small_entry_width)
        axes_linewidth_viewer.grid(row=2, column=5)
        axes_linewidth_scale = ttk.Scale(self, from_=1, to=10, orient=HORIZONTAL,
                                         variable=self.figure_axes_linewidth_value, style="Tick.TScale",
                                         command=lambda x: axes_linewidth_viewer.config(
                                             text=str(self.figure_axes_linewidth_value.get())
                                         ))
        axes_linewidth_scale.grid(row=2, column=4, sticky="ew")

        # grid linewidth
        grid_linewidth_label = ttk.Label(self, text="Grid linewidth: ", font=top.widget_font)
        grid_linewidth_label.grid(row=3, column=3, sticky="e")

        grid_linewidth_viewer = ttk.Label(self, text=str(self.figure_grid_linewidth_value.get()), font=top.widget_font,
                                          width=top.small_entry_width)
        grid_linewidth_viewer.grid(row=3, column=5)
        grid_linewidth_scale = ttk.Scale(self, from_=1, to=10, orient=HORIZONTAL,
                                         variable=self.figure_grid_linewidth_value, style="Tick.TScale",
                                         command=lambda x: grid_linewidth_viewer.config(
                                             text=str(self.figure_grid_linewidth_value.get())
                                         ))
        grid_linewidth_scale.grid(row=3, column=4, sticky="ew")

        # grid alpha
        grid_alpha_label = ttk.Label(self, text="Grid opacity: ", font=top.widget_font)
        grid_alpha_label.grid(row=4, column=3, sticky="e")

        grid_alpha_viewer = ttk.Label(self, text=str(self.figure_grid_alpha_value.get()) + "%", font=top.widget_font,
                                      width=top.small_entry_width)
        grid_alpha_viewer.grid(row=4, column=5)
        grid_alpha_scale = ttk.Scale(self, from_=0, to=100, orient=HORIZONTAL,
                                     variable=self.figure_grid_alpha_value, style="Tick.TScale",
                                     command=lambda x: grid_alpha_viewer.config(
                                         text=str(self.figure_grid_alpha_value.get()) + "%"
                                     ))
        grid_alpha_scale.grid(row=4, column=4, sticky="ew")

        # ticklabel size
        tick_fontsize_label = ttk.Label(self, text="Ticklabel size: ", font=top.widget_font)
        tick_fontsize_label.grid(row=5, column=3, sticky="e")
        tick_fontsize_viewer = ttk.Label(self, text=str(self.figure_tick_fontsize_value.get()), font=top.widget_font,
                                         width=top.small_entry_width)
        tick_fontsize_viewer.grid(row=5, column=5)
        tick_fontsize_scale = ttk.Scale(self, from_=1, to=25, orient=HORIZONTAL,
                                        variable=self.figure_tick_fontsize_value, style="Tick.TScale",
                                        command=lambda x: tick_fontsize_viewer.config(
                                            text=str(self.figure_tick_fontsize_value.get())
                                        ))
        tick_fontsize_scale.grid(row=5, column=4, sticky="ew")

        # graph linewidth
        graph_linewidth_label = ttk.Label(self, text="Graph linewidth: ", font=top.widget_font)
        graph_linewidth_label.grid(row=6, column=3, sticky="e")
        graph_linewidth_viewer = ttk.Label(self, text=str(self.graph_linewidth_value.get()), font=top.widget_font,
                                           width=top.small_entry_width)
        graph_linewidth_viewer.grid(row=6, column=5)
        graph_linewidth_scale = ttk.Scale(self, from_=1, to=10, orient=HORIZONTAL,
                                          variable=self.graph_linewidth_value, style="Tick.TScale",
                                          command=lambda x: graph_linewidth_viewer.config(
                                              text=str(self.graph_linewidth_value.get())
                                          ))
        graph_linewidth_scale.grid(row=6, column=4, sticky="ew")

        def set_default_light_colors():
            self.flow_color_selection.set("gray")
            self.figure_axes_color_selection.set("gray")

        def set_default_dark_colors():
            self.flow_color_selection.set("white")
            self.figure_axes_color_selection.set("white")

        def on_light():
            if self.light_mode.get():
                self.dark_mode.set(0)
                set_default_light_colors()
            else:
                self.dark_mode.set(1)
                set_default_dark_colors()

        def on_dark():
            if self.dark_mode.get():
                self.light_mode.set(0)
                set_default_dark_colors()
            else:
                self.light_mode.set(1)
                set_default_light_colors()

        # light mode
        light_mode_checkbutton = ttk.Checkbutton(self, variable=self.light_mode, onvalue=True, offvalue=False,
                                                 text="Light mode", command=on_light)
        light_mode_checkbutton.grid(row=0, column=1, columnspan=2)

        # dark mode
        dark_mode_checkbutton = ttk.Checkbutton(self, variable=self.dark_mode, onvalue=True, offvalue=False,
                                                text="Dark mode", command=on_dark)
        dark_mode_checkbutton.grid(row=0, column=3, columnspan=2)

        def apply():
            if self.light_mode.get():
                top.mode = "light"
            elif self.dark_mode.get():
                top.mode = "dark"

            top.set_GUI_theme(top.mode)

            top.flow_color = self.flow_color_selection.get()
            top.flow_highlight_color = self.flow_highlight_color_selection.get()
            top.flow_linewidth = self.flow_linewidth_value.get()
            top.flow_circle_diameter = self.flow_circle_diameter_value.get()
            top.flow_arrowhead_size = self.flow_arrowhead_size_value.get()

            top.flow_trajectory_collection.set(linewidths=top.flow_linewidth, colors=top.flow_color)
            top.flow_circle_collection.set(facecolors=top.flow_color)
            top.flow_arrowhead_collection.set(facecolors=top.flow_color)

            if top.flows:
                for flow in top.flows:
                    flow.update_circle_radius(top.flow_circle_diameter, top.figure_width, top.figure_height,
                                              top.figure_settings.xmin, top.figure_settings.xmax,
                                              top.figure_settings.ymin, top.figure_settings.ymax)
                    flow.update_arrowhead_points(top.flow_arrowhead_size, top.figure_width, top.figure_height,
                                                 top.figure_settings.xmin, top.figure_settings.xmax,
                                                 top.figure_settings.ymin, top.figure_settings.ymax)

            top.numerical_method = self.numerical_method_selection.get()

            top.figure_axes_color = self.figure_axes_color_selection.get()
            top.figure_axes_linewidth = self.figure_axes_linewidth_value.get()
            top.figure_grid_linewidth = self.figure_grid_linewidth_value.get()
            top.figure_grid_alpha = self.figure_grid_alpha_value.get() / 100
            top.figure_tick_fontsize = self.figure_tick_fontsize_value.get()

            set_figure_properties(top.fig, top.ax, top.figure_tick_length,
                                  top.figure_tick_fontsize, top.figure_axes_linewidth, top.figure_grid_style,
                                  top.figure_grid_linewidth, top.figure_grid_alpha)

            set_figure_colors(top.fig, top.ax, top.figure_background_color, top.figure_axes_color)

            set_figure_axes(top.fig, top.ax, top.figure_settings.xmin, top.figure_settings.xmax,
                            top.figure_settings.ymin, top.figure_settings.ymax, top.figure_axes_color)

            set_figure_ticklabels(top.fig, top.ax, top.figure_settings.show_x_ticklabels.get(),
                                  top.figure_settings.xmin, top.figure_settings.xmax,
                                  top.figure_settings.show_y_ticklabels.get(), top.figure_settings.ymin,
                                  top.figure_settings.ymax)

            set_figure_grid(top.fig, top.ax, top.figure_settings.show_grid.get(), top.figure_settings.xtick_spacing,
                            top.figure_settings.ytick_spacing)

            top.graph_linewidth = self.graph_linewidth_value.get()

            if top.graphs:
                for graph in top.graphs:
                    graph.update_linewidth(top.graph_linewidth)

            top.annot.set(color=top.figure_axes_color)
            top.annot.get_bbox_patch().set(facecolor=top.figure_background_color, edgecolor=top.flow_highlight_color)

            top.fig.canvas.draw()

        # apply button
        apply_button = ttk.Button(self, width=top.small_button_width, style="Accent.TButton", text="Apply",
                                  command=apply)
        apply_button.grid(row=7, column=2, columnspan=2)
