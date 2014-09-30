import sys
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import MySQLdb

Protocol = "HTTP/1.1"

if sys.argv[1:]:
	port = int(sys.argv[1])
else:
	port = 9000

server_address = ("", port)

class myHandler(BaseHTTPRequestHandler):

	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content_type", "text/html")
		self.end_headers()

	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ]
		message = '\r\n'.join(message_parts)
		self.send_response(200)
		self.send_header("Content_type", "text/html")
		self.end_headers()
		self.wfile.write(message)
		
		if(self.path == "/wordcount"):
			try:
				conn = MySQLdb.connect(host='localhost', user='root', db='test',port=3306)
				cur = conn.cursor()
				count = cur.execute('describe wordcount')
				print count
				result = cur.fetchall()
				for r in result:
					print r

				conn.commit()
				cur.close()
				conn.close()

			except MySQLdb.Error,e:
     				print "Mysql Error %d: %s" % (e.args[0], e.args[1])


			'''
			self.wfile.write("<html><head><title>It works!</title></head>")
			self.wfile.write("<body><p>Test</p>")
			self.wfile.write("<body><p>Test again</p>")
			self.wfile.write("</body></html>")
			'''
		

if __name__ == '__main__':
	httpd = HTTPServer(server_address, myHandler)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
