from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        if tag == 'h1':
        	print "Encountered a start tag:", tag, attrs

    def handle_endtag(self, tag):
    	pass
        #print "Encountered an end tag :", tag
    def handle_data(self, data):
    	pass
        # print "Encountered some data  :", data



# filter an article form html file to find the trending topic
def main():
	path = 'res/'
	file_name = 'Miss Bumbum 2014 Contestants Hope To Have Brazil\'s Best Butt'
	htmltxt = ''
	with open(path+file_name+'.html', 'r') as reading_file:
		htmltxt = reading_file.read()

	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	parser.feed(htmltxt)

if __name__ == '__main__' :
	main()
