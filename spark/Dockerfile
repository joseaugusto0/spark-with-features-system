FROM docker.io/bitnami/spark:3.5

USER root

COPY ./requirements.txt ./

# Install prerequisites
RUN apt-get update && pip install -r ./requirements.txt

COPY ./jars/mongo-spark-connector_2.12-3.0.1.jar /opt/bitnami/spark/jars
COPY ./jars/bson-4.0.5.jar /opt/bitnami/spark/jars
COPY ./jars/mongodb-driver-core-4.0.5.jar /opt/bitnami/spark/jars
COPY ./jars/mongodb-driver-sync-4.0.5.jar /opt/bitnami/spark/jars
COPY ./jars/ojdbc8-21.5.0.0.jar /opt/bitnami/spark/jars


COPY ./src /opt/bitnami/spark/