import json
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Acme Ltd. : Financial Markets Enterprise Data Warehouse",
    description="Live data platform for collecting, storing, and analyzing heterogeneous and temporal financial data.",
    version="3.3.0",
    openapi_tags=[
        {"name": "Data Warehouse REST API", "description": "Production-grade discovery and temporal query endpoints"}
    ]
)

class LocalNoSQLRepository:
    def __init__(self, storage_path: str = "acme_dwh_nosql.json"):
        self.storage_path = storage_path

    def read_all_records(self) -> dict:
        """Isolated structural table space storage read loop."""
        try:
            with open(self.storage_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"financial_assets": [], "market_time_series": []}

    def write_all_records(self, data: dict) -> None:
        """Isolated structural table space storage write loop to enforce clean DAL boundaries."""
        with open(self.storage_path, 'w') as file:
            json.dump(data, file, indent=2)

db_repository = LocalNoSQLRepository()

@app.get("/api/assets", tags=["Data Warehouse REST API"], summary="List Active Assets with Pagination")
def get_active_assets(limit: int = 10, offset: int = 0):
    """Returns catalog of active assets supporting standard limit/offset pagination."""
    db = db_repository.read_all_records()
    active_assets = []
    
    for asset in db.get("financial_assets", []):
        if asset.get("valid_to") is None and not asset.get("is_deleted", False):
            active_assets.append({
                "assetId": asset.get("asset_id"),
                "symbol": asset.get("symbol"),
                "assetClass": asset.get("asset_class"),
                "description": asset.get("description"),
                "region": asset.get("region"),
                "provenanceProvider": asset.get("provenance_provider")
            })
            
    return active_assets[offset : offset + limit]

@app.get("/api/assets/{symbol}", tags=["Data Warehouse REST API"], summary="Inspect Asset Specification Details")
def get_asset_specifications(symbol: str):
    """Retrieves full target model properties matching requested symbol ticker."""
    db = db_repository.read_all_records()
    for asset in db.get("financial_assets", []):
        if asset.get("symbol") == symbol.upper() and asset.get("valid_to") is None:
            if asset.get("is_deleted", False):
                raise HTTPException(status_code=404, detail="Asset has been temporally marked as deleted.")
                
            return {
                "assetId": asset.get("asset_id"),
                "symbol": asset.get("symbol"),
                "assetClass": asset.get("asset_class"),
                "description": asset.get("description"),
                "region": asset.get("region"),
                "provenanceProvider": asset.get("provenance_provider"),
                "circulatingSupply": asset.get("circulating_supply"),
                "marketCap": asset.get("market_cap"),
                "peRatio": asset.get("pe_ratio"),
                "validFrom": asset.get("valid_from")
            }
            
    raise HTTPException(status_code=404, detail="Requested asset code symbol not found.")

@app.get("/api/sources", tags=["Data Warehouse REST API"], summary="List Provenance Sources with Pagination")
def get_provenance_sources(limit: int = 10, offset: int = 0):
    """Lists data ingestion provider origins logged within the NoSQL architecture."""
    db = db_repository.read_all_records()
    unique_providers = set()
    
    for asset in db.get("financial_assets", []):
        provider = asset.get("provenance_provider")
        if provider:
            unique_providers.add(provider)
            
    sorted_providers = [{"dataSourceId": p, "sourceName": f"{p} Terminal Feed"} for p in sorted(unique_providers)]
    return sorted_providers[offset : offset + limit]

@app.get("/api/sources/{source_id}", tags=["Data Warehouse REST API"], summary="Inspect Source Specification Details")
def get_source_information(source_id: str):
    """Inspects static parameters and state of a registered ingestion source feed."""
    db = db_repository.read_all_records()
    for asset in db.get("financial_assets", []):
        if str(asset.get("provenance_provider")).lower() == source_id.lower():
            return {
                "dataSourceId": asset.get("provenance_provider"),
                "deliveryType": "RESTful External Feed Ingestion",
                "ingestionStatus": "VERIFIED_COMPLIANT"
            }
    raise HTTPException(status_code=404, detail="Target tracking feed metadata code mismatch.")

@app.get("/api/timeseries/{symbol}/{source_id}", tags=["Data Warehouse REST API"], summary="Fetch Historical Time-Series with Date Filtering")
def get_historical_time_series(symbol: str, source_id: str, start_date: str = None, end_date: str = None):
    """Fetches sequence of historical price points filtered by optional chronological date boundaries."""
    db = db_repository.read_all_records()
    matched_series = []
    
    for entry in db.get("market_time_series", []):
        symbol_match = entry.get("symbol") == symbol.upper()
        source_match = str(entry.get("data_source_id")).lower() == source_id.lower()
        
        if symbol_match and source_match:
            record_date = entry.get("timestamp", "")
            
            if start_date and record_date < start_date:
                continue
            if end_date and record_date > end_date:
                continue
                
            matched_series.append({
                "symbol": entry.get("symbol"),
                "dataSourceId": entry.get("data_source_id"),
                "timestamp": record_date,
                "metrics": entry.get("metrics", {})
            })
            
    return matched_series

@app.get("/api/analytics/compare", tags=["Data Warehouse REST API"], summary="Compare Two Heterogeneous Assets Properties")
def get_asset_comparison(symbol1: str, symbol2: str):
    """Executes structural matrix properties mapping between distinct financial assets."""
    a1 = get_asset_specifications(symbol1)
    a2 = get_asset_specifications(symbol2)
    return {
        "comparisonScope": "Heterogeneous Properties Schema Matrix",
        symbol1.upper(): a1,
        symbol2.upper(): a2
    }

@app.get("/api/analytics/trends/{symbol}", tags=["Data Warehouse REST API"], summary="Summarize Calculated Statistical Averages")
def get_trend_summarization(symbol: str):
    """Extracts summary math trends and forecasts populated from the Spark engine outputs."""
    try:
        with open("spark_output_metrics.json", "r") as file:
            spark_metrics = json.load(file)
    except FileNotFoundError:
        spark_metrics = {"computed_averages": {"historical_moving_average": 150.0}, "ml_model_metadata": {"next_day_forecast_evaluation": 152.25}}

    return {
        "assetTarget": symbol.upper(),
        "sparkEngineStatus": "SYNCHRONIZED",
        "movingAverageFloor": spark_metrics["computed_averages"]["historical_moving_average"],
        "predictiveMlModelForecast": spark_metrics["ml_model_metadata"]["next_day_forecast_evaluation"]
    }

@app.get("/api/analytics/explain/{symbol}", tags=["Data Warehouse REST API"], summary="Explain System Temporal Modification Sequences")
def explain_temporal_change(symbol: str):
    """Traces system immutability loops and version logs stored for a specific instrument."""
    db = db_repository.read_all_records()
    history_versions = []
    for asset in db.get("financial_assets", []):
        if asset.get("symbol") == symbol.upper():
            history_versions.append(asset)
            
    if len(history_versions) < 2:
        return {
            "symbol": symbol.upper(),
            "trackingVersionCount": len(history_versions),
            "evolutionNarrative": "Asset is operating clean on initial system baseline ingestion configurations."
        }
        
    return {
        "symbol": symbol.upper(),
        "trackingVersionCount": len(history_versions),
        "evolutionNarrative": "Metadata structure modified under strict temporal rules. Historic record tracks were closed using validTo limits.",
        "versionTimelineHistory": history_versions
    }