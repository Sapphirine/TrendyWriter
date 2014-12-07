new functions to insert clusters and single words into mongodb
how to run:
	create folders under the result folder using the name of fields (news, for example, is used in the test case)
	run insert.py with the name of fields as argument, it will automatically search for the result/{field_name}/ folder for files
	files required: part-r-00000(pig word count result)
			topics_clusters_dump
			hottest_words.txt

then run server.py when insertion complete, default port: 9000

url query 1: localhost:9000/query?field=news
	returns list of top words. if the word is included in clustering, you can also find cluster names in the JSON object
	also returns a list of top phrases
url query 2: localhost:9000/cluster?field=news&cname=VL-183
	returns the list of words in a specific cluster
