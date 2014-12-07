from HTMLParser import HTMLParser

txt_path = 'txt/'
res_path = 'res/'
filter_path = 'filter/'

txt_file_name01 = 'Miss Bumbum 2014 Contestants Hope To Have Brazil\'s Best Butt'
res_file_name01 = 'Miss Bumbum 2014 Contestants Hope To Have Brazil\'s Best Butt'
filter_file_name01 = 'Miss Bumbum 2014 Contestants Hope To Have Brazil\'s Best Butt'

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
            # print "Encountered a start tag:", tag, attrs

    def handle_endtag(self, tag):   
        pass
        #print "Encountered an end tag :", tag
        
    def handle_data(self, data):
        if self.found == True:
            
            # print 'Data = ', data 
            with open(txt_path + txt_file_name01 + '.txt', 'a+') as writing_file:
                writing_file.write(data);

            self.found = False
        # print "Encountered some data  :", data

    def handle_comment(self, data):
        pass

def searchKeyword():
    with open(txt_path + txt_file_name01 + '.txt', 'r') as reading_file:
        for line in reading_file:
            word_list = []
            for part in line.split():
                if part in word_list:
                    print 'keyword = ' + part
                    with open(filter_path + filter_file_name01 + '.txt', 'a+') as filter_file:
                        filter_file.write(part + '\n')
                word_list.append(part)


# filter an article form html file to find the trending topic
def main():
    # keyword = raw_input('Enter a keyword : ')
    htmltxt = ''
    with open(res_path + res_file_name01 + '.html', 'r') as reading_file:
        htmltxt = reading_file.read()
        # print htmltxt

    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(htmltxt)
    searchKeyword()
    

if __name__ == '__main__' :
    main()
