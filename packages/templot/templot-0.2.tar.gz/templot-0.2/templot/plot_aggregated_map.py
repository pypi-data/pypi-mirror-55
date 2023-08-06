"""
Plot Aggregated Map.
"""

import numpy as np
import pandas as pd
import folium
import json
import pkg_resources
import os
import warnings
import matplotlib.pyplot as plt
import re
from io import BytesIO
import base64

DATA_PATH = pkg_resources.resource_filename('templot', 'data')


def plot_aggregated_map(df, vars, group="Regions", agr="average", height=300):

    """
    Plots a map of aggregated values of y by group.

    :param df: data
    :param vars: a list of ncolumn names conatining values each year
    :param group: group variable name
    :param agr: aggregation method
    :param height: tooltip height in pixels
    :return: folium map

    One example of this simple graph:

    .. raw:: html

        <iframe src="example_agrmap.html" height="600px" width="100%"></iframe>

    """

    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError(f"df must be a DataFrame not {type(df)}.")

    if len(df.shape) != 2:
        raise ValueError(f"df must be a matrix but shape is {df.shape}")

    if df.shape[1] < 2:
        raise ValueError(
            f"df must be a matrix with at least two columns but shape is {df.shape}"
        )

    if not vars:
        raise ValueError(f"vars must be supplied.")

    if not isinstance(vars, list):
        raise TypeError(f"vars must be a list, not {type(vars)}")

    for var in vars:
        if var not in df.columns:
            raise ValueError(f"{var} is not a valid column name.")

        if df[var].dtype != "float64":
            raise ValueError(
                f"{var} must contain numeric values, specifically float64."
            )

    if group not in df.columns:
        raise ValueError(f"{group} is not a valid column name.")

    if group not in ["Regions", "Departements", "Communes"]:
        raise ValueError(
            f"{group} is not a valid name. Possible values are: Regions, Departements or Communes"
        )

    if not isinstance(height, int):
        raise TypeError(f"Height must be an int, not {type(height)}")

    if height <= 0:
        raise ValueError("Tooltip height must be positive")

    if len(df[group].unique()) > 90:
        warnings.warn(
            f"Having too many groups may result in reduced performance."
        )

    aggregates = {
        "average": df.groupby(group).mean(),
        "median": df.groupby(group).median(),
        "max": df.groupby(group).max(),
        "min": df.groupby(group).min(),
        "count": df.groupby(group).count().astype("float"),
    }

    if agr not in aggregates:
        raise ValueError(
            f"{group} is not a valid aggregation method. Possible values are: {', '.join([k for k in aggregates])}"
        )

    map_data = aggregates[agr][vars]

    if group == "Regions":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'regions.geojson')).read()
        )

    if group == "Departements":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'departements.geojson')).read()
        )

    if group == "Communes":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'communes.geojson')).read()
        )

    for feat in geojson["features"]:
        if feat["properties"]["nom"] in map_data.index:
            row = map_data[map_data.index == feat["properties"]["nom"]]
            heights = (row[vars]).values.flatten().tolist()
            y_pos = np.arange(len(vars))
            plt.bar(y_pos, heights)
            labels = [
                re.search(r"\d{4}", s).group() if re.search(r"\d{4}", s) else s
                for s in vars
            ]
            plt.xticks(y_pos, labels)
            plt.xticks(rotation=45, size=9)
            plt.title(feat["properties"]["nom"])
            img2bytes = BytesIO()
            plt.savefig(img2bytes, format='png')
            plt.close()
            img2bytes.seek(0)
            bytesto64 = base64.b64encode(img2bytes.read())
            feat["properties"][
                "image"
            ] = f'<img height="{height}" src="data:image/png;base64,{bytesto64.decode("utf-8")}"/>'

        else:
            feat["properties"]["image"] = ""

    m = folium.Map(tiles="CartoDB positron", zoom_start=2)
    choropleth = folium.Choropleth(
        geo_data=geojson,
        data=map_data.mean(axis=1),
        fill_color="BuPu",
        key_on="feature.properties.nom",
        highlight=True,
        bins=9,
    ).add_to(m)

    choropleth.color_scale.caption = (
        f'Mean {agr} quantity over the {len(vars)} years'
    )
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=["image"], labels=False)
    )

    m.fit_bounds(m.get_bounds())
    return m
