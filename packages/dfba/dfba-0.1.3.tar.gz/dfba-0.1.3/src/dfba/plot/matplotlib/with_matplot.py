# Copyright (C) 2018, 2019 Columbia University Irving Medical Center,
#     New York, USA
# Copyright (C) 2019 Novo Nordisk Foundation Center for Biosustainability,
#     Technical University of Denmark

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import pandas as pd

import matplotlib.pyplot as plt

from ..plot_helpers import get_df_time, palette


def plot_concentrations(results, metabolites=[], strain="Biomass"):
    """Plot the concentration results of a simulated DfbaModel (matplotlib)
    The resulting plot can be managed with `matplotlib.pyplot` as usual with this library.

    Plot description
    2 y-axes: biomass on the left, (Concentration/time)
              metabolites on the right (Concentration/time)
    x-axis: `time`

    Parameters
    ----------
    results: pandas.DataFrame
        results of the simulation. It expects a "time" column
    metabolites: list of strings
        name of the metabolites/strains in the legend. Default: all columns
    strain: string
        name of biomass in `metabolites`. Default: "Biomass"
    """
    # apply filters
    to_plot = results
    if metabolites:
        to_plot = to_plot.loc[:, metabolites]
    t = get_df_time(results)
    if "time" in to_plot:
        to_plot = to_plot.drop("time", axis=1)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    # the colors of lines in different axis must not overlap
    ax2.set_prop_cycle("color", palette[1:])
    for col in to_plot:
        if col == strain:
            ax1.plot(t, to_plot[col], palette[0], linewidth=0.8, label=col)
        elif col != "time":
            ax2.plot(t, to_plot[col], linestyle="--", linewidth=0.8, label=col)
    # Set axis labels
    ax1.set_xlabel("time")
    ax1.set_ylabel("biomass")
    ax2.set_ylabel("metabolites")
    # legend outside the plot
    fig.legend(loc="center right", borderaxespad=0.1)
    plt.subplots_adjust(right=0.7)
    return


def plot_trajectories(results, reactions=[]):
    """Plot the flux trajectories of a simulated DfbaModel (matplotlib)
    The resulting plot can be managed with `matplotlib.pyplot` as usual with this library.

    Plot description
    y-axis: flux trajectories (Concentration/gDw/time).
    x-axis: time

    Parameters
    ----------
    results: pandas.DataFrame
        results of the simulation. It expects a "time" column
    reactions: list of strings
        name of the reactions in the legend. Default: all columns
    """
    # apply filters
    to_plot = results
    if reactions:
        to_plot = to_plot.loc[:, reactions]
    t = get_df_time(results)
    if "time" in to_plot:
        to_plot = to_plot.drop("time", axis=1)

    fig, ax = plt.subplots(1, 1)
    for col in to_plot:
        plt.plot(t, to_plot[col], label=col)
    plt.xlabel("time")
    plt.ylabel("flux trajectories")
    # legend outside the plot
    fig.legend(loc="center right", borderaxespad=0.1)
    plt.subplots_adjust(right=0.7)
    return
