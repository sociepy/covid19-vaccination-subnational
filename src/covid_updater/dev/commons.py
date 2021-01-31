import pandas as pd


def get_vaccination_metrics(total_vaccinations=None, people_vaccinated=None, people_fully_vaccinated=None):
    if total_vaccinations and people_vaccinated and not people_fully_vaccinated:
        people_fully_vaccinated = total_vaccinations - people_vaccinated
    elif total_vaccinations and not people_vaccinated and people_fully_vaccinated:
        people_vaccinated = total_vaccinations - people_fully_vaccinated
    elif not total_vaccinations and people_vaccinated and people_fully_vaccinated:
        total_vaccinations = people_vaccinated + people_fully_vaccinated
    return total_vaccinations, people_vaccinated, people_fully_vaccinated


class BatchUpdater:
    def __init__(self, url, country_name, country_iso, region_replace, date_format,
                date_field=None, region_field=None, 
                total_vaccinations_field=None, people_vaccinated=None, people_fully_vaccinated=None):
        self.url = url
        self.country_name = country_name
        self.country_iso = country_iso
        self.region_replace = region_replace
        self.date_format = date_format

        self.rename_columns = self._rename_columns(
            date_field, region_field, total_vaccinations_field, 
            people_vaccinated, people_fully_vaccinated
        )
        _ = self.rename_columns.pop(None)

    def from_csv(self):
        df = pd.read_csv(self.url)
        return df

    def process(self, df):
        # Rename columns
        df.rename(columns=self.rename_columns)
        # Add some columns
        df.loc[:, "location"] = self.country_name
        if self.region_replace:
            df.loc[:, "region"] = df.loc[:, "region"].replace(self.region_replace)
        # Edit dates
        df = self.process_date(df, self.date_format)
        # Add ISO codes
        df = merge_iso(df, country_iso=self.country_iso)

    def add_cols(self, df):
        # TODO
        if total_vaccinations and people_vaccinated and not people_fully_vaccinated:
            people_fully_vaccinated = total_vaccinations - people_vaccinated
        elif total_vaccinations and not people_vaccinated and people_fully_vaccinated:
            people_vaccinated = total_vaccinations - people_fully_vaccinated
        elif not total_vaccinations and people_vaccinated and people_fully_vaccinated:
            total_vaccinations = people_vaccinated + people_fully_vaccinated
        #return total_vaccinations, people_vaccinated, people_fully_vaccinated
        
        if "total_vaccinations" not in df:
            if "people"
        total_vaccinations, people_vaccinated, people_fully_vaccinated = get_vaccination_metrics(
            total_vaccinations=None,
            people_vaccinated=None,
            people_fully_vaccinated=None
        )

    def _rename_columns(self, date_field, region_field, total_vaccinations_field
             people_vaccinated, people_fully_vaccinated):
        rename = {
            date_field: "date",
            region_field: "region",
            total_vaccinations_field: "total_vaccinations",
            people_vaccinated: "people_vaccinated",
            people_fully_vaccinated: "people_fully_vaccinated"
        }
        _ = rename.pop(None)
        return rename

    def process_date(self, df, date_format):
        df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format=date_format)
        df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
        return df


    def export(self, output_file):
        # Reorder columns
        col_names = ["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]
        for col in ["people_vaccinated", "people_fully_vaccinated"]:
            if col in self.rename_columns.values():
                col_names.append(col)
        df = df[col_names]
        # Sort rows
        df = df.sort_values(by=["region", "date"])
        # Export
        df.to_csv(output_file, index=False)

