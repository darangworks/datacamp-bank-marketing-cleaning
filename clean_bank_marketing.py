"""Clean and split the DataCamp bank marketing campaign dataset.

Expected input:
    bank_marketing.csv

Generated outputs:
    client.csv
    campaign.csv
    economics.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILE = Path("bank_marketing.csv")


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE.resolve()}. "
            "Place bank_marketing.csv in the project directory and rerun."
        )

    bank_marketing = pd.read_csv(INPUT_FILE)

    required_columns = {
        "client_id", "age", "job", "marital", "education",
        "credit_default", "mortgage", "number_contacts",
        "contact_duration", "previous_campaign_contacts",
        "previous_outcome", "campaign_outcome", "month", "day",
        "cons_price_idx", "euribor_three_months",
    }
    missing_columns = required_columns.difference(bank_marketing.columns)
    if missing_columns:
        raise ValueError(
            "The input dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # 1. Client table
    client = bank_marketing[
        [
            "client_id", "age", "job", "marital", "education",
            "credit_default", "mortgage",
        ]
    ].copy()

    client["client_id"] = client["client_id"].astype("int64")
    client["age"] = client["age"].astype("int64")
    client["job"] = client["job"].str.replace(".", "_", regex=False)
    client["marital"] = client["marital"].astype("object")
    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", np.nan)
    )
    client["credit_default"] = client["credit_default"].eq("yes").astype(bool)
    client["mortgage"] = client["mortgage"].eq("yes").astype(bool)

    # 2. Campaign table
    campaign = bank_marketing[
        [
            "client_id", "number_contacts", "contact_duration",
            "previous_campaign_contacts", "previous_outcome",
            "campaign_outcome", "month", "day",
        ]
    ].copy()

    campaign["client_id"] = campaign["client_id"].astype("int64")
    for column in [
        "number_contacts", "contact_duration",
        "previous_campaign_contacts",
    ]:
        campaign[column] = campaign[column].astype("int64")

    campaign["previous_outcome"] = (
        campaign["previous_outcome"].eq("success").astype(bool)
    )
    campaign["campaign_outcome"] = (
        campaign["campaign_outcome"].eq("yes").astype(bool)
    )

    # The project specification assigns 2022 to all contact dates.
    campaign["year"] = 2022
    campaign["last_contact_date"] = pd.to_datetime(
        campaign["day"].astype(str)
        + "-"
        + campaign["month"].str.title()
        + "-"
        + campaign["year"].astype(str),
        format="%d-%b-%Y",
        errors="raise",
    )

    campaign = campaign[
        [
            "client_id", "number_contacts", "contact_duration",
            "previous_campaign_contacts", "previous_outcome",
            "campaign_outcome", "last_contact_date",
        ]
    ].copy()

    # 3. Economics table
    economics = bank_marketing[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].copy()

    economics["client_id"] = economics["client_id"].astype("int64")
    economics["cons_price_idx"] = economics["cons_price_idx"].astype("float64")
    economics["euribor_three_months"] = economics[
        "euribor_three_months"
    ].astype("float64")

    # 4. Validate schemas and row counts before writing files.
    expected_client_columns = [
        "client_id", "age", "job", "marital", "education",
        "credit_default", "mortgage",
    ]
    expected_campaign_columns = [
        "client_id", "number_contacts", "contact_duration",
        "previous_campaign_contacts", "previous_outcome",
        "campaign_outcome", "last_contact_date",
    ]
    expected_economics_columns = [
        "client_id", "cons_price_idx", "euribor_three_months",
    ]

    assert client.columns.tolist() == expected_client_columns
    assert campaign.columns.tolist() == expected_campaign_columns
    assert economics.columns.tolist() == expected_economics_columns
    assert len(client) == len(bank_marketing)
    assert len(campaign) == len(bank_marketing)
    assert len(economics) == len(bank_marketing)
    assert campaign["last_contact_date"].notna().all()

    client.to_csv("client.csv", index=False)
    campaign.to_csv(
        "campaign.csv", index=False, date_format="%Y-%m-%d"
    )
    economics.to_csv("economics.csv", index=False)

    print("Data cleaning and validation completed.")
    print(f"Source rows: {len(bank_marketing):,}")
    print(f"client.csv:   {client.shape}")
    print(f"campaign.csv: {campaign.shape}")
    print(f"economics.csv:{economics.shape}")
    print("\nClient data types:\n", client.dtypes)
    print("\nCampaign data types:\n", campaign.dtypes)
    print("\nEconomics data types:\n", economics.dtypes)


if __name__ == "__main__":
    main()
