import datetime
import json
import os

# quick check if file exists, if not make it empty list
if not os.path.exists('acme_dwh_nosql.json'):
    with open('acme_dwh_nosql.json', 'w') as f:
        json.dump({"financial_assets": [], "market_time_series": []}, f)

def load_db():
    with open('acme_dwh_nosql.json', 'r') as f:
        return json.load(f)

def save_db(data):
    with open('acme_dwh_nosql.json', 'w') as f:
        json.dump(data, f, indent=2)

def ingest_or_update_asset(symbol, asset_class, description, region, provider, extra_attrs=None):
    if extra_attrs is None:
        extra_attrs = {}
    
    db_data = load_db()
    assets = db_data["financial_assets"]
    now = datetime.datetime.utcnow().isoformat()
    
    # temporal logic: close old version if symbol matches
    for item in assets:
        if item.get("symbol") == symbol.upper() and item.get("valid_to") is None:
            item["valid_to"] = now
            
    # build the new record
    new_rec = {
        "asset_id": "asset_" + str(len(assets) + 1),
        "symbol": symbol.upper(),
        "asset_class": asset_class,
        "description": description,
        "region": region,
        "provenance_provider": provider,
        "valid_from": now,
        "valid_to": None,
        "is_deleted": False
    }
    
    # merge extra fields for heterogeneity
    for k, v in extra_attrs.items():
        new_rec[k] = v
        
    assets.append(new_rec)
    db_data["financial_assets"] = assets
    save_db(db_data)

def delete_asset_temporal(symbol):
    db_data = load_db()
    assets = db_data["financial_assets"]
    now = datetime.datetime.utcnow().isoformat()
    
    for item in assets:
        if item.get("symbol") == symbol.upper() and item.get("valid_to") is None:
            item["valid_to"] = now
            
    marker = {
        "symbol": symbol.upper(),
        "valid_from": now,
        "valid_to": None,
        "is_deleted": True
    }
    assets.append(marker)
    db_data["financial_assets"] = assets
    save_db(db_data)

def ingest_time_series_point(symbol, source_id, timestamp, metrics):
    db_data = load_db()
    ts = db_data["market_time_series"]
    
    new_pt = {
        "symbol": symbol.upper(),
        "data_source_id": source_id,
        "timestamp": timestamp,
        "metrics": metrics
    }
    ts.append(new_pt)
    db_data["market_time_series"] = ts
    save_db(db_data)

if __name__ == "__main__":
    # reset db for fresh start
    init_data = {"financial_assets": [], "market_time_series": []}
    save_db(init_data)
    
    print("populating database with fake data...")
    ingest_or_update_asset("BTC", "crypto", "Bitcoin", "Global", "CoinGecko", {"circulating_supply": 19600000})
    ingest_or_update_asset("TSLA", "stock", "Tesla Inc", "US", "Nasdaq", {"market_cap": 950000000000})
    ingest_or_update_asset("NFLX", "stock", "Netflix Inc", "US", "Bloomberg", {"pe_ratio": 35.4})
    
    ingest_time_series_point("BTC", "CoinGecko", "2026-06-07T00:00:00", {"open": 105000, "high": 106500, "low": 104000, "close": 106000})
    ingest_time_series_point("TSLA", "Nasdaq", "2026-06-07T00:00:00", {"open": 335.0, "high": 339.0, "low": 334.0, "close": 337.80})
    print("done ingest.")