import operator

# Specify file path to execute word count
target_path = 'topic/all_topics.txt'

txtfile = open(target_path,"r+")
wordcount={}

for word in txtfile.read().split():
    word = word.translate (None, ',.?-()\'')
    pword = word.lower ()

    if pword.isdigit ():
        continue

    if len (pword) < 5:
        continue

    if pword not in wordcount:
        wordcount[pword] = 1
    else:
        wordcount[pword] += 1

counts = wordcount.items()
# sort all words in the order of wordcount amount 
sorted_counts = sorted (counts, key=operator.itemgetter(1))

for k,v in sorted_counts:
    print k, v
