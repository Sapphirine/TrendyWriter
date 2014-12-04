from pymongo import MongoClient
import datetime

class Cluster:
	def __init__(self, cluster_name, words):
		self.n = cluster_name
		self.ws = words
		self.t = datetime.datetime.utcnow()
		self.d = {"name" : cluster_name,
				  "words" : words,
				  "date" : self.t}

def read_blocks(cluster_file):
	count = 0
	blocks = []
	block = []
	for line in cluster_file:
		block.append(line)
		count+=1
		if(count == 14):
			blocks.append(block)
			block = []
			count = 0

	return blocks

def block_to_cluster(block):
	cluster_name = block[0][1:block[0].find('{')]
	top_words = []
	for i in range(2, 12):
		top_words.append(block[i].partition(' ')[0].strip('\t'))

	cluster = Cluster(cluster_name, top_words)
	return cluster

def insert(path):
	client = MongoClient()
	db = client['test']
	clusters = db[path+'_clusters']

	with open("result/" + path+"/topics_clusters_dump", "r+") as cluster_dump:
		for block in read_blocks(cluster_dump):
			cluster = block_to_cluster(block)
			clusters.insert(cluster.d)

