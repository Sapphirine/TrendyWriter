MAHOUT="/home/jethro/mahout/bin/mahout"
HADOOP_HOME="/home/jethro/.linuxbrew/Cellar/hadoop/2.5.1"
HDFS="$HADOOP_HOME/bin/hdfs"
PROJECT_HOME="/home/jethro/GitHub/__Python-Backend-Project___TrendyWriter-api_v1.2"

$HDFS dfs -rm -r topics
$HDFS dfs -rm -r topics-seqfiles
$HDFS dfs -rm -r topics-vectors
$HDFS dfs -rm -r topics-vectors-bigram
$HDFS dfs -rm -r topics-kmeans
$HDFS dfs -rm -r topics-kmeans-clusters

$HDFS dfs -mkdir topics
$HDFS dfs -copyFromLocal $PROJECT_HOME/data/ topics/

$MAHOUT seqdirectory -c UTF-8 -i topics -o topics-seqfiles
$MAHOUT seq2sparse -i topics-seqfiles -o topics-vectors-bigram -ow -chunk 200 -wt tfidf -s 5 -md 3 -x 90 -ng 2 -ml 50 -seq
$MAHOUT kmeans -i topics-vectors-bigram/tfidf-vectors -c topics-kmeans-clusters -o topics-kmeans -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -cd 1.0 -k 20 -x 20 -ow --clustering
$MAHOUT clusterdump -i topics-kmeans/clusters-*-final -o $PROJECT_HOME/result/topics_clusters_dump -d topics-vectors-bigram/dictionary.file-* -dt sequencefile -b 100 -n 10 --evaluate -dm org.apache.mahout.common.distance.SquaredEuclideanDistanceMeasure -sp 0 --pointsDir topics-kmeans/clusteredPoints
$MAHOUT seqdumper -i topics-kmeans/clusteredPoints -o $PROJECT_HOME/result/topics_seq_dump

