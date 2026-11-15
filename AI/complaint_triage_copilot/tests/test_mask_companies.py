"""Tests for masking firm and brand names in narratives."""

import pandas as pd
import pytest

from src.copilot.data.mask_companies import load_company_terms, mask_companies

TERMS = pd.DataFrame(
    {
        "term": ["Bank of America", "Citibank", "Citi", "JPMorgan Chase", "Chase", "Cash App", "CashApp", "Affirm"],
        "case_sensitive": [False, False, False, False, True, False, False, True],
    }
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("I complained to Bank of America about Zelle.", "I complained to [COMPANY] about Zelle."),
        ("Citibank and citi both refused.", "[COMPANY] and [COMPANY] both refused."),
        ("Chase closed my account.", "[COMPANY] closed my account."),
        ("I had to chase them for weeks.", "I had to chase them for weeks."),
        ("JPMorgan Chase refused a refund.", "[COMPANY] refused a refund."),
        ("Money sent with Cash App and cashapp.", "Money sent with [COMPANY] and [COMPANY]."),
        ("They affirmed the charge was valid.", "They affirmed the charge was valid."),
        ("The Visa charge went through Zelle.", "The Visa charge went through Zelle."),
    ],
)
def test_mask_companies(raw, expected):
    assert mask_companies(pd.Series([raw]), TERMS).iloc[0] == expected


def test_adjacent_names_collapse_to_one_placeholder():
    assert mask_companies(pd.Series(["Citi Citibank"]), TERMS).iloc[0] == "[COMPANY]"


def test_config_file_loads():
    terms = load_company_terms()
    assert {"term", "case_sensitive"} <= set(terms.columns)
    assert terms["term"].str.len().gt(0).all()
    assert terms["case_sensitive"].dtype == bool