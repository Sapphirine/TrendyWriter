import operator
from nltk.stem import WordNetLemmatizer
from stemming.porter2 import stem
from nltk.corpus import stopwords

txtfile = open("ulysses.txt","r+")
wordcount={}
wnl = WordNetLemmatizer()
stop = stopwords.words('english')

for word in txtfile.read().split():
    word = word.translate(None,',.?-()_').lower()
    if word not in stop:
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
    
    print k, v
