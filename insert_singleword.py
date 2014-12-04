from pymongo import MongoClient
import datetime

class Word:
	def __init__(self, word_text, count = 0, cluster_names = []):
		self.w = word_text
		self.c = count
		self.t = datetime.datetime.utcnow()
		self.cn = cluster_names
		self.d = {
				"word":word_text,
				"count":count,
				"date":self.t,
				"cluster":cluster_names}

	def readFromMongo(self, entry):
		self.d = entry

def insert(path):
	client = MongoClient()
	db = client['test']
	single_word = db[path+'_single_word']

	with open("result/" + path+"/part-r-00000","r+") as pig_output:
		for line in pig_output:
			w,c = line.split()
			#print w,c
			cluses = db[path+'_clusters'].find({"words":w.lower()})
			clus_names = []
			if cluses:
				for clus in cluses:
					clus_names.append(clus['name'])
			word_instance = Word(w,int(c), clus_names)
			word_id = single_word.insert(word_instance.d)
			#print word_id
	"""
	with open("result/" + path+"hottest_words.txt", "r+") as collocation:
		for line in collocation:
			phrase_instance = Word(line)
			phrase_id = single_word.insert(phrase_instance)
			"""
