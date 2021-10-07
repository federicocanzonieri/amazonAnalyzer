
# amazonAnalyzer

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/federicocanzonieri/amazonAnalyzer/HEAD?filepath=book)
## Description

- This is a project created for the subject of TAP (Technologies for Advanced Programming) at UniCT.
- It creates a complete stream data pipeline to take reviews of a product from Amazon e then perfom some sentiment analysis.



## Technologies/method used


| Step | Technology used |
| :-: | :-: |
| Source | [Amazon with Python Scraper (Selenium)](https://www.amazon.it/ref=nav_logo) |
|Integration | [Logstash](https://www.elastic.co/logstash/)|
| Streaming| [Apache Kafka](https://kafka.apache.org/) |
| Processing |  [Apache Spark with sentiment analysis by Vader](https://spark.apache.org/) |
| Data storage | [Elasticsearch](https://www.elastic.co/enterprise-search) |
| Visualization | [Kibana](https://www.elastic.co/kibana) |


## Start


This project required **Docker** and **Docker-compose**.
- Download
  ```bash
  
  git clone URL
  cd amazonAnalyzer
	  ```
- Build:
   ```bash
  ./build.sh
	  ```
- Start:
  ```bash
  ./start.sh
  ```
- Stop:
  ```bash
  ./stop.sh
  ```
Make sure to configure **.env** properly before use it (CODE_PRODUCT).

## Configuration

To modify configuration see **.env** file

| Variable| Description |Default value|
| :-: | :-: |:-:|
|CODE_PRODUCT| Code of the product to analyze (default alexa) | ... |
|TIMEOUT_FETCH_ANOTHER_PAGE|Time (second) to wait before fetch another page | 5 |
|START_PAGE |Page start reviews |0 |
|END_PAGE|Page end reviews | 6 |
|MINUTES_TO_WAIT|Wait before fetch **streaming** page | 5 |
|DOMAIN_URL| Domain for fetch pages (www.amazon.) | supported co.uk,it  |
|MODE_REVIEWS| "recent" or "useful" | "recent"  |


## Network

Here is the table of services and network configuration.

| Service| IP|Port |
| :-: | :-: |:-:|  
|Python |**10.100.100.4**|
|Streaming|**10.100.100.5** |
|Logstash| **10.100.100.15** |**6000/6001**
|Zookeeper|**10.100.100.22** |**2181**
|KafkaServers | **10.100.100.23** |**9092**
|WebUI |  |**8080**
|Spark| **10.0.100.80** |
|ElasticSearch | **10.0.100.51** |**9200/9300**
|Kibana | **10.0.100.52** |


## Notes
Make sure that you have all the containers up after the "start.sh".