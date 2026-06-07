import os
import json
from app import read_warehouse_storage

def test_database_file_parsing_logic():
    """Validates that the storage data reader layer parses components cleanly."""
    data = read_warehouse_storage()
    # Check that the data returned is valid 
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
            # Verify that the core NoSQL and temporal keys exist
            assert "asset_id" in item
            assert "symbol" in item
            assert "provenance_provider" in item
            assert "valid_from" in item