import insert_singleword, insert_cluster
import sys

field = str(sys.argv.pop())
if field:
	insert_cluster.insert(field)
	insert_singleword.insert(field)
