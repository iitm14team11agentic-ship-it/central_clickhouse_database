## 📋 Requirements

**System:**
* Linux (Ubuntu 20.04+) or Windows Subsystem for Linux (WSL 2).
* **Java Runtime (JRE):** Required for Kafka (`sudo apt install default-jre`).
* **Python 3.10+:** With `pip` installed.

**Required Files:**
1.  `master_schema.sql` (Infrastructure)
2.  `producer.py` (Dummy Data Generator)
3.  `decision_service.py` (The Application)

(producer.py is for pipeline demonstration purposes)

# Install ClickHouse
curl [https://clickhouse.com/](https://clickhouse.com/) | sh
sudo ./clickhouse install
sudo service clickhouse-server start

# Download Kafka 3.6.0
wget [https://archive.apache.org/dist/kafka/3.6.0/kafka_2.13-3.6.0.tgz](https://archive.apache.org/dist/kafka/3.6.0/kafka_2.13-3.6.0.tgz)

# Extract it
tar -xzf kafka_2.13-3.6.0.tgz

# Libraries used
pip install clickhouse-connect kafka-python pandas

# Run these on 2 new and seperate terminals
cd kafka_2.13-3.6.0
bin/zookeeper-server-start.sh config/zookeeper.properties

cd kafka_2.13-3.6.0
bin/kafka-server-start.sh config/server.properties

# Create the Data Pipes (Topics)

cd kafka_2.13-3.6.0
bin/kafka-topics.sh --create --topic Calculated --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic News --bootstrap-server localhost:9092
cd ..

# Deploy Database Schema
clickhouse-client --multiquery < master_schema.sql

# run
python3 producer.py
python3 decision_service.py
