from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.functions import from_json, col, to_timestamp, unix_timestamp, window
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import time
import socket
import os
from pyspark.sql.functions import udf

HOST_ELASTIC=os.getenv("IP_ELASTIC")
PORT_ELASTIC=os.getenv("PORT_ELASTIC_1")
TOPIC=os.getenv("TOPIC")
INDEX=os.getenv("INDEX")
vader=SentimentIntensityAnalyzer()

##ESTABLISH CONNECTION TO LOGSTASH
time.sleep(int(os.getenv("TIMEOUT_BEFORE_START_SPARK")))


##GET POLARITY
def get_sentiment(text):
    value = vader.polarity_scores(text)
    value = value['compound']
    return value

##SCHEMA JSON (FROM KAFKA)
schema = StructType([
    StructField("date", StringType(), False),
    StructField("body", StringType(), False),
    StructField("title", StringType(), False),
    StructField("rating", StringType(), False),
    StructField("name", StringType(), False),
    StructField("verified_buy", StringType(), False),
    StructField("helpful_vote", StringType(), False),
    StructField("country", StringType(), False),
    #StructField("rating", LongType(), False),
])

def get_spark_session():
    spark_conf = SparkConf()\
        .set('es.nodes', 'elastic_search_AM')\
        .set('es.port', '9200')
    sc = SparkContext(appName='reviews_analyzer', conf=spark_conf)
    return SparkSession(sc)



spark = get_spark_session()
spark.sparkContext.setLogLevel("ERROR")

topic=TOPIC
elastic_host = "elastic_search_AM"
elastic_index = INDEX
kafkaServer = "kafka_server_AM:9092"

print("nuovo")

df=spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', kafkaServer) \
        .option('subscribe', topic) \
        .option("startingOffsets","earliest") \
        .load() \
        #
        #.load() \
        #.option("kafka.group.id", "spark-consumer") \
        


es_mapping = {
    "mappings": {
        "properties": {
            "@timestamp":       {"type": "date", "format": "epoch_second"},
            "rating":   {"type": "integer"},
            "title":    {"type": "keyword"},
            "body":     {"type": "keyword"},
            "date":     {"type": "keyword"},
            ##AGGIUNGERE ALTRI
            #"coords":           {"type": "text"},
            #"PI":               {"type": "keyword"}
        }
    }
}

###FROM HEREEEEEEEEEEEE

es = Elasticsearch(host='elastic_search_AM')
response = es.indices.create(
    index=elastic_index, 
    body=es_mapping, 
    ignore=400
)

if 'acknowledged' in response:
    if response['acknowledged'] == True:
        print("Successfully created index:", response['index'])

##Con solo cast as string funziona
df=df.selectExpr("CAST(value as STRING)") \
    .select(from_json("value",schema=schema).alias("data"))\
    .select("data.*") \
      #.alias("data"))\
     #\

def splitting(x):
    return x.split(" ")

sentimen=udf(get_sentiment,DoubleType())
splitt=udf(splitting,ArrayType(StringType()))
df=df.withColumn("sentiment",sentimen("title"))
df=df.withColumn("words",splitt("title"))

#pprint(df)
#print(df.describe())
#print(df.show())

query=df.writeStream \
        .option("checkpointLocation", "./checkpoints") \
        .format("es") \
        .start(elastic_index + "/_doc")\
        #.show()
        #.show()
query.awaitTermination()










