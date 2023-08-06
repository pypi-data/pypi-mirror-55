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

import os
import pandas as pd

from _plotly_future_ import v4_subplots  # no longer important for version 4
import plotly.graph_objs as go  # graph_objects in v4 but still supported
from plotly.subplots import make_subplots

from ..plot_helpers import get_df_time, palette


def plot_concentrations(results, metabolites=[], strain="Biomass"):
    """Plot the concentration results of a simulated DfbaModel (plotly)
    The resulting plot can be managed with the returned object for this backend.

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

    Returns
    -------
    fig: plotly.graph_objs.Figure
        plotly Figure object that can be displayed (`show()` method) and saved (`write_*` methods)
    """
    # filter
    to_plot = results
    if metabolites:
        to_plot = to_plot.loc[:, metabolites]
    t = get_df_time(results)
    if "time" in to_plot:
        to_plot = to_plot.drop("time", axis=1)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for name in to_plot:
        if name == strain:
            fig.add_trace(
                go.Scatter(x=t, y=to_plot[name], mode="lines", name=name),
                secondary_y=False,
            )
        elif name != "time":
            fig.add_trace(
                go.Scatter(
                    x=t,
                    y=to_plot[name],
                    mode="lines",
                    name=name,
                    line=dict(dash="dot"),
                ),
                secondary_y=True,
            )
    # Set axis labels
    # TODO: I don't know if I should add the units here...
    fig.update_xaxes(title_text="<b>time</b> h")
    fig.update_yaxes(title_text="<b>biomass</b> g/L", secondary_y=False)
    fig.update_yaxes(title_text="<b>metabolites</b> mmol/L", secondary_y=True)
    return fig


def plot_trajectories(results, reactions=[]):
    """Plot the flux trajectories of a simulated DfbaModel (plotly)
    The resulting plot can be managed with the returned object for this backend.

    Plot description
    y-axis: flux trajectories (Concentration/gDw/time).
    x-axis: time

    Parameters
    ----------
    results: pandas.DataFrame
        results of the simulation. It expects a "time" column
    reactions: list of strings
        name of the reactions in the legend. Default: all columns

    Returns
    -------
    fig: plotly.graph_objs.Figure
        plotly Figure object that can be displayed (`show()` method) and saved (`write_*` methods)
    """
    # filter
    to_plot = results
    if reactions:
        to_plot = to_plot.loc[:, reactions]
    t = get_df_time(results)
    if "time" in to_plot:
        to_plot = to_plot.drop("time", axis=1)

    fig = go.Figure()
    for name in to_plot:
        fig.add_trace(go.Scatter(x=t, y=to_plot[name], mode="lines", name=name))
    fig.update_xaxes(title_text="<b>time</b>")
    fig.update_yaxes(title_text="<b>flux trajectories</b>")
    return fig
