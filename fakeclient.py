import json, requests

data = {
        'username': 'jethro894',
		'password': 'passpass'
}

header = {'content-type': 'application/json'}

s = requests.Session()
r1 = s.post('http://localhost:9000/login', data=json.dumps(data), headers=header)
print s.cookies
r2 = s.get('http://localhost:9000/query?field=news')