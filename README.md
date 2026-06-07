# Financial Market Enterprise Data Warehouse (Acme Ltd)

This project implements a Data Warehouse platform for **Acme Ltd**, designed to collect, store, explore, and analyze heterogeneous financial market data while preserving historical versions and data provenance.

# Architecture Overview
## Storage Layer

The platform uses a document-oriented NoSQL storage model implemented through a native JSON engine (`acme_dwh_nosql.json`).
The design supports heterogeneous financial assets, allowing different asset classes to expose different attributes:

* Cryptocurrencies (blockchain, circulating supply, etc.)
* Stocks (exchange, sector, market capitalization, etc.)
* Commodities and other instruments

This approach makes the system easily extensible for future asset types.

## Temporal Data Management

The platform follows a temporal database approach based on immutable records.
* Existing records are never overwritten.
* Updates generate new versions of the same entity.
* Historical states remain available.
* Logical deletion is represented through marker records with validity timestamps.
This enables historical reconstruction and guarantees consistent data over time.

## Data Ingestion and Provenance

The origin of each dataset is tracked through dedicated metadata fields:
* `provenance_provider`
* `data_source_id`
Supported providers include:
* Nasdaq
* Bloomberg
Data provenance information allows complete traceability of imported financial records.

# Project Structure

### `db_ingest.py`
Populates the database with financial instruments, providers, and historical time-series records.

### `app.py`
Implements the FastAPI server and exposes REST endpoints for data exploration and analytics.

### `spark_analytics.py`
Runs data aggregation and simple analytical workloads, including:
* minimum price
* maximum price
* average price
* moving averages
* basic trend detection
* simple next-day forecasts

### `mcp_server.py`
Implements the Model Context Protocol (MCP) layer used by the LLM assistant to access platform capabilities as tools.

# REST API

## Asset Discovery
### GET `/api/assets`
Returns all active financial assets stored in the warehouse.

### GET `/api/assets/{symbol}`
Returns complete metadata for a specific asset.

## Provider Discovery
### GET `/api/sources`
Lists available financial data providers.

### GET `/api/sources/{source_id}`
Returns information about a particular provider.

## Time-Series Data
### GET `/api/timeseries/{symbol}/{source_id}`
Returns historical market data for the selected asset and provider.

# Analytics Endpoints
### GET `/api/analytics/compare`
Performs side-by-side comparison between two assets.

Examples:
* BTC vs ETH
* TSLA vs MSFT

### GET `/api/analytics/trends/{symbol}`
Computes:
* minimum price
* maximum price
* average price
* moving average
* trend indicators
* simple forecast values

### GET `/api/analytics/explain/{symbol}`
Explains temporal changes and historical versions recorded for the asset.

# LLM Assistant via MCP
The platform exposes its capabilities through MCP tools that can be consumed by an LLM assistant.
Supported operations include:
* list assets
* retrieve time-series data
* summarize trends
* compare assets
* explain historical changes
All answers are grounded in platform data rather than generic financial knowledge.

# Installation
Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

# Running the Project

## 1. Populate the database

```bash
py db_ingest.py
```

## 2. Start the REST API

```bash
py -m uvicorn app:app --reload
```
Swagger documentation is available at:

```
http://127.0.0.1:8000/docs
```

## 3. Execute analytics workloads

```bash
py spark_analytics.py
```

## 4. Run the MCP assistant layer

```bash
py mcp_server.py
```

# Main Features
* NoSQL data warehouse architecture
* Heterogeneous asset model
* Historical time-series storage
* Temporal database support
* Immutable records
* Data provenance tracking
* REST API for data exploration
* Analytics and trend analysis
* Asset comparison capabilities
* LLM integration through MCP
* Extensible architecture suitable for future development