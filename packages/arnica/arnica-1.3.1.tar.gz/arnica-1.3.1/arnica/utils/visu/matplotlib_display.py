"""
matplotlib_display.py

It permits to display the desired graphs, thanks to the the provided layout
and the provided data frame, with the library "matplotlib"
"""

from math import ceil
from mplcursors import cursor
import pandas as pd
import matplotlib.pyplot as plt
from arnica.utils.visu.lay_and_temp_manager import decompact_template

__all__ = ["display"]


def display(layout, data):
    """It displays the desired graphs described by the provided layout
    thanks to the provided key-value object which contains
    the required data

    Input:
    ------
    data : key-value object
    layout : nested object
    """

    for curve in layout["graphs"]:
        for var in curve["curves"]:
            for val in var.values():
                if "*" in val:
                    layout = decompact_template(layout, data)


    if not isinstance(data, pd.DataFrame):
        dataframe = pd.DataFrame.from_dict(data)
    else:
        dataframe = data

    figure_number = 0
    graph_position = 1
    display_params = initialize_display(layout)

    for graph_layout in layout['graphs']:
        if (graph_position > display_params['numb_max_of_graphs_per_fig']
                or figure_number == 0):
            graph_position = 1
            figure_number += 1
            figure = build_new_figure(display_params, figure_number)
        build_new_graph(figure, display_params['fig_struct'],
                        graph_position, graph_layout, dataframe)
        graph_position += 1

    cursor()
    plt.show()


def initialize_display(layout):
    """Sets some parameters needed by the function "display", thanks
    to the provided layout, and returns them in a dictionary

    Input:
    ------
    layout : nested object

    Output:
    ------
    display_params : dictionary
    """

    display_params = {}
    display_params['numb_of_graphs'] = len(layout['graphs'])

    if "figure_structure" in layout:
        display_params['fig_struct'] = layout["figure_structure"]
    else:
        if display_params['numb_of_graphs'] == 1:
            display_params['fig_struct'] = [1, 1]
        else:
            display_params['fig_struct'] = [2, 3]

    display_params['numb_max_of_graphs_per_fig'] = (display_params['fig_struct'][0]
                                                    *display_params['fig_struct'][1])
    display_params['numb_of_figs'] = ceil(display_params['numb_of_graphs']
                                          /display_params['numb_max_of_graphs_per_fig'])

    if "figure_dpi" in layout:
        display_params['fig_dpi'] = layout["figure_dpi"]
    else:
        display_params['fig_dpi'] = None

    if "figure_size" in layout:
        display_params['fig_size'] = layout["figure_size"]
    else:
        display_params['fig_size'] = None

    if "title" in layout:
        display_params['lay_title'] = layout['title']
    else:
        display_params['lay_title'] = None

    return display_params


def build_new_figure(display_params, figure_number):
    """Builds a new matplotlib figure thanks to the provided parameters

    Input:
    ------
    display_params : dictionary
    figure_number : integer

    Output:
    ------
    figure : matplotlib object
    """

    if display_params['fig_dpi']:
        figure = plt.figure(dpi=display_params['fig_dpi'])
    else:
        figure = plt.figure()

    if display_params['fig_size']:
        figure.set_size_inches(*display_params['fig_size'])

    if display_params['lay_title']:
        if display_params['numb_of_graphs'] <= display_params['numb_max_of_graphs_per_fig']:
            figure_name = display_params['lay_title']
        else:
            figure_name = (display_params['lay_title'] +
                           ' (' + str(figure_number) + '/' +
                           str(display_params['numb_of_figs']) + ')')
        figure.canvas.set_window_title(figure_name)
        figure.suptitle(figure_name, fontsize=20,
                        fontweight='bold', y=0.99)

    figure.subplots_adjust(left=0.1, bottom=0.1,
                           right=0.9, top=0.9,
                           wspace=0.3, hspace=0.3)

    return figure


def build_new_graph(figure, figure_structure, graph_position,
                    graph_layout, dataframe):
    """Builds a new matplotlib graph in the provided matplotlib
    figure thanks to the provided parameters

    Input:
    ------
    figure : matplotlib object
    figure_structure : tuple of 2 integers
    graph_position : integer
    graph_layout : nested object
    dataframe : pandas data frame
    """

    subplot = figure.add_subplot(*figure_structure, graph_position)

    if "x_label" in graph_layout:
        subplot.set_xlabel(graph_layout["x_label"])

    if "y_label" in graph_layout:
        subplot.set_ylabel(graph_layout["y_label"])

    if "title" in graph_layout:
        subplot.set_title(graph_layout["title"],
                          fontweight='bold')

    if graph_layout["x_var"] in dataframe.keys():
        for curve_layout in graph_layout["curves"]:
            if curve_layout["var"] in dataframe.keys():
                if "legend" in curve_layout:
                    curve_legend = curve_layout["legend"]
                else:
                    curve_legend = curve_layout["var"]
                subplot.plot(dataframe[graph_layout["x_var"]],
                             dataframe[curve_layout["var"]],
                             label=curve_legend)

    subplot.legend(loc='upper right')
