import operator

txtfile = open("ulysses.txt","r+")
wordcount={}
for word in txtfile.read().split():
    word = word.translate(None,',.?-()')
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

counts = wordcount.items()
sorted_counts = sorted(counts, key=operator.itemgetter(1))
for k,v in sorted_counts:
    print k, v
