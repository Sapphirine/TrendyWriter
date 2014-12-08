#!/bin/sh


# PLEASE CHANGE THE FOLLOWING TWO ENVIRONMENT PARAMETER BEFORE START THE PROGRAM
export crawl_url="http://www.huffingtonpost.com/politics/"
export crawl_field="politics"

# setup environment variables
export project_home="/Users/Marcus/Documents/PycharmProjects/TrendyWriterVirtualEnv/__Python-Backend-Project___TrendyWriter-api_v1.2"
export pig="/Users/Marcus/Documents/pig-0.12-without_Hadoop/bin/pig"

# clean up all relative files
rm -rf ${project_home}/res/*
rm -rf ${project_home}/paragraph/data/*
rm -rf ${project_home}/topic/*
rm -rf ${project_home}/url/*
rm -rf ${project_home}/filter/*
rm -rf ${project_home}/mahout/cluster_result/*
rm -rf ${project_home}/pig/trending_singleword
rm -rf ${project_home}/result

# fetch data (paragraphs and titles)
python fetchtitle_v2.py ${crawl_url}
python fetchparagraph_v1.py ${crawl_url}

# process data
python wordcount.py
$pig -x local -f pig/topic_analysis.pig
./mahout/cluster_localfs.sh

# move result files for MongoDB
mkdir ${project_home}/result
mkdir ${project_home}/result/${crawl_field}
mv ${project_home}/pig/trending_singleword/part-r-00000 ${project_home}/result/${crawl_field}
mv ${project_home}/mahout/cluster_result/topics_clusters_dump ${project_home}/result/${crawl_field}
mv ${project_home}/filter/hottest_words.txt ${project_home}/result/${crawl_field}