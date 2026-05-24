import pandas as pd


def parse_dataset_dates(df, value_col=None):
    """
    Clean and standardize macroeconomic time-series datasets.
    Returns a DataFrame indexed by Date.
    """

    df = df.copy()
    df = df.dropna(how="all")

    # If Date is already the index
    if isinstance(df.index, pd.DatetimeIndex):
        df.index.name = "Date"

        if value_col is not None:
            df = df[[value_col]]

        return df.sort_index()

    # Detect date column
    date_keywords = ["date", "time", "period", "observation"]

    possible_date_cols = [
        col for col in df.columns
        if any(keyword in str(col).lower() for keyword in date_keywords)
    ]

    if possible_date_cols:
        date_col = possible_date_cols[0]
    else:
        date_col = df.columns[0]

    # Rename date column
    df = df.rename(columns={date_col: "Date"})

    # Convert dates robustly
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="mixed",
        errors="coerce",
        dayfirst=True
    )

    # Remove invalid dates
    df = df.dropna(subset=["Date"])

    # Select value column
    if value_col is None:
        value_cols = [col for col in df.columns if col != "Date"]

        if len(value_cols) == 0:
            raise ValueError("No value column found.")

        value_col = value_cols[0]

    # Keep only Date and selected value
    df = df[["Date", value_col]]

    # Clean final dataset
    df = df.drop_duplicates(subset=["Date"])
    df = df.sort_values("Date")
    df = df.set_index("Date")

    return df



# Print datasets heads

def print_datasets_head(*datasets, n=5):
    """
    Print the head of multiple pandas DataFrames.
    """

    for name, df in datasets:

        print("=" * 60)
        print(f"{name} - HEAD ({n} rows)")
        print("=" * 60)

        if df is None:
            print("Dataset is None.\n")
            continue

        try:
            print(df.head(n))

        except Exception as e:
            print(f"Error while displaying dataset: {e}")

        print("\n")