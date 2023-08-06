"""
Unit tests for ``plot_aggregated_map``.
"""
import unittest
from templot import plot_aggregated_map, download_irep, add_regions
import os
import pandas as pd


class TestPlotAggregatedMap(unittest.TestCase):
    "Tests for submodule plot_aggregated_map"
    filepath = os.path.join('.', 'df_test.csv')

    if not os.path.exists(filepath):
        download_irep(filepath)
        df = pd.read_csv(filepath)
        df = add_regions(
            df, "LLX", "LLY", add=["regions", "departements", "communes"]
        )
        df.to_csv(filepath, index=False)

    df = pd.read_csv(filepath)

    def test_bad_df(self):
        with self.assertRaises(TypeError):
            df = []
            plot_aggregated_map(df)

    def test_bad_var(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                var="Quantite201",
                group="Regions",
                agr="average",
                log="auto",
            )

    def test_bad_group(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                var="Quantite2017",
                group="Departement",
                agr="average",
                log="auto",
            )

    def test_performance(self):
        with self.assertWarns(UserWarning):
            plot_aggregated_map(
                self.df,
                var="Quantite2017",
                group="Departements",
                agr="average",
                log="auto",
            )

    def test_bad_agr(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                var="Quantite2017",
                group="Departement",
                agr="averag",
                log="auto",
            )

    def test_bad_log(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                var="Quantite2017",
                group="Departement",
                agr="averag",
                log="False",
            )


if __name__ == '__main__':
    unittest.main()
