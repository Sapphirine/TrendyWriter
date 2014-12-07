import sys

import insert_singleword
import insert_cluster


field = str(sys.argv.pop())
if field:
    insert_cluster.insert(field)
    insert_singleword.insert(field)
