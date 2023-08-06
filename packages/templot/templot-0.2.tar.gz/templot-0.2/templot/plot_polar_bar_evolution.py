"""
Plot polar bar.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def plot_polar_bar_evolution(
    df, var="Quantite", year="Annee", group="Regions", agr="average"
):

    """
    Plots a polar bar showing the evolution of y by group across year.

    :param df: data
    :param var: y
    :param year: year
    :param group: group variable name
    :param agr: aggregation method
    :return: matplotlib animation

    One example of this simple graph:

    .. raw:: html

        <img src="example_polarbar_animation.gif" height="620px" width="100%">

    """

    aggregates = {
        "average": df.groupby([group, year])[var].mean().reset_index(),
        "median": df.groupby([group, year])[var].median().reset_index(),
        "max": df.groupby([group, year])[var].max().reset_index(),
        "min": df.groupby([group, year])[var].min().reset_index(),
        "count": df.groupby([group, year])[var]
        .count()
        .astype("float")
        .reset_index(),
    }

    df_agr = aggregates[agr]

    N = len(df_agr[group].unique())

    theta = np.arange(0, 2 * np.pi, 2 * np.pi / N)
    data = df_agr[var]

    viridis = plt.cm.get_cmap('viridis')
    c = viridis(np.interp(data, (data.min(), data.max()), (0, +1)))

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, polar=True)
    ax.set_xticks(theta)
    ax.set_xticklabels(df_agr[group].unique())

    for th, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        th = th * ax.get_theta_direction() + ax.get_theta_offset()
        th = np.pi / 2 - th
        y, x = np.cos(th), np.sin(th)
        if x >= 0.1:
            label.set_horizontalalignment('left')
        if x <= -0.1:
            label.set_horizontalalignment('right')
        if y >= 0.5:
            label.set_verticalalignment('bottom')
        if y <= -0.5:
            label.set_verticalalignment('top')

    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    plt.setp(ax.get_yticklabels(), visible=False)

    cNorm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
    ax3 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax3, norm=cNorm)
    plt.gcf().subplots_adjust(right=0.7)

    years = df_agr[year].unique()
    data = df_agr[df_agr[year] == years[0]][var]
    title = f"{var} de {years[0]}"
    ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1))
    ax.bar(theta, data, width=0.4, color=c[df_agr[year] == years[0]])

    def update(i):
        data = df_agr[df_agr[year] == years[i]][var]
        for obj in ax.findobj(match=mpl.patches.Rectangle):
            obj.remove()
        title = f"{var} de {years[i]}"
        ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1))
        bars = ax.bar(
            theta, data, width=0.4, color=c[df_agr[year] == years[i]]
        )
        return bars

    ani = animation.FuncAnimation(
        fig, update, frames=len(years), interval=1000, blit=False, repeat=False
    )
    plt.close()
    return ani
