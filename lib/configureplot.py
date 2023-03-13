"""
Collection of functions that updates the top window's figure axes, ticks, ticklabels, and grid based on user input
values entered and validated in the FigureSettingsFrame. Methods to set the figure style and colors/theme are also
included.

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


def set_figure_properties(fig, ax, tick_length, tick_fontsize, axes_linewidth, grid_style, grid_linewidth, grid_alpha):
    # Setting margin widths.
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    # Setting tick style parameters.
    ax.tick_params(length=tick_length, width=axes_linewidth, direction="in", axis="both", which="both",
                   labelsize=tick_fontsize, zorder=0)

    # Setting axes width.
    for spine in ax.spines.values():
        spine.set_linewidth(axes_linewidth)
        spine.set_zorder(0)

    # Setting gridline style parameters.
    ax.grid(linestyle=grid_style, linewidth=grid_linewidth, alpha=grid_alpha)

    fig.canvas.draw()


def set_figure_colors(fig, ax, background_color, axes_color):
    # Setting background color.
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Setting axes color.
    for spine in ax.spines.values():
        spine.set_edgecolor(axes_color)

    # Setting tick color.
    ax.tick_params(axis="both", which="both", color=axes_color, labelcolor=axes_color)

    # Setting grid color.
    ax.grid(color=axes_color)

    fig.canvas.draw()


def set_figure_axes(fig, ax, xmin, xmax, ymin, ymax, figure_axes_color):
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # The location of the spines will be reset to the left/right and top/bottom boundaries whenever this function is
    # called. The location of the bottom/left spline may change if the x/y-axis is to be drawn somewhere in the middle.
    ax.spines["left"].set_position(("axes", 0))
    ax.spines["right"].set_position(("axes", 1))
    ax.spines["bottom"].set_position(("axes", 0))
    ax.spines["top"].set_position(("axes", 1))

    # Setting location of y-axis.
    if xmin < 0 < xmax:  # If the y-axis should be somewhere in the middle...
        ax.spines["left"].set_color(figure_axes_color)
        ax.spines["left"].set_position("zero")  # Reposition a spine to go where "zero" is.
        ax.spines["right"].set_color("none")
    elif xmax == 0:  # If the y-axis should be on the right side.
        ax.spines["left"].set_color("none")
        ax.spines["right"].set_color(figure_axes_color)
    elif xmin == 0:  # If the y-axis should be on the left side...
        ax.spines["left"].set_color(figure_axes_color)
        ax.spines["right"].set_color("none")
    else:  # If the y-axis is not in viewing range.
        ax.spines["left"].set_color("none")
        ax.spines["right"].set_color("none")

    # Setting location of x-axis.
    if ymin < 0 < ymax:  # If the x-axis should be somewhere in the middle...
        ax.spines["bottom"].set_color(figure_axes_color)
        ax.spines["bottom"].set_position("zero")  # Reposition a spine to go where "zero" is.
        ax.spines["top"].set_color("none")
    elif ymax == 0:  # If the x-axis should be on the top.
        ax.spines["bottom"].set_color("none")
        ax.spines["top"].set_color(figure_axes_color)
    elif ymin == 0:  # If the x-axis should be on the bottom.
        ax.spines["bottom"].set_color(figure_axes_color)
        ax.spines["top"].set_color("none")
    else:  # If the x-axis is not in viewing range.
        ax.spines["bottom"].set_color("none")
        ax.spines["top"].set_color("none")

    fig.canvas.draw()


def set_figure_ticks(fig, ax, xtick_spacing, xmin, xmax, ytick_spacing, ymin, ymax):
    if xtick_spacing:  # Configuring xticks
        if xmin < 0 < xmax:
            xticks = np.concatenate((-np.arange(0, -xmin, xtick_spacing), np.arange(0, xmax, xtick_spacing)))
        else:
            xticks = np.arange(xmin, xmax, xtick_spacing)

        xticks = xticks[xticks != 0]  # Removing zero tick
        ax.set_xticks(xticks)

        # Set location of x tickmarks based on ymin/ymax values.
        if (ymin < 0 < ymax) or ymin >= 0:
            ax.tick_params(axis="x", bottom=True, top=False)
        else:
            ax.tick_params(axis="x", bottom=False, top=True)
    else:
        ax.set_xticks([])

    if ytick_spacing:  # Configuring yticks
        if ymin < 0 < ymax:
            yticks = np.concatenate((-np.arange(0, -ymin, ytick_spacing), np.arange(0, ymax, ytick_spacing)))
        else:
            yticks = np.arange(ymin, ymax, ytick_spacing)

        yticks = yticks[yticks != 0]  # Removing zero tick
        ax.set_yticks(yticks)

        # Set location of yticks based on xmin/xmax values.
        if (xmin < 0 < xmax) or xmin >= 0:
            ax.tick_params(axis="y", left=True, right=False)
        else:
            ax.tick_params(axis="y", left=False, right=True)
    else:
        ax.set_yticks([])

    fig.canvas.draw()


def set_figure_ticklabels(fig, ax, show_x_ticklabels, xmin, xmax, show_y_ticklabels, ymin, ymax):
    if show_x_ticklabels:
        if ymin >= 0:  # If the ticks are on the very bottom...
            ax.tick_params(axis="x", labelbottom=True, labeltop=False, pad=-18)
        elif ymax <= 0:  # If the ticks are on very top...
            ax.tick_params(axis="x", labelbottom=False, labeltop=True, pad=-18)
        else:
            ax.tick_params(axis="x", labelbottom=True, labeltop=False, pad=6)
        for xtick in ax.get_xticklabels():
            xtick.set_horizontalalignment("left")
    else:
        ax.tick_params(axis="x", labelbottom=False, labeltop=False)

    if show_y_ticklabels:
        if xmin >= 0:  # If the ticks are on the very left...
            ax.tick_params(axis="y", labelleft=True, labelright=False, pad=-36)
        elif xmax <= 0:  # If the ticks are on the very right...
            ax.tick_params(axis="y", labelleft=False, labelright=True, pad=-36)
        else:
            ax.tick_params(axis="y", labelleft=True, labelright=False, pad=6)
        for ytick in ax.get_yticklabels():
            ytick.set_verticalalignment("bottom")
    else:
        ax.tick_params(axis="y", labelleft=False, labelright=False)

    fig.canvas.draw()


def set_figure_grid(fig, ax, show_grid, xtick_spacing, ytick_spacing):
    if show_grid:
        if xtick_spacing:
            ax.grid(visible=True, axis="x")

        if ytick_spacing:
            ax.grid(visible=True, axis="y")
    else:
        ax.grid(visible=False, axis="both")

    fig.canvas.draw()
