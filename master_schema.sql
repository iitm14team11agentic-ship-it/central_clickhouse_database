-- 1. CLEANUP (Start fresh)
DROP TABLE IF EXISTS technical_metrics;
DROP TABLE IF EXISTS sentiment_stream;
DROP TABLE IF EXISTS kafka_metrics_queue;
DROP TABLE IF EXISTS kafka_sentiment_queue;
DROP TABLE IF EXISTS mv_metrics_ingest;
DROP TABLE IF EXISTS mv_sentiment_ingest;

-- 2. STORAGE TABLES
CREATE TABLE technical_metrics (
    symbol String,
    timestamp DateTime,
    ts_ms UInt64,
    close Float32,
    sigma_forecast Float32,
    arma_forecast Float32,
    ema_trend_filter_trend_up Bool,
    ema_trend_filter_trend_down Bool,
    long_term_bias_trend_up Bool,
    long_term_bias_trend_down Bool,
    macd_signal Int32,
    bb_signal Int32,
    risk_adj_ret Float32,
    long_signal Bool,
    short_signal Bool,
    rsi_timing Int32
) ENGINE = MergeTree()
ORDER BY (symbol, timestamp)
TTL timestamp + INTERVAL 30 DAY;

CREATE TABLE sentiment_stream (
    symbol String,
    timestamp DateTime,
    sentiment_score Float32,
    news_title String,
    news_url String
) ENGINE = MergeTree()
ORDER BY (symbol, timestamp)
TTL timestamp + INTERVAL 90 DAY;

-- 3. KAFKA CONSUMERS (Localhost)
CREATE TABLE kafka_metrics_queue (
    symbol String, 
    timestamp DateTime, 
    ts_ms UInt64, 
    close Float32,
    sigma_forecast Float32, 
    arma_forecast Float32,
    ema_trend_filter_trend_up Bool, 
    ema_trend_filter_trend_down Bool,
    long_term_bias_trend_up Bool, 
    long_term_bias_trend_down Bool,
    macd_signal Int32, 
    bb_signal Int32, 
    risk_adj_ret Float32,
    long_signal Bool, 
    short_signal Bool, 
    rsi_timing Int32
) ENGINE = Kafka()
SETTINGS kafka_broker_list = 'localhost:9092', kafka_topic_list = 'Calculated', kafka_group_name = 'ch_metrics', kafka_format = 'JSONEachRow';

CREATE TABLE kafka_sentiment_queue (
    symbol String, timestamp DateTime, sentiment_score Float32, news_title String, news_url String
) ENGINE = Kafka()
SETTINGS kafka_broker_list = 'localhost:9092', kafka_topic_list = 'News', kafka_group_name = 'ch_news', kafka_format = 'JSONEachRow';

-- 4. MATERIALIZED VIEWS (The Movers)
CREATE MATERIALIZED VIEW mv_metrics_ingest TO technical_metrics AS SELECT * FROM kafka_metrics_queue;
CREATE MATERIALIZED VIEW mv_sentiment_ingest TO sentiment_stream AS SELECT * FROM kafka_sentiment_queue;