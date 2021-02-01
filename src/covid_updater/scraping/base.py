from covid_updater.iso import ISODB
from covid_updater.utils import export_data


class Scraper:
    def __init__(self, country, country_iso, data_url, data_url_reference, region_renaming, column_renaming):
        self.country = country
        self.country_iso = country_iso
        self.data_url = data_url
        self.data_url_reference = data_url_reference
        self.region_renaming = region_renaming
        self.column_renaming = column_renaming

    def load_data(self):
        raise NotImplementedError("Call child's method instead.")

    def _preprocess(self, df):
         # Rename column names
        df = df.rename(columns=self.column_renaming)

        # Add location info
        if "location" not in df.columns:
            df.loc[:, "location"] = self.country

        # Rename regions
        df.loc[:, "region"] = df.loc[:, "region"].replace(self.region_renaming)

        return df

    def _process(self, df):
        raise NotImplementedError("Call child's method instead!")

    def process(self, df):
        # Common preprocessing
        df = self._preprocess(df)

        # Country-specific processing
        df = self._process(df)

        # Add ISO codes
        df = ISODB().merge(df, country_iso=self.country_iso)

        return df

    def run(self, output_file):
        # Load
        df = self.load_data()
        # Process
        df = self.process(df)
        # Export
        export_data(
            df=df,
            data_url_reference=self.data_url_reference,
            output_file=output_file
        )

    @property
    def filename(self):
        return self.country.title().replace(" ", "_")