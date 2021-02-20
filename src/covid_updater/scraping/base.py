import os
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import keep_min_date, COLUMNS_ALL, COLUMNS_ORDER, COLUMNS_INT


class Scraper:
    def __init__(self, country, country_iso, data_url, data_url_reference, region_renaming=None, 
                 field_renaming=None, column_renaming=None, mode_iso_merge=None, do_cumsum_fields=None):
        self.country = country
        self.country_iso = country_iso
        self.data_url = data_url
        self.data_url_reference = data_url_reference
        self.region_renaming = region_renaming if region_renaming is not None else {}
        self.field_renaming = field_renaming if field_renaming is not None else {}
        self.column_renaming = column_renaming if column_renaming is not None else {}
        self.mode_iso_merge = mode_iso_merge if mode_iso_merge is not None else "region_iso"
        self.do_cumsum_fields = do_cumsum_fields if do_cumsum_fields is not None else []
        self.last_update = None
        self.second_dose = None

    def load_data(self):
        raise NotImplementedError("Call child's method instead.")

    def _preprocess(self, df):
         # Rename column names
        df = df.rename(columns=self.column_renaming)
        # Replace field values
        for field, renaming in self.field_renaming.items():
            df.loc[:, field] = df.loc[:, field].replace(renaming)

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
        cols = [col for col in COLUMNS_ALL if col in df.columns]
        df = df[cols]

        # Avoid repeating reports
        df = keep_min_date(df)

        # Ensure Int types
        count_cols = [col for col in COLUMNS_INT if col in cols]
        df[count_cols] = df[count_cols].astype("Int64").fillna(pd.NA)

        # Update class atributes
        self.last_update = df["date"].max()
        self.second_dose = int("people_fully_vaccinated" in df.columns)

        # Export
        df = df.sort_values(by=COLUMNS_ORDER)
        df.to_csv(output_file, index=False)

    def export_info(self, output_file):
        """Update or create source data file.
        
        This file specifies data for each country such as the URL of the source data, last update, etc.
        """
        if self.last_update is None or self.second_dose is None:
            raise AttributeError("Attributes last_update or second_dose are None! You may need to run `export`")
        # Load tracking file
        if os.path.isfile(output_file):
            df = pd.read_csv(output_file, index_col="country")
        else:
            df = pd.DataFrame()
            df.index.name = "country"
        # Update/Add country entry
        if self.country in df.index:
            df.loc[self.country, "data_source_url"] = self.data_url_reference
            df.loc[self.country, "last_update"] = self.last_update
            df.loc[self.country, "second_dose"] = self.second_dose
            df.loc[self.country, "country_iso"] = self.country_iso
        else:
            s = pd.Series(
                data=[self.country_iso, self.data_url_reference, self.last_update, self.second_dose],
                index=["country_iso", "data_source_url", "last_update", "second_dose"],
                name=self.country
            )
            df = df.append(s)
        df = df[["country_iso", "data_source_url", "last_update", "second_dose"]].astype({
            "second_dose": int
        })
        df.to_csv(output_file)

    def run(self, output_file_data, output_file_info=None):
        # Load
        try:
            df = self.load_data()
        except pd.errors.EmptyDataError:
            return 0
        # Process
        df = self.process(df)
        # Export country data
        self.export(df, output_file=output_file_data)
        # Export data info
        if output_file_info is not None:
            self.export_info(output_file=output_file_info)

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