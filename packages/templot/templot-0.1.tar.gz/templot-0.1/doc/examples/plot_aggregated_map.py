"""
Plot Aggregated Map Example.
============================
"""
import os
import pandas as pd
from templot import plot_aggregated_map, add_regions, download_irep


filepath = os.path.join('..', 'templot', 'data', 'df.csv')

if not os.path.exists(filepath):
    download_irep(filepath)
    df = pd.read_csv(filepath)
    df = add_regions(df, "LLX", "LLY")
    df.to_csv(filepath, index=False)

df = pd.read_csv(filepath)

map = plot_aggregated_map(df=df)

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    with open(os.path.join(tmp_dir, 'example_agrmap.html'), 'wt') as fh:
        fh.write(map.get_root().render())

####################################
# .. raw:: html
#
#     <iframe src="../example_agrmap.html" height="600px" width="100%"></iframe>
