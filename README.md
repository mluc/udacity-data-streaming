# Public Transit Status with Apache Kafka
## Testing:
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