# Public Transit Status with Apache Kafka
## Github link:
- https://github.com/mluc/udacity-data-streaming
## How to run:
- `docker-compose up`
- `python producers/simulation.py`
- `faust -A faust_stream worker -l info`
- `python consumers/python ksql.py`
- `python consumers/python server.py`
## Screenshots:
- `screenshot.png`
## Testing during development:
### Test Kafka Producers:
- `python producer_test.py`
```
(venv) Roberts-MBP:udacity-data-streaming myluc$ docker exec -it udacity-data-streaming_kafka0_1 bash
root@c14de902f0e4:/# kafka-topics --list --zookeeper zookeeper:2181
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-ksql_service_docker_command_topic
_schemas
addison.arrival
austin.arrival
...
turnstile
uic_halsted.arrival
washington.arrival
western_and_forest_pk_branch.arrival
western_and_ohare_branch.arrival
root@c14de902f0e4:/# kafka-console-consumer --topic turnstile --bootstrap-server localhost:9092 --from-beginning
��Irving Parblue
��Irving Parblue
��Irving Parblue
��Irving Parblue
��Addisoblue
��Addisoblue
��Belmonblue
��Californiblue
^CProcessed a total of 8 messages
root@c14de902f0e4:/# kafka-console-consumer --topic addison.arrival --bootstrap-server localhost:9092 --from-beginning
��
BL001bluein_service��b
��
BL009bluein_service��a
^CProcessed a total of 2 messages
root@c14de902f0e4:/#
```
### Test Kafka REST Proxy Producer:
- `python weather_test.py`
```
(venv) Roberts-MBP:udacity-data-streaming myluc$ docker exec -it udacity-data-streaming_kafka0_1 bash
root@250d642995c2:/# kafka-topics --list --zookeeper zookeeper:2181
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-ksql_service_docker_command_topic
_schemas
connect-config
connect-offset
connect-status
weather
root@250d642995c2:/# kafka-console-consumer --topic weather --bootstrap-server localhost:9092 --from-beginning
{"temperature":45.0563414899434,"status":"sunny"}

```
### Test postgres:
- `psql` from local to tunnel through postgres:
```
(venv) Roberts-MBP:producers myluc$ psql -h localhost -p 5432 -d cta -U cta_admin --password
Password:
psql (12.3, server 11.10 (Debian 11.10-1.pgdg90+1))
Type "help" for help.

cta=# select * from stations limit 1;
 stop_id | direction_id |         stop_name         | station_name | station_descriptive_name | station_id | order | red | blue | green
---------+--------------+---------------------------+--------------+--------------------------+------------+-------+-----+------+-------
   30004 | W            | Harlem (Terminal arrival) | Harlem/Lake  | Harlem/Lake (Green Line) |      40020 |     0 | f   | f    | t
(1 row)

cta=# \q
```
### Test connector:
- `python connector.py` to create a new connector
- Kafka Connect API:
```
(venv) Roberts-MBP:producers myluc$ curl http://localhost:8083/connectors | python -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    951      0 --:--:-- --:--:-- --:--:--  1000
[
    "stations"
]
(venv) Roberts-MBP:producers myluc$ curl http://localhost:8083/connectors/stations/status | python -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   158  100   158    0     0   7171      0 --:--:-- --:--:-- --:--:--  7523
{
    "name": "stations",
    "connector": {
        "state": "RUNNING",
        "worker_id": "connect:8083"
    },
    "tasks": [
        {
            "id": 0,
            "state": "RUNNING",
            "worker_id": "connect:8083"
        }
    ],
    "type": "source"
}
(venv) Roberts-MBP:producers myluc$
```
- Kafka-console-consumer and kafka-topics CLI:
```
(venv) Roberts-MBP:udacity-data-streaming myluc$ docker exec -it udacity-data-streaming_kafka0_1 bash
root@e37b8e9edf16:/# kafka-topics --list --zookeeper zookeeper:2181
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-ksql_service_docker_command_topic
_schemas
connect-config
connect-offset
connect-status
my-topic-stations
root@e37b8e9edf16:/# kafka-console-producer --broker-list localhost:9092 --topic my-topic-stations
>hello0
>hello1
root@e37b8e9edf16:/# kafka-console-consumer --topic my-topic-stations --bootstrap-server localhost:9092 --from-beginning
{"stop_id":30001,"direction_id":"E","stop_name":"Austin (O'Hare-bound)","station_name":"Austin","station_descriptive_name":"Austin (Blue Line)","station_id":40010,"order":29,"red":false,"blue":true,"green":false}
...
{"stop_id":30384,"direction_id":"S","stop_name":"Washington/Wabash (Inner Loop)","station_name":"Washington/Wabash","station_descriptive_name":"Washington/Wabash (Brown, Green, Orange, Purple & Pink Lines)","station_id":41700,"order":16,"red":false,"blue":false,"green":true}
hello0
hello1

```
### Test Faust Stream Processor:
- `python connector.py`
- `python faust_stream.py worker`
```
(venv) Roberts-MBP:udacity-data-streaming myluc$ docker exec -it udacity-data-streaming_kafka0_1 bash
root@d8786c7321bb:/# kafka-topics --list --zookeeper zookeeper:2181
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-ksql_service_docker_command_topic
_schemas
connect-config
connect-offset
connect-status
my-topic-stations
my-topic-stations-transformed
stations-stream-__assignor-__leader

root@d8786c7321bb:/# kafka-console-consumer --topic my-topic-stations --bootstrap-server localhost:9092 --from-beginning
{"stop_id":30001,"direction_id":"E","stop_name":"Austin (O'Hare-bound)","station_name":"Austin","station_descriptive_name":"Austin (Blue Line)","station_id":40010,"order":29,"red":false,"blue":true,"green":false}
{"stop_id":30002,"direction_id":"W","stop_name":"Austin (Forest Pk-bound)","station_name":"Austin","station_descriptive_name":"Austin (Blue Line)","station_id":40010,"order":29,"red":false,"blue":true,"green":false}
...

root@d8786c7321bb:/# kafka-console-consumer --topic my-topic-stations-transformed --bootstrap-server localhost:9092 --from-beginning
{"station_id": 40010, "station_name": "Austin", "order": 29, "line": "blue", "__faust": {"ns": "consumers.udacity-data-streaming.faust_stream.TransformedStation"}}
{"station_id": 40010, "station_name": "Austin", "order": 29, "line": "blue", "__faust": {"ns": "consumers.udacity-data-streaming.faust_stream.TransformedStation"}}
...

```
### Test KSQL:
- `python producer_test.py` to create `turnstile` topic
```
(venv) Roberts-MBP:consumers myluc$ docker exec -it udacity-data-streaming_ksql_1 bash
root@2378801f9f3a:/# ksql

                  ===========================================
                  =        _  __ _____  ____  _             =
                  =       | |/ // ____|/ __ \| |            =
                  =       | ' /| (___ | |  | | |            =
                  =       |  <  \___ \| |  | | |            =
                  =       | . \ ____) | |__| | |____        =
                  =       |_|\_\_____/ \___\_\______|       =
                  =                                         =
                  =  Streaming SQL Engine for Apache Kafka® =
                  ===========================================

Copyright 2017-2018 Confluent Inc.

CLI v5.2.2, Server v5.2.2 located at http://localhost:8088

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql> SET 'auto.offset.reset' = 'earliest';
Successfully changed local property 'auto.offset.reset' to 'earliest'. Use the UNSET command to revert your change.

ksql> CREATE TABLE turnstile (
>    station_id INTEGER,
>    station_name VARCHAR,
>    line VARCHAR
>) WITH (
>    KAFKA_TOPIC='turnstile',
>    VALUE_FORMAT='AVRO',
>    KEY='station_id'
>);

 Message
---------------
 Table created
---------------
ksql> CREATE TABLE turnstile_summary
>WITH (
>    KAFKA_TOPIC='turnstile.summary',
>    VALUE_FORMAT='JSON'
>) AS
>    select station_id, count(*) as count from TURNSTILE group by station_id;

 Message
---------------------------
 Table created and running
---------------------------

ksql> SHOW TABLES;

 Table Name        | Kafka Topic       | Format | Windowed
-----------------------------------------------------------
 TURNSTILE         | turnstile         | AVRO   | false
 TURNSTILE_SUMMARY | turnstile.summary | JSON   | false
-----------------------------------------------------------

ksql> select * from TURNSTILE limit 5;
1606000478149 | 枴ѽ] | 40220 | Western/Forest Pk Branch | blue
1606000477803 | �ѽ] | 40230 | Cumberland | blue
1606000477803 | ֙�ѽ] | 40230 | Cumberland | blue
1606000477830 | ڙ�ѽ] | 40750 | Harlem | blue
1606000478189 | ܟ�ѽ] | 40970 | Cicero | blue
Limit Reached
Query terminated

ksql> select * from TURNSTILE_SUMMARY limit 5;
1606000477878 | 41330 | 41330 | 2
1606000478210 | 40180 | 40180 | 1
1606000478149 | 40220 | 40220 | 1
1606000478189 | 40970 | 40970 | 1
1606000477803 | 40230 | 40230 | 2
Limit Reached
Query terminated

ksql> SHOW TOPICS;

 Kafka Topic                          | Registered | Partitions | Partition Replicas | Consumers | ConsumerGroups
------------------------------------------------------------------------------------------------------------------
 _schemas                             | false      | 1          | 1                  | 0         | 0
 addison.arrival                      | false      | 1          | 1                  | 0         | 0
 austin.arrival                       | false      | 1          | 1                  | 0         | 0
 ...
 turnstile                            | true       | 1          | 1                  | 1         | 1
 turnstile.summary                    | true       | 4          | 1                  | 0         | 0
 uic_halsted.arrival                  | false      | 1          | 1                  | 0         | 0
 washington.arrival                   | false      | 1          | 1                  | 0         | 0
 western_and_forest_pk_branch.arrival | false      | 1          | 1                  | 0         | 0
 western_and_ohare_branch.arrival     | false      | 1          | 1                  | 0         | 0
------------------------------------------------------------------------------------------------------------------

ksql> describe turnstile_summary;

Name                 : TURNSTILE_SUMMARY
 Field      | Type
----------------------------------------
 ROWTIME    | BIGINT           (system)
 ROWKEY     | VARCHAR(STRING)  (system)
 STATION_ID | INTEGER
 COUNT      | BIGINT
----------------------------------------
For runtime statistics and query details run: DESCRIBE EXTENDED <Stream,Table>;

ksql> SHOW QUERIES;

 Query ID                 | Kafka Topic       | Query String
-----------------------------------------------------------------------------------------------------------------------------
 CTAS_TURNSTILE_SUMMARY_0 | TURNSTILE_SUMMARY | CREATE TABLE turnstile_summary
WITH (
    KAFKA_TOPIC='turnstile.summary',
    VALUE_FORMAT='JSON'
) AS
    select station_id, count(*) as count from TURNSTILE group by station_id;
-----------------------------------------------------------------------------------------------------------------------------
For detailed information on a Query run: EXPLAIN <Query ID>;
ksql> terminate CTAS_TURNSTILE_SUMMARY_0;

 Message
-------------------
 Query terminated.
-------------------
ksql> drop table TURNSTILE_SUMMARY;

 Message
----------------------------------------
 Source TURNSTILE_SUMMARY was dropped.
----------------------------------------
ksql> drop table TURNSTILE;

 Message
--------------------------------
 Source TURNSTILE was dropped.
--------------------------------
ksql>

```