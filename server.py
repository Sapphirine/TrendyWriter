import sys,json,urlparse,hashlib,Cookie,time,os
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from pymongo import MongoClient

Protocol = "HTTP/1.1"

if sys.argv[1:]:
	port = int(sys.argv[1])
else:
	port = 9000

server_address = ("", port)

cookies = []


class myHandler(BaseHTTPRequestHandler):

	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content_type", "application/json")
		self.end_headers()

	def parse_POST(self):
		self.postvars = {}
		if self.headers.type == 'application/json':
			self.query_string = self.rfile.read(int(self.headers['content-length']))
			self.postvars = json.loads(self.query_string)

	def do_POST(self):
		self.parse_POST()
		if self.postvars == {}:
			self.send_response(404)
			return

		parsed = urlparse.urlparse(self.path)

		if parsed.path=="/create":
			usrn = self.postvars['username']
			pswd = self.postvars['password']
			mongo_client = MongoClient()
			db = mongo_client['test']
			users = db['users']
			if users.find({'username':usrn}).count() > 0:
				self.send_response(409)
				return
			user = {'username': usrn,
					'password_hash':hashlib.md5(pswd).hexdigest()}
			users.insert(user)
			self.send_response(200)
			self.wfile.write(self.new_cookie().output())

		if parsed.path=="/login":
			usrn = self.postvars['username']
			pswd = self.postvars['password']
			mongo_client = MongoClient()
			db = mongo_client['test']
			users = db['users']
			if users.find({'username':usrn}).count() == 0:
				self.send_response(404)
				return
			for user in users.find({'username':usrn}).limit(1):
				if user['password_hash'] == hashlib.md5(pswd).hexdigest():
					self.send_response(200)
					self.wfile.write(self.new_cookie().output())
				else:
					self.send_response(401)

	def new_cookie(self):
		cookie = Cookie.SimpleCookie()
		cookie['sid'] = hashlib.md5(str(time.time())).hexdigest()
		expires = time.time() + 30*60
		cookie['sid']['expires'] = expires
		cookies.append(cookie)
		return cookie

	def verify_cookie(self):
		cookie = self.headers['cookie']
		if cookie is None:
			return False
		for ck in cookies:
			if 'sid='+ck['sid'].value == cookie:
				if float(ck['sid']['expires']) < time.time():
					return False
				return True
		return False

	def do_GET(self):
		parsed = urlparse.urlparse(self.path)
		if self.verify_cookie() is False:
			self.send_error(401)

		if parsed.path=="/query":
			field=urlparse.parse_qs(parsed.query)['field'][0]
			mongo_client = MongoClient()
			db = mongo_client['test']
			if field+'_single_word' not in db.collection_names():
				self.send_response(404)
			else:
				single = db[field+'_single_word']
				top_words = single.find().limit(20)
				message = []

				for word in top_words:
					a_word = {'word': word['word']}
					if len(word['cluster'])>0:
						a_word['cluster'] = word['cluster']
					message.append(a_word)

				double = db[field+'_phrase']
				top_phrases = double.find().limit(10)
				for phrase in top_phrases:
					a_phrase = {'word' : phrase['word']}
					message.append(a_phrase)

				self.send_response(200, message)
				self.send_header("Content_type", "application/json")
				self.end_headers()
				self.wfile.write(message)

		if parsed.path=="/cluster":
			field=urlparse.parse_qs(parsed.query)['field'][0]
			name = urlparse.parse_qs(parsed.query)['cname'][0]
			mongo_client = MongoClient()
			db = mongo_client['test']
			if field+'_clusters' not in db.collection_names():
				self.send_response(404)
			else:
				clus = db[field+'_clusters']
				cluster_wanted = clus.find({"name":name}).limit(1)
				message = []
				for a_cluster in cluster_wanted:
					message.append(a_cluster['words'])
				self.send_response(200, message)
				self.send_header("Content_type", "application/json")
				self.end_headers()
				self.wfile.write(message)

if __name__ == '__main__':
	httpd = HTTPServer(server_address, myHandler)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

