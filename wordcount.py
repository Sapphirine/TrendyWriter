import operator
import nltk
import os
import sys
from nltk.stem import WordNetLemmatizer
from stemming.porter2 import stem
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.tokenize import *

filename = str(sys.argv.pop())
#txtfile = open("ulysses.txt","r+")
txtfile = open(filename,"r+")
#filepath = os.path.abspath(txtfile.name)
wordcount={}
wnl = WordNetLemmatizer()
stop = stopwords.words('english')
words = [w.translate(None,',.?()_:') for w in txtfile.read().split()]

for word in words:
	if not word.isupper():
		word = word.lower()

	if word not in stop and word.__len__()>=2:
		#stemmed_word = stem(wnl.lemmatize(word))
		stemmed_word = wnl.lemmatize(word)
		if stemmed_word not in stop:
			if stemmed_word not in wordcount:
				wordcount[stemmed_word] = 1
			else:
				wordcount[stemmed_word] += 1

counts = wordcount.items()
sorted_counts = sorted(counts, key=operator.itemgetter(1))

for k,v in sorted_counts:
	if v > 20:
		#tag = nltk.pos_tag(word_tokenize(k))
		#if tag[0][1] != 'VB':
		mnls_word = ['make','get','set','say','said']
		if k not in mnls_word:
			print k, v

'''
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

finder = BigramCollocationFinder.from_words(words,window_size = 2)
finder.apply_freq_filter(3) 
print finder.nbest(bigram_measures.pmi, 10)

finder2 = TrigramCollocationFinder.from_words(words)
finder2.apply_freq_filter(3)
print finder2.nbest(trigram_measures.pmi,10)
'''
