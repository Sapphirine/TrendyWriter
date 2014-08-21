import urllib
from HTMLParser import HTMLParser

# specify url to fetch
# url = 'http://www.upworthy.com/'
# save path and file name
local = 'res/url_01.html'
strore_path = 'topic/all_topic.txt'

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self):
        # call super constructor
        HTMLParser.__init__(self)
        self.found_a  = False
        self.found_h1 = False
        self.found_h2 = False
        self.found_h3 = False
        self.found_h4 = False
        self.found_h5 = False
        self.found_h6 = False
        
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag, attrs
        if tag == 'a':
         	self.found_a = True
     	if tag == 'h1':
        	self.found_h2 = True
        if tag == 'h2':
        	self.found_h2 = True
        if tag == 'h3':
            self.found_h2 = True
        if tag == 'h4':
         	self.found_h3 = True
     	if tag == 'h5':
         	self.found_h3 = True
     	if tag == 'h6':
         	self.found_h3 = True


    def handle_endtag(self, tag):
    	#print "Encountered an end tag :", tag
    	if tag == 'a':
         	self.found_a = False
     	if tag == 'h1':
        	self.found_h2 = False
        if tag == 'h2':
        	self.found_h2 = False
        if tag == 'h3':
            self.found_h2 = False
        if tag == 'h4':
         	self.found_h3 = False
     	if tag == 'h5':
         	self.found_h3 = False
     	if tag == 'h6':
         	self.found_h3 = False
        
    def handle_data(self, data):
    	# print "Encountered some data  :", data
        if (self.found_h1 == True and self.found_a == True)\
      	   or (self.found_h2 == True and self.found_a == True)\
      	   or (self.found_h3 == True and self.found_a == True)\
      	   or (self.found_h4 == True and self.found_a == True)\
      	   or (self.found_h5 == True and self.found_a == True)\
      	   or (self.found_h6 == True and self.found_a == True):
            print 'Data = ', data 

            # TODO..
            #data.join()
            with open(strore_path, 'a+') as writing_file:
                writing_file.write(data + '\n');

    def handle_comment(self, data):
        pass


def main():
	url = raw_input('Enter a url : ')
	result = urllib.urlretrieve(url, local)
	# print result
	htmltxt = ''
	with open(local, 'r') as reading_file:
		htmltxt = reading_file.read()
		# print htmltxt

	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	parser.feed(htmltxt)

if __name__ == '__main__' :
	main()

