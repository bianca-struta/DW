import json

def run_spark_simulation():
    print("starting mock spark engine analysis process:")
    
    try:
        with open("acme_dwh_nosql.json", "r") as f:
            db = json.load(f)
    except:
        print("error loading json db file")
        return
        
    ts_data = db.get("market_time_series", [])
    print("loaded records count from nosql storage:", len(ts_data))
    
    print("running basic aggregations (min, max, average) for mining:")
    for row in ts_data:
        sym = row.get("symbol")
        src = row.get("data_source_id")
        metrics = row.get("metrics", {})
        
        h = metrics.get("high", 0)
        l = metrics.get("low", 0)
        c = metrics.get("close", 0)
        
        avg = (h + l) / 2
        forecast = c * 1.015
        
        print("Symbol: " + str(sym) + " | Source: " + str(src))
        print("  Calculated Avg: " + str(avg) + " | Min: " + str(l) + " | Max: " + str(h))
        print("  Basic simple forecast price: " + str(round(forecast, 2)))

if __name__ == "__main__":
    run_spark_simulation()