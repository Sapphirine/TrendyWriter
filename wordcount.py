import operator

# Specify file path to execute word count
target_path = 'topic/all_topics.txt'

txtfile = open(target_path,"r+")
wordcount={}
for word in txtfile.read().split():
    word = word.translate(None,',.?-()')
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

counts = wordcount.items()
# sort all words in the order of wordcount amount 
sorted_counts = sorted(counts, key=operator.itemgetter(1))
for k,v in sorted_counts:
    print k, v
