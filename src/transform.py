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


if __name__ == "__main__":
    # get the root folder of the project
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Load the extracted data
    houses_info_df = pd.read_csv(
        os.path.join(root_folder, "outputs/extracted/houses-info.csv")
    )

    mandatory_columns = {
        "Available": {"type": "date"},
        "Deposit": {"type": "float"},
        "Living area": {"type": "float"},
        "Offered since": {"type": "date"},
        "price": {"type": "float"},
        "Rental price": {"type": "float"},
        "Service costs": {"type": "float"},
    }

    # Add missing columns
    for col in mandatory_columns:
        if col not in houses_info_df.columns:
            houses_info_df[col] = pd.NA

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
    output_dir = os.path.join(root_folder, "outputs/transformed")
    os.makedirs(output_dir, exist_ok=True)
    houses_info_df.to_csv(
        os.path.join(output_dir, "houses-info-transformed.csv"), index=False
    )  # noqa
