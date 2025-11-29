import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', port=8123)

def get_inference_data(symbol, limit=1):
    print(f"Fetching last {limit} aligned rows for {symbol}...")
    
    query = f"""
    SELECT
        t.timestamp, 
        t.close, 
        t.sigma_forecast, 
        t.arma_forecast,
        t.ema_trend_filter_trend_up, 
        t.ema_trend_filter_trend_down,
        t.long_term_bias_trend_up, 
        t.long_term_bias_trend_down,
        t.macd_signal, 
        t.bb_signal, 
        t.risk_adj_ret,
        t.long_signal, 
        t.short_signal, 
        t.rsi_timing,
        s.sentiment_score, 
        s.news_title
    FROM technical_metrics t
    ASOF JOIN sentiment_stream s 
        ON t.symbol = s.symbol AND t.timestamp >= s.timestamp
    WHERE t.symbol = '{symbol}'
    ORDER BY t.timestamp DESC
    LIMIT {limit} 
    """
    
    return client.query_df(query)

if __name__ == "__main__":
    # Example 1: Get ONLY the latest row (For XGBoost Inference)
    latest = get_inference_data('AAPL', limit=1)
    print(latest)

    # Example 2: Get history (For Analysis/Training)
    history = get_inference_data('AAPL', limit=50)
    print(history)