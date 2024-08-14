import os
import socket
import time
from pyspark.sql import SparkSession
from Configuracoes import Configuracoes




sparkSession: SparkSession = SparkSession.builder 

if os.path.isdir("/opt/bitnami/spark/jars/"):
    path_to_jar = '/opt/bitnami/spark/jars/'
elif os.path.isdir("/opt/jars/"):
    path_to_jar = '/opt/jars/'
else:
    path_to_jar = "./"

sparkSession = sparkSession.config("spark.jars", 
    f"{path_to_jar}mongo-spark-connector_2.12-3.0.1.jar," +
    f"{path_to_jar}bson-4.0.5.jar," +
    f"{path_to_jar}mongodb-driver-core-4.0.5.jar," + 
    f"{path_to_jar}mongodb-driver-sync-4.0.5.jar," +
    f"{path_to_jar}ojdbc8-21.5.0.0.jar")
        
sparkSession = sparkSession\
    .config("spark.mongodb.input.uri", Configuracoes().mongo_uri_input) \
    .config("spark.mongodb.output.uri", Configuracoes().mongo_uri_output) \
    .config("spark.mongodb.input.sampleSize", 50000) \
    .config("spark.driver.host", socket.gethostbyname(socket.gethostname()))\
    .appName("ExtratorInformacoes") \
    .enableHiveSupport() \
    .getOrCreate()

#Setting log level in spark
#sparkSession.sparkContext.setLogLevel('WARN')

init_time = time.time()


print(f"Tempo corrido: {time.time() - init_time}")
sparkSession.stop()