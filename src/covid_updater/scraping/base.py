import os
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


class Scraper:
    def __init__(self, country, country_iso, data_url, data_url_reference, region_renaming=None, column_renaming=None,
                 mode_iso_merge=None, do_cumsum_fields=None):
        self.country = country
        self.country_iso = country_iso
        self.data_url = data_url
        self.data_url_reference = data_url_reference
        self.region_renaming = region_renaming if region_renaming is not None else {}
        self.column_renaming = column_renaming if column_renaming is not None else {}
        self.mode_iso_merge = mode_iso_merge if mode_iso_merge is not None else "region_iso"
        self.do_cumsum_fields = do_cumsum_fields if do_cumsum_fields is not None else []

    def load_data(self):
        raise NotImplementedError("Call child's method instead.")

    def _preprocess(self, df):
         # Rename column names
        df = df.rename(columns=self.column_renaming)

        # Add location info
        if "location" not in df.columns:
            df.loc[:, "location"] = self.country

        # Rename regions
        if "region" in df.columns:
            df = df.loc[~df.loc[:, "region"].isnull()]
            df.loc[:, "region"] = df.loc[:, "region"].replace(self.region_renaming)
        return df

    def _process(self, df):
        raise NotImplementedError("Call child's method instead!")

    def _postprocess(self, df):
        df = ISODB().merge(df, country_iso=self.country_iso, mode=self.mode_iso_merge)
        df = df.sort_values(by="date")
        for field in self.do_cumsum_fields:
            df[field] = df.groupby("region")[field].cumsum().values
        # TODO: Insert here population info (need path to population.csv as class attribute)
        return df

    def process(self, df):
        # Common preprocessing
        df = self._preprocess(df)
        # Country-specific processing
        df = self._process(df)
        # Add ISO codes
        df = self._postprocess(df)
        return df

    def export(self, df, output_file):
        export_data(
            df=df,
            data_url_reference=self.data_url_reference,
            output_file=output_file
        )

    def run(self, output_file):
        # Load
        df = self.load_data()
        # Process
        df = self.process(df)
        # Export
        self.export(df, output_file)

    @property
    def filename(self):
        return self.country.title().replace(" ", "_")


class IncrementalScraper(Scraper):
    def export(self, df, output_file):
        df = self._merge_with_current_data(df, output_file)
        super().export(df, output_file)

    def _merge_with_current_data(self, df, filepath):
        # Load current data
        if os.path.isfile(filepath):
            df_current = pd.read_csv(filepath)
            # Merge
            key = df.loc[:, "region"].astype(str) + df.loc[:, "date"]
            df_current = df_current[~(df_current["region"].astype(str) + df_current["date"]).isin(key)]
            df = pd.concat([df, df_current])
        return df