import datetime
from app import db_repository

def load_db():
    return db_repository.read_all_records()

def save_db(data):
    db_repository.write_all_records(data)

def ingest_or_update_asset(symbol, asset_class, description, region, provider, extra_attrs=None):
    db = load_db()
    current_time = datetime.datetime.now().isoformat()
    symbol = symbol.upper()
    
    # Check if active asset version exists to close it out temporally
    for asset in db["financial_assets"]:
        if asset["symbol"] == symbol and asset["valid_to"] is None:
            asset["valid_to"] = current_time

    new_asset = {
        "asset_id": f"asset_{len(db['financial_assets']) + 1}",
        "symbol": symbol,
        "asset_class": asset_class.lower(),
        "description": description,
        "region": region,
        "provenance_provider": provider,
        "valid_from": current_time,
        "valid_to": None,
        "is_deleted": False
    }

    if extra_attrs:
        new_asset.update(extra_attrs)

    db["financial_assets"].append(new_asset)
    save_db(db)
    print(f"[Ingestion Layer] Successfully stored asset configuration for: {symbol}")

def ingest_time_series_point(symbol, provider, metrics_dict):
    db = load_db()
    current_time = datetime.datetime.now().isoformat()
    
    new_point = {
        "time_series_id": f"ts_{len(db['market_time_series']) + 1}",
        "symbol": symbol.upper(),
        "data_source_id": provider,
        "timestamp": current_time,
        "metrics": metrics_dict
    }
    
    db["market_time_series"].append(new_point)
    save_db(db)
    print(f"[Ingestion Layer] Logged historical time-series metric entry for: {symbol.upper()}")

def delete_asset_temporal(symbol):
    db = load_db()
    current_time = datetime.datetime.now().isoformat()
    symbol = symbol.upper()
    
    # Close current active track timeline
    for asset in db["financial_assets"]:
        if asset["symbol"] == symbol and asset["valid_to"] is None:
            asset["valid_to"] = current_time
            
            deleted_marker = asset.copy()
            deleted_marker["asset_id"] = f"asset_{len(db['financial_assets']) + 1}"
            deleted_marker["valid_from"] = current_time
            deleted_marker["valid_to"] = None
            deleted_marker["is_deleted"] = True
            
            db["financial_assets"].append(deleted_marker)
            save_db(db)
            print(f"[Temporal Layer] Registered soft-deletion state for target asset: {symbol}")
            return
            
    print(f"[Warning] Asset {symbol} not active. Mutation skipped.")

if __name__ == "__main__":
    # Seed financial dataset configuration baseline
    ingest_or_update_asset("BTC", "crypto", "Bitcoin", "Global", "CoinGecko", {"circulating_supply": 19600000})
    ingest_or_update_asset("TSLA", "stock", "Tesla Inc", "US", "Nasdaq", {"market_cap": 950000000000})
    ingest_or_update_asset("NFLX", "stock", "Netflix Inc", "US", "Bloomberg", {"pe_ratio": 42.5})
    
    # Seed historical price feeds compliance sequences
    ingest_time_series_point("BTC", "CoinGecko", {"open": 64000.0, "high": 65000.0, "low": 63500.0, "close": 64800.0})
    ingest_time_series_point("TSLA", "Nasdaq", {"open": 330.0, "high": 345.0, "low": 328.0, "close": 343.0})
    ingest_time_series_point("TSLA", "Nasdaq", {"open": 340.0, "high": 342.0, "low": 325.0, "close": 330.0})