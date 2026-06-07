import json
from app import get_active_assets, get_historical_time_series, get_asset_comparison, get_trend_summarization, explain_temporal_change

class ModelContextProtocolServer:
    def __init__(self):
        # register available tools for the assistant mapping the backend functions
        self.registered_tools = {
            "list_assets": "Retrieves active financial assets logged in the warehouse.",
            "fetch_time_series": "Retrieves historical time series points for an asset.",
            "compare_two_assets": "Executes side-by-side mapping of two distinct instruments.",
            "summarize_trends": "Runs arithmetic routines to parse market trends and averages.",
            "explain_a_change": "Analyzes and explains historical version modifications."
        }

    def execute_llm_tool_call(self, tool_name, arguments=None):
        args = arguments if arguments is not None else {}
        print(f"[MCP Layer] Assistant triggered tool '{tool_name}' with args: {args}")
        
        if tool_name == "list_assets":
            return {"status": "success", "data": get_active_assets()}
        elif tool_name == "fetch_time_series":
            sym = args.get("symbol", "BTC")
            src = args.get("source", "CoinGecko")
            return {"status": "success", "data": get_historical_time_series(sym, src)}
        elif tool_name == "compare_two_assets":
            s1 = args.get("symbol1", "BTC")
            s2 = args.get("symbol2", "TSLA")
            return {"status": "success", "data": get_asset_comparison(s1, s2)}
        elif tool_name == "summarize_trends":
            sym = args.get("symbol", "BTC")
            return {"status": "success", "data": get_trend_summarization(sym)}
        elif tool_name == "explain_a_change":
            sym = args.get("symbol", "TSLA")
            return {"status": "success", "data": explain_temporal_change(sym)}
        else:
            return {"status": "error", "message": f"Tool '{tool_name}' not recognized."}

    def run_automated_portfolio_analysis(self, symbol):
        """Helper process to execute a multi-step verification pipeline for a specific asset."""
        print(f"\n Starting multi-step analysis sequence for: {symbol} ")
        
        print("Step 1: Validating if asset is active")
        assets = get_active_assets()
        
        print("Step 2: Retrieving data rows from database history")
        provider_name = "Nasdaq" if symbol == "TSLA" else "CoinGecko"
        series = get_historical_time_series(symbol, provider_name)
        
        print("Step 3: Calculating statistical averages and trend thresholds")
        trends = get_trend_summarization(symbol)
        
        print("Step 4: Consolidating final output format")
        return {
            "status": "COMPLETED",
            "pipeline_steps": ["check_active_catalog", "fetch_time_series_logs", "compute_metrics"],
            "analysis_summary": {
                "asset_target": symbol,
                "moving_average": trends["aggregations"]["midpoint_moving_average"],
                "next_day_estimate": trends["predictive_signals"]["next_day_forecast"]
            }
        }

if __name__ == "__main__":
    mcp_instance = ModelContextProtocolServer()
    
    # testing execution flows 
    print("Testing Tool: compare_two_assets")
    res1 = mcp_instance.execute_llm_tool_call("compare_two_assets", {"symbol1": "BTC", "symbol2": "TSLA"})
    print("Response:", res1)
    
    print("\n Testing Tool: explain_a_change")
    res2 = mcp_instance.execute_llm_tool_call("explain_a_change", {"symbol": "TSLA"})
    print("Response:", res2)
    
    # testing the integrated custom analytical flow
    pipeline_report = mcp_instance.run_automated_portfolio_analysis("TSLA")
    print("\nFinal Pipeline Report JSON:")
    print(json.dumps(pipeline_report, indent=2))