from kafka import KafkaProducer
import json
import time
from datetime import datetime

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("--- 📡 SENDING DUMMY DATA STREAMS ---")

# 1. SEND NEWS (Sparse - 1 article)
news_msg = {
    "symbol": "AAPL",
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "sentiment_score": 0.85,
    "news_title": "Apple releases M5 Chip",
    "news_url": "bloomberg.com/tech"
}
producer.send('News', value=news_msg)
print(f"[News] Sent: {news_msg['news_title']}")

# 2. SEND METRICS (Dense - 10 ticks)
for i in range(10):
    metric_msg = {
        "symbol": "AAPL",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ts_ms": int(time.time() * 1000),
        "close": 150.0 + (i * 0.5),
        
        "sigma_forecast": 0.015,
        "arma_forecast": 152.0,
        
        # Boolean Filters
        "ema_trend_filter_trend_up": True,
        "ema_trend_filter_trend_down": False,
        "long_term_bias_trend_up": True,
        "long_term_bias_trend_down": False,
        
        # Signals
        "macd_signal": 1,
        "bb_signal": 0,
        "risk_adj_ret": 0.05,
        "long_signal": True,
        "short_signal": False,
        "rsi_timing": 60 + i
    }
    producer.send('Calculated', value=metric_msg)
    print(f"[Metrics] Sent tick {i+1}/10")
    time.sleep(1)

producer.flush()
print("--- ✅ DONE ---")