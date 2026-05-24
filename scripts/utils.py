import pandas as pd

def parse_dataset_dates(df, value_col=None, date_format=None):
    df = df.copy()
    df = df.dropna(how="all")

    # If Date is already in index
    if isinstance(df.index, pd.DatetimeIndex):
        df.index.name = "Date"
        if value_col is not None:
            df = df[[value_col]]
        return df.sort_index()

    # Find date column automatically
    possible_date_cols = [
        col for col in df.columns
        if any(word in str(col).lower() for word in ["date", "time", "period", "observation"])
    ]

    # If no date-like name, try first column as date
    if len(possible_date_cols) == 0:
        first_col = df.columns[0]
        test_dates = pd.to_datetime(
            df[first_col],
            format=date_format,
            errors="coerce"
        )

        if test_dates.notna().sum() > 0:
            date_col = first_col
        else:
            raise ValueError("No date column found.")
    else:
        date_col = possible_date_cols[0]

    # Rename date column first
    df = df.rename(columns={date_col: "Date"})

    # Convert Date column
    df["Date"] = pd.to_datetime(
        df["Date"],
        format=date_format,
        errors="coerce"
    )

    # Choose value column
    if value_col is None:
        other_cols = [col for col in df.columns if col != "Date"]
        value_col = other_cols[0]

    df = df[["Date", value_col]]

    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date")
    df = df.drop_duplicates(subset=["Date"])
    df = df.set_index("Date")

    return df