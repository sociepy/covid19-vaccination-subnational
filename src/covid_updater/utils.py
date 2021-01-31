import pandas as pd


def keep_min_date(df):
    df = df.copy()
    cols = df.columns
    # Remove NaNs
    count_cols = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
    count_cols = [col for col in count_cols if col in cols]
    df.loc[:, count_cols] = df.loc[:, count_cols].fillna(-1).astype(int)
    # Goup by    
    df = df.groupby(
        by=[col for col in df.columns if col != "date"]
    ).min().reset_index()

    # Bring NaNs back
    df.loc[:, count_cols] = df.loc[:, count_cols].astype("Int64").replace({-1: pd.NA})
    return df.loc[:, cols]