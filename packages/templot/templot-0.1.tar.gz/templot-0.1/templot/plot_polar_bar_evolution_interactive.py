"""
Plot Interactive polar bar.
"""

import plotly.express as px


def plot_polar_bar_evolution_interactive(
    df, var="Quantite", year="Annee", group="Regions", agr="average"
):

    """
    Plots a polar bar showing the evolution of y by group across year.

    :param df: data
    :param var: y
    :param year: year
    :param group: group variable name
    :param agr: aggregation method
    :return: plotly figure

    One example of this simple graph:

    .. raw:: html

        <iframe src="example_polarbar.html" height="620px" width="100%"></iframe>

    """

    aggregates = {
        "average": df.groupby([group, year])[var].mean().reset_index(),
        "median": df.groupby([group, year])[var].median().reset_index(),
        "max": df.groupby([group, year])[var].max().reset_index(),
        "min": df.groupby([group, year])[var].min().reset_index(),
        "count": df.groupby([group, year])[var].count().astype("float").reset_index(),
    }

    df_agr = aggregates[agr]

    fig = px.bar_polar(
        df_agr,
        r=var,
        theta=group,
        color=group,
        animation_frame=year,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma[-2::-1],
    )
    fig.update_layout(showlegend=False)
    return fig
