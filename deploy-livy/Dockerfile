FROM openjdk:11-jdk-slim-buster

RUN apt-get update
RUN apt-get install unzip
RUN apt-get -y install wget

############
# Versions #
############
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV LIVY_VERSION=0.8.0
ENV LIVY_INCUBATING_VERSION=2.12

##############################
# Paths inside the container #
##############################
ENV WORKDIR_PATH=/opt
ENV ARCHIVES_PATH=/tmp

ENV SPARK_HOME=$WORKDIR/spark
ENV LIVY_HOME=$WORKDIR/livy

###########################
# External archives paths #
###########################
# Assuming you already downloaded Spark to the current directory from https://archive.apache.org/dist/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7
ENV SPARK_FOLDER_IN_ARCHIVE=spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_ARCHIVE=${SPARK_FOLDER_IN_ARCHIVE}.tgz

# Assuming you already downloaded Livy to the current directory from http://mirror.23media.de/apache/incubator/livy/0.7.0-incubating/apache-livy-0.7.0-incubating-bin.zip
ENV LIVY_FOLDER_IN_ARCHIVE=apache-livy-${LIVY_VERSION}-incubating_${LIVY_INCUBATING_VERSION}-bin
ENV LIVY_ARCHIVE=${LIVY_FOLDER_IN_ARCHIVE}.zip

##############################################
# Copy archives, extract and delete archives #
##############################################
COPY ./$SPARK_ARCHIVE $ARCHIVES_PATH
COPY ./$LIVY_ARCHIVE $ARCHIVES_PATH

RUN tar -xvzf $ARCHIVES_PATH/$SPARK_ARCHIVE -C $WORKDIR_PATH
RUN unzip $ARCHIVES_PATH/$LIVY_ARCHIVE -d $WORKDIR_PATH

RUN mv $WORKDIR_PATH/$SPARK_FOLDER_IN_ARCHIVE $SPARK_HOME
RUN mv $WORKDIR_PATH/$LIVY_FOLDER_IN_ARCHIVE $LIVY_HOME

RUN rm $ARCHIVES_PATH/$SPARK_ARCHIVE
RUN rm $ARCHIVES_PATH/$LIVY_ARCHIVE

##############
# Enrtypoint #
##############  
COPY ./entrypoint.sh $WORKDIR_PATH
RUN chmod +x $WORKDIR_PATH/entrypoint.sh

WORKDIR $WORKDIR_PATH
ENTRYPOINT ./entrypoint.sh $LIVY_HOME $SPARK_HOME

COPY ./src $WORKDIR_PATH
COPY ./requirements.txt $WORKDIR_PATH
COPY ./jars /spark/jars
COPY ./jars /opt/bitnami/spark/jars

#Installing Python 3.11.9
RUN apt-get update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev 
RUN wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
RUN tar -xf Python-3.11.9.tgz
RUN cd ./Python-3.11.9  && ./configure --enable-optimizations && make -j$(nproc) && make altinstall
RUN python3.11 -m pip install -r $WORKDIR_PATH/requirements.txt

ENV PYSPARK_PYTHON="python3.11"
ENV PYSPARK_DRIVER_PYTHON="python3.11"
