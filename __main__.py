from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self):
        # call super constructor
        HTMLParser.__init__(self)
        self.found = False
        
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        if tag == 'p' and attrs == []:
            self.found = True
            print "Encountered a start tag:", tag, attrs

    def handle_endtag(self, tag):   
        pass
        #print "Encountered an end tag :", tag
        
    def handle_data(self, data):
        if self.found == True:
           print 'Data = ', data
           
           self.found = False
        # print "Encountered some data  :", data

    def handle_comment(self, data):
        pass

# filter an article form html file to find the trending topic
def main():
    res_path = 'res/'
    file_name = 'Miss Bumbum 2014 Contestants Hope To Have Brazil\'s Best Butt'
    htmltxt = ''
    with open(res_path + file_name + '.html', 'r') as reading_file:
        htmltxt = reading_file.read()
        # print htmltxt

    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(htmltxt)

if __name__ == '__main__' :
    main()
