import pandas as pd



def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Handle missing values
    df = df.fillna(method="ffill").fillna(0)

    # Remove duplicates
    df = df.drop_duplicates()

    # Fix column names (strip spaces, lowercase)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    return df
