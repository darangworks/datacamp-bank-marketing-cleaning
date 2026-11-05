"""Automated tests for the bank-marketing cleaning pipeline."""

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "clean_bank_marketing.py"
SPEC = importlib.util.spec_from_file_location("clean_bank_marketing", SCRIPT_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pipeline)


@pytest.fixture
def sample_source(tmp_path, monkeypatch):
    """Create a small, valid source dataset and isolate generated files."""
    source = pd.DataFrame(
        {
            "client_id": [101, 102, 103],
            "age": [34, 45, 29],
            "job": ["admin.", "blue-collar", "technician"],
            "marital": ["single", "married", "single"],
            "education": ["university.degree", "unknown", "high.school"],
            "credit_default": ["no", "yes", "no"],
            "mortgage": ["yes", "no", "no"],
            "number_contacts": [1, 2, 1],
            "contact_duration": [120, 80, 200],
            "previous_campaign_contacts": [0, 1, 2],
            "previous_outcome": ["nonexistent", "success", "failure"],
            "campaign_outcome": ["no", "yes", "no"],
            "month": ["may", "jun", "dec"],
            "day": [5, 16, 31],
            "cons_price_idx": [93.2, 94.1, 92.8],
            "euribor_three_months": [1.2, 1.4, 0.9],
        }
    )
    source.to_csv(tmp_path / "bank_marketing.csv", index=False)
    monkeypatch.chdir(tmp_path)
    return tmp_path, source


def test_pipeline_creates_expected_outputs(sample_source):
    folder, source = sample_source
    pipeline.main()

    client = pd.read_csv(folder / "client.csv")
    campaign = pd.read_csv(folder / "campaign.csv")
    economics = pd.read_csv(folder / "economics.csv")

    assert client.shape == (3, 7)
    assert campaign.shape == (3, 7)
    assert economics.shape == (3, 3)
    assert client.columns.tolist() == [
        "client_id", "age", "job", "marital", "education",
        "credit_default", "mortgage",
    ]
    assert campaign.columns.tolist() == [
        "client_id", "number_contacts", "contact_duration",
        "previous_campaign_contacts", "previous_outcome",
        "campaign_outcome", "last_contact_date",
    ]
    assert economics.columns.tolist() == [
        "client_id", "cons_price_idx", "euribor_three_months",
    ]
    assert client["client_id"].tolist() == source["client_id"].tolist()
    assert campaign["client_id"].tolist() == source["client_id"].tolist()
    assert economics["client_id"].tolist() == source["client_id"].tolist()


def test_categorical_boolean_and_date_conversions(sample_source):
    folder, _ = sample_source
    pipeline.main()

    client = pd.read_csv(folder / "client.csv")
    campaign = pd.read_csv(folder / "campaign.csv")

    assert client["job"].tolist()[0] == "admin_"
    assert pd.isna(client.loc[1, "education"])
    assert client["credit_default"].tolist() == [False, True, False]
    assert client["mortgage"].tolist() == [True, False, False]
    assert campaign["previous_outcome"].tolist() == [False, True, False]
    assert campaign["campaign_outcome"].tolist() == [False, True, False]
    assert campaign["last_contact_date"].tolist() == [
        "2022-05-05", "2022-06-16", "2022-12-31"
    ]


def test_missing_input_raises_clear_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="bank_marketing.csv"):
        pipeline.main()


def test_missing_required_column_raises_clear_error(tmp_path, monkeypatch):
    source = pd.DataFrame({"client_id": [1], "age": [25]})
    source.to_csv(tmp_path / "bank_marketing.csv", index=False)
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError, match="missing required columns"):
        pipeline.main()
