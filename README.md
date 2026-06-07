# Financial Market Enterprise Data Warehouse (Acme Ltd)

This project implements a Data Warehouse platform for Acme Ltd, designed to collect, store, explore, and analyze heterogeneous financial market data while preserving historical versions and data provenance.

## System Architecture Diagram

**Project Demo Video**

[Demo video: ](https://drive.google.com/file/d/1TI9JnjFRd8i3Ig05C-jBrSrx1ZzBZFvx/view?usp=sharing)

```text
+--------------------------------------------------------------------------+
|                       Model Context Protocol (MCP)                        |
|                      [ mcp_server.py (LLM Tools) ]                        |
+------------------------------------+-------------------------------------+
                                     |
                                     | (Grounded Context)
                                     v
+--------------------------------------------------------------------------+
|                           Presentation Layer                             |
|                    [ app.py (FastAPI REST Engine) ]                       |
+------------------------------------+-------------------------------------+
                                     |
                                     | (Repository Boundary)
                                     v
+--------------------------------------------------------------------------+
|                         Data Access Layer (DAL)                           |
|              [ LocalNoSQLRepository Class Abstraction ]                   |
+---------------------+-------------------------------+---------------------+
                      |                               |
                      v                               v
+--------------------------------------+  +--------------------------------+
|      Big Data & Analytics Engine     |  |          Storage Layer         |
| [ spark_analytics.py (ML Pipeline) ] |  |     [ acme_dwh_nosql.json ]    |
+--------------------------------------+  +--------------------------------+
```

## Architecture Overview

### Storage Layer
The platform uses a document-oriented NoSQL storage model implemented through a native JSON engine (`acme_dwh_nosql.json`). The design supports heterogeneous financial assets, allowing different asset classes to expose different attributes. Cryptocurrencies may contain blockchain-specific information, stocks may include exchange or market sector information, while other asset types expose their own properties. This approach makes the system easily extensible for future financial instruments.

### Temporal Data Management
The platform follows a temporal database approach based on immutable records. Existing records are never overwritten, updates generate new versions of the same entity, and historical states remain available. Logical deletion is represented through marker records with validity timestamps. This approach enables historical reconstruction and guarantees data consistency over time.

### Data Ingestion and Provenance
The origin of each dataset is tracked through dedicated metadata fields such as `provenance_provider` and `data_source_id`. Supported providers include Nasdaq and Bloomberg. Provenance information allows complete traceability of imported financial records.

## Project Structure

### db_ingest.py
Populates the database with financial instruments, providers, and historical time-series records.

### app.py
Implements the FastAPI server while abstracting database operations under a formal Data Access Layer (DAL) repository pattern.

### spark_analytics.py
Runs automated data aggregations and analytical workloads using Apache Spark DataFrames and simple machine learning forecasting models.

### test_warehouse.py
Contains isolated unit tests validating parser components and temporal data integrity rules.

### mcp_server.py
Implements the Model Context Protocol layer used by the LLM assistant to access platform capabilities as tools.

## REST API Specification

### Asset Discovery
* `GET /api/assets` – Returns all active financial assets stored in the warehouse. Supports `limit` and `offset` pagination parameters.
* `GET /api/assets/{symbol}` – Returns complete metadata for a specific asset using consistent schemas.

### Provider Discovery
* `GET /api/sources` – Lists available financial data providers with pagination support.
* `GET /api/sources/{source_id}` – Returns information about a specific provider.

### Time-Series Data
* `GET /api/timeseries/{symbol}/{source_id}` – Returns historical market data and supports optional `start_date` and `end_date` filters.

## Analytics Endpoints
* `GET /api/analytics/compare` – Performs side-by-side comparisons between heterogeneous financial instruments.
* `GET /api/analytics/trends/{symbol}` – Computes minimum values, maximum values, averages, moving averages, trend indicators, and predictive estimates generated from the Spark pipeline.
* `GET /api/analytics/explain/{symbol}` – Explains temporal changes, version history, and tracking information recorded for an asset.

## LLM Assistant via MCP
The platform exposes its capabilities through MCP tools that can be consumed by an LLM assistant. Supported operations include listing assets, retrieving time-series data, summarizing trends, comparing assets, and explaining historical changes. All answers are grounded in platform data rather than generic financial knowledge.

## Installation
Install the required dependencies:

```bash
pip install fastapi uvicorn pydantic pyspark numpy pytest
```

## Running the Project

### 1. Populate the Database
Run the ingestion script to seed the data warehouse:

```bash
py db_ingest.py
```

### 2. Execute Unit Tests
Validate parser components and temporal constraints:

```bash
py -m pytest test_warehouse.py
```

### 3. Execute Analytics Pipelines
Run Apache Spark analytical workloads and forecasting procedures:

```bash
py spark_analytics.py
```

### 4. Start the REST API Server
Launch the FastAPI application:

```bash
py -m uvicorn app:app --reload
```

### 5. Run the MCP Assistant Layer
Start the Model Context Protocol server:

```bash
py mcp_server.py
```

## Main Platform Features
* NoSQL data warehouse architecture
* Structured heterogeneous asset schemas
* Data Access Layer repository abstraction
* Temporal database versioning support
* Immutable close-and-append update strategy
* Data provenance tracking
* Pagination and range-filtering support
* Apache Spark analytical processing
* Machine learning forecasting workflows
* Grounded LLM integration through Model Context Protocol
* Modular architecture suitable for future extensions
