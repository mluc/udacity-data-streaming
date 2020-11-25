# udacity-data-streaming
## Step 1:
- Terminal 1: `/usr/bin/zookeeper-server-start config/zookeeper.properties`
- Terminal 2: `/usr/bin/kafka-server-start config/server.properties`
- Terminal 3: `python kafka_server.py`
- Terminal 4: 
```
root@c1b2c1a75be5:/home/workspace# /usr/bin/kafka-topics --list --zookeeper localhost:2181__confluent.support.metrics
__consumer_offsets
sf.crime.topic

```
- Terminal 4: `/usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic sf.crime.topic --from-beginning`
    - Screenshot: `step1.png`
- Terminal 4: `python consumer_server.py`
    - Screenshot: `step1_consumer_server.png`
    
## Step 2:
- `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`
- Screenshots: `step2_spark_job.png` and `step2_ui.png`

## Step 3:
- How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
    - The larger `maxOffsetsPerTrigger` value, the more data needs to be shuffled (shuffle read/write is higher). Larger `maxOffsetsPerTrigger` value will take longer to finish the batch.
    - `processingTime`: The trigger interval is too small, batches fall behind since time to process is larger trigger interval. If it is too big, the next batch needs to wait.

- What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?
    - `maxOffsetsPerTrigger` = 200 and `processingTime` = 5 seconds are good for this dataset. Average duration is 5 s and shuffle read/write is minimal.