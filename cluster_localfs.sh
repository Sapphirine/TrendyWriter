#!/bin/bash

export PROJECT_HOME="/Users/Marcus/Documents/PycharmProjects/TrendyWrite_api"


# run on Hadoop
# export HADOOP_HOME="/usr/local/Cellar/hadoop/2.5.1"
# export HADOOP_PREFIX="/usr/local/Cellar/hadoop/2.5.1/libexec"
# export HDFS="${HADOOP_HOME}/bin/hdfs"
# export MAHOUT="/Users/Marcus/Documents/mahout-trunk/bin/mahout"
# unset MAHOUT_LOCAL
# export MAHOUT_CONF_DIR="/Users/Marcus/Documents/mahout-trunk/src/conf"

# run on local
export MAHOUT="/Users/Marcus/Documents/mahout-distribution-0.9/bin/mahout"
# export MAHOUT_CONF_DIR="/Users/Marcus/Documents/mahout-distribution-0.9/conf"
export MAHOUT_LOCAL=1


# run on Hadoop (only)
# $HDFS dfs -rm -r topics
# $HDFS dfs -rm -r topics-seqfiles
# $HDFS dfs -rm -r topics-vectors
# $HDFS dfs -rm -r topics-vectors-bigram
# $HDFS dfs -rm -r topics-kmeans
# $HDFS dfs -rm -r topics-kmeans-clusters
# $HDFS dfs -mkdir topics
# $HDFS dfs -copyFromLocal ${PROJECT_HOME}/topic/ topics/


# run on local
$MAHOUT seqdirectory -c UTF-8 -i ${PROJECT_HOME}/topic -o ${PROJECT_HOME}/result/topics-seqfiles
$MAHOUT seq2sparse -i ${PROJECT_HOME}/result/topics-seqfiles -o ${PROJECT_HOME}/result/topics-vectors-bigram -ow -chunk 200 -wt tfidf -s 5 -md 3 -x 90 -ng 2 -ml 50 -seq
$MAHOUT kmeans -i ${PROJECT_HOME}/result/topics-vectors-bigram/tfidf-vectors -c ${PROJECT_HOME}/result/topics-kmeans-clusters -o ${PROJECT_HOME}/result/topics-kmeans -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -cd 1.0 -k 20 -x 20 -ow --clustering
$MAHOUT clusterdump -i ${PROJECT_HOME}/result/topics-kmeans/clusters-*-final -o ${PROJECT_HOME}/result/topics_clusters_dump -d ${PROJECT_HOME}/result/topics-vectors-bigram/dictionary.file-* -dt sequencefile -b 100 -n 10 --evaluate -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -sp 0 --pointsDir ${PROJECT_HOME}/result/topics-kmeans/clusteredPoints
$MAHOUT seqdumper -i ${PROJECT_HOME}/result/topics-kmeans/clusteredPoints -o ${PROJECT_HOME}/result/topics_seq_dump

# run on Hadoop
# $MAHOUT seqdirectory -c UTF-8 -i topics/topic -o topics-seqfiles
# $MAHOUT seq2sparse -i topics-seqfiles -o topics-vectors-bigram -ow -chunk 200 -wt tfidf -s 5 -md 3 -x 90 -ng 2 -ml 50 -seq
# $MAHOUT kmeans -i topics-vectors-bigram/tfidf-vectors -c topics-kmeans-clusters -o topics-kmeans -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -cd 1.0 -k 20 -x 20 -ow --clustering
# $MAHOUT clusterdump -i topics-kmeans/clusters-*-final -o $PROJECT_HOME/result/topics_clusters_dump -d topics-vectors-bigram/dictionary.file-* -dt sequencefile -b 100 -n 10 --evaluate -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -sp 0 --pointsDir topics-kmeans/clusteredPoints
# $MAHOUT seqdumper -i topics-kmeans/clusteredPoints -o $PROJECT_HOME/result/topics_seq_dump



