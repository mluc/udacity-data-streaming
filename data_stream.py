import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

# TODO Create a schema for incoming resources
schema = StructType([StructField('crime_id', StringType()),
                     StructField('original_crime_type_name', StringType()),
                     StructField('report_date', StringType()),
                     StructField('call_date', StringType()),
                     StructField('offense_date', StringType()),
                     StructField('call_time', StringType()),
                     StructField('call_date_time', TimestampType()),
                     StructField('disposition', StringType()),
                     StructField('address', StringType()),
                     StructField('city', StringType()),
                     StructField('state', StringType()),
                     StructField('agency_id', StringType()),
                     StructField('address_type', StringType()),
                     StructField('common_location', StringType())])


def run_spark_job(spark):
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sf.crime.topic") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 200) \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    kafka_df = df.selectExpr("CAST(value AS string)")
    service_table = kafka_df \
        .select(psf.from_json(psf.col('value'), schema).alias("DF")) \
        .select("DF.*")

    # select original_crime_type_name and disposition
    distinct_table = service_table.na.drop(subset=['original_crime_type_name', 'disposition']) \
        .select('original_crime_type_name', 'disposition', 'call_date_time') \
        .distinct() \
        .withWatermark("call_date_time", "2 minutes")

    # count the number of original crime type
    agg_df = distinct_table.groupby('original_crime_type_name').count()

    # write output stream
    query = agg_df \
        .writeStream \
        .trigger(processingTime="5 seconds") \
        .outputMode('Complete') \
        .format('console') \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()

    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    join_query = agg_df.join(radio_code_df, agg_df.disposition == radio_code_df.disposition, "inner")

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    spark = SparkSession \
        .builder \
        .config('spark.ui.port', 3000) \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()

    spark.sparkContext.setLogLevel('WARN')

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
