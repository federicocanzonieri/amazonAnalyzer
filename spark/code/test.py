from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.functions import from_json, col, to_timestamp, unix_timestamp, window
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
import time
import socket
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


##ESTABLISH CONNECTION TO LOGSTASH
###TESTING 
sid = SentimentIntensityAnalyzer()


schema = StructType([

    StructField("date", StringType(), False),
    StructField("body", StringType(), False),
    StructField("title", StringType(), False),
    StructField("rating", StringType(), False),
    #StructField("rating", LongType(), False),
    
])

def get_spark_session():
    spark_conf = SparkConf()\
        #.set('es.nodes', 'elastic_search_AM')\
        #.set('es.port', '9200')
    sc = SparkContext(appName='amazon_reviews', conf=spark_conf)
    return SparkSession(sc)

def get_sentiment(text):
    value = sid.polarity_scores(text)
    value = value['compound']
    return value

#time.sleep(150)
print("ECCOMI SVEGLIO")

spark = get_spark_session()
spark.sparkContext.setLogLevel("ERROR")

topic="amazon"
elastic_host = "elastic_search_AM"
elastic_index = "reviews"
kafkaServer = "kafka_server_AM:9092"

print("nuovo")

df=spark.readStream \
        .schema(schema) \
        .json("/opt/tap/json/test1.json") \
        #.start()
        #.load() \
        #
        #.load() \
        #.option("kafka.group.id", "spark-consumer") \
        
#print(df.collect())
#print(df.take(10))

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

# es = Elasticsearch(host='elastic_search_AM')
# response = es.indices.create(
#     index=elastic_index, 
#     body=es_mapping, 
#     ignore=400
# )

# if 'acknowledged' in response:
#     if response['acknowledged'] == True:
#         print("Successfully created index:", response['index'])



##Con solo cast as string funziona
#df=df.selectExpr("CAST(value as STRING)") \
 #   .select(from_json("value",schema=schema).alias("data"))\
  #  .select("data.*") \
     #.alias("data"))\
     #\

# df=df.rdd.map(lambda x:{
#     'title':x['title'],
#     'sentiment':get_sentiment(x['title'])
# })
    

#pprint(df)
# print(df.describe())
#print(df.show())


query=df.writeStream \
        .format("console")\
        .foreachBatch(lambda x :print(x))\
        .start()\
        .awaitTermination()\
         #.option("checkpointLocation", "./checkpoints") \
         #.format("es") \
         
         #.start(elastic_index + "/_doc")\
# query.awaitTermination()










