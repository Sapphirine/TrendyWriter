# NOTE (MongoDB)
## functions to insert clusters and single words into mongodb
### Files required:
<ol>
<li>part-r-00000(pig word count result)</li>
<li>topics_clusters_dump</li>
<li>hottest_words.txt</li>
</ol>

### how to run:
<ol>
<li>Crate folders under the result folder using the name of fields (news, for example, 
is used in the test case) run insert.py with the name of fields as argument, it will automatically search for the 
result/{field_name}/ folder for files</li>
<li>Run server.py when insertion complete, default port: 9000</li>
</ol>

### how to query:
<ol>
<li>Query 1</li>
<ul>
<li>HTTP Request 1: localhost:9000/query?field=news</li>
<li>HTTP Response 1: Return a list of top words. if the word is included in clustering, 
you can also find cluster names in the JSON object also returns a list of top phrases</li>
</ul>
<li>Query 2</li>
<ul>
<li>HTTP Request 2: localhost:9000/cluster?field=news&cname=VL-183</li>
<li>HTTP Response 2: Return a list of words in a specific cluster</li>
</ul>    
</ol>