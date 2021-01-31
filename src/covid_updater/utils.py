def keep_min_date(df):
    cols = df.columns
    df = df.groupby(
        by=[col for col in df.columns if col != "date"]
    ).min().reset_index()
    return df[cols]