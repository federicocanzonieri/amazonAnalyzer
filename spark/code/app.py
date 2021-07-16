from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.functions import from_json, col, to_timestamp, unix_timestamp, window
from pyspark.sql.types import *
#from sklearn.linear_model import LinearRegression
from elasticsearch import Elasticsearch
import time


schema = StructType([
    StructField("date", StringType(), False),
    StructField("body", StringType(), False),
    StructField("title", StringType(), False),
    StructField("rating", StringType(), False),
    #StructField("rating", LongType(), False),
    
])

def get_spark_session():
    spark_conf = SparkConf()\
        .set('es.nodes', 'elastic_search_AM')\
        .set('es.port', '9200')
    sc = SparkContext(appName='amazon_reviews', conf=spark_conf)
    return SparkSession(sc)


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
        .format('kafka') \
        .option('kafka.bootstrap.servers', kafkaServer) \
        .option('subscribe', 'amazon') \
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










