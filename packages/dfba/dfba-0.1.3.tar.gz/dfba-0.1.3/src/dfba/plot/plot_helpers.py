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

"""
utils functions for management of dataframes for plotting
"""

palette = [  # color scheme: http://geog.uoregon.edu/datagraphics/color/Cat_12.txt
    "#ff7f00",  # TODO: maybe use palletable for this
    "#32ff00",  #       but I'm not sure if it is worh to install
    "#19b2ff",  #       another dependency just for the color scheme
    "#654cff",
    "#e51932",
    "#000000",
    "#ffff32",
    "#ff99bf",
    "#ccbfff",
    "#a5edff",
    "#b2ff8c",
    "#ffff99",
    "#ffbf7f",
]


def get_df_time(df):
    """ Get the x-axis (time) from a pd.DataFrame `df` """
    return range(0, df.shape[0]) if not "time" in df else df.time
