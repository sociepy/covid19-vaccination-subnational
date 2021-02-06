"""To change:
- merge_iso -> merge
- load_iso -> as_df

"""
import os
import pandas as pd


this_directory = os.path.abspath(os.path.dirname(__file__))
ISO_ORIGINAL_FILE = os.path.join(this_directory, "assets/IP2LOCATION-ISO3166-2.CSV")
ISO_NEW_FILE = os.path.join(this_directory, "assets/ISO_3166_2.csv")


class ISODB():
    def __init__(self, filepath=ISO_NEW_FILE, df=None):
        self._file = filepath
        if isinstance(df, pd.DataFrame):
            self._df = df
        else:
            if os.path.isfile(self._file):
                self._df = pd.read_csv(self._file)
            else:
                raise Exception("DB file not created. Run `create_from_source` before.")

    @classmethod
    def create_from_source(cls, source_file=ISO_ORIGINAL_FILE, filepath=ISO_NEW_FILE):
        """Create ISO db.

        Uses IP2LOCATION-ISO3166-2 file.

        Args:
            source_file (str): Path to source file.

        """
        df = pd.read_csv(source_file)
        df = df.rename(columns={
            "country_code": "location_iso",
            "code": "region_iso"
        })
        df = df.sort_values(["location_iso", "region_iso"])
        df.to_csv(filepath, index=False)
        return cls(filepath=filepath, df=df)

    def append(self, items):
        new_items = pd.DataFrame(items, columns=["location_iso", "region_iso", "subdivision_name"])
        self._df = self._df.append(new_items, ignore_index=True)
        self._df = self._df.sort_values(["location_iso", "region_iso"])
        self._df.to_csv(self._file, index=False)

    def rename_values(self, colname, rename_dix):
        self._df.loc[:, colname] = self._df.loc[:, colname].replace(rename_dix)

    def merge(self, df, mode="region_iso", country_iso=None):
        """Merge input dataframe with ISO database.

        To get ISO codes, use `mode='region_iso'`. Use `mode='region'` to get region names.

        Args:
            df (pandas.DataFrame): ISO data.
            mode (str): Merge mode. Currently supports two modes ('region' or 'region_iso').
            country_iso (str): Country ISO code

        Returns:
            pandas.DataFrame: Joined table.
        """
        if mode == "region_iso" and country_iso is not None:
            df_iso_country = self._df[self._df["location_iso"]==country_iso]
            df = df.merge(df_iso_country, left_on="region", right_on="subdivision_name", how="left")
            df["region_iso"] = df[["region_iso"]].fillna("-")
            df = df.drop(columns=["subdivision_name"])
        elif mode == "region":
            df = df.merge(self._df, on="region_iso")
            df = df.rename(columns={
                "subdivision_name": "region"
            })
        else:
            raise ValueError(f"{mode} is not a  valid `mode` value. Choose either 'region_iso' or 'region'. If" + \
                            "'region_iso', make sure to set a value for `country_iso`.")
        return df
