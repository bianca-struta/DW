import os
import json
from app import db_repository

def test_database_file_parsing_logic():
    """Validates that the formal repository layer abstraction parses data spaces safely."""
    data = db_repository.read_all_records()
    assert isinstance(data, dict)
    assert "financial_assets" in data
    assert "market_time_series" in data

def test_temporal_asset_integrity_rules():
    """Validates that asset structures within warehouse match baseline requirements."""
    source_file = "acme_dwh_nosql.json"
    if os.path.exists(source_file):
        with open(source_file, "r") as file:
            db_data = json.load(file)
            
        assets = db_data.get("financial_assets", [])
        for item in assets:
            assert "asset_id" in item
            assert "symbol" in item
            assert "provenance_provider" in item
            assert "valid_from" in item