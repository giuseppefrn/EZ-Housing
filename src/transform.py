import os

import pandas as pd


# Function to convert date strings to standardized date format
def convert_to_date(date_str):
    if (
        pd.isnull(date_str)
        or "In consultation" in date_str
        or "Immediately" in date_str
    ):
        return pd.NaT
    try:
        return pd.to_datetime(date_str, format="%d-%m-%Y").date()
    except ValueError:
        return pd.NaT


# Function to extract numeric values from strings
def extract_numeric(value_str):
    if pd.isnull(value_str):
        return pd.NA
    try:
        return float("".join(filter(str.isdigit, value_str)))
    except ValueError:
        return pd.NA


# Load the extracted data
houses_info_df = pd.read_csv("outputs/extracted/houses-info.csv")

# Apply conversions
houses_info_df["Offered since"] = houses_info_df["Offered since"].apply(
    convert_to_date
)  # noqa
houses_info_df["Available"] = houses_info_df["Available"].apply(
    lambda x: (
        convert_to_date(x.split("From ")[-1])
        if "From" in str(x)
        else convert_to_date(x)
    )
)
houses_info_df["Rental price"] = houses_info_df["Rental price"].apply(
    extract_numeric
)  # noqa
houses_info_df["Living area"] = houses_info_df["Living area"].apply(
    lambda x: extract_numeric(x.split(" ")[0])
)
houses_info_df["price"] = houses_info_df["price"].astype(float)
houses_info_df["Service costs"] = houses_info_df["Service costs"].apply(
    lambda x: extract_numeric(x.split("€")[-1]) if pd.notnull(x) else pd.NA
)
houses_info_df["Deposit"] = houses_info_df["Deposit"].apply(
    lambda x: extract_numeric(x.split("€")[-1]) if pd.notnull(x) else pd.NA
)

# Save the transformed data

# Create a folder for the transformed data
output_dir = "outputs/transformed"
os.makedirs(output_dir, exist_ok=True)
houses_info_df.to_csv(
    "outputs/transformed/houses-info-transformed.csv", index=False
)  # noqa
