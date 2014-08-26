# (TODO..) Generate the hashcode of all urls and titles, and "mod 1000" to seperate a number of
#          buckets, in order to eliminate duplicate urls and titles

import urllib
from HTMLParser import HTMLParser

store_html = 'res/url_'
store_homepage = 'res/home_.html'
store_topic = 'topic/all_topics.txt'
store_url = 'url/all_urls.txt'

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self, get_url, url):
        # call super constructor
        HTMLParser.__init__(self)
        self.get_url = get_url
        self.url = url
        self.found_a  = False

        self.found_h1 = False
        self.found_h2 = False
        self.found_h3 = False
        self.found_h4 = False
        self.found_h5 = False
        self.found_h6 = False

        self.found_li = False
        
        
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag, attrs
        if self.get_url == False:
            if tag == 'a':
                 self.found_a = True
            if tag == 'h1':
                self.found_h1 = True
            if tag == 'h2':
                self.found_h2 = True
            if tag == 'h3':
                self.found_h3 = True
            if tag == 'h4':
                 self.found_h4 = True
            if tag == 'h5':
                 self.found_h5 = True
            if tag == 'h6':
                 self.found_h6 = True
        else:
            if tag == 'li':
                self.found_li = True
            if tag == 'a' and self.found_li == True:
                self.found_a = True
                for attr in attrs:
                    if attr[0] == 'href':
                        if attr[1][0:7] == 'http://' and attr[1][-4:] != '.pdf'\
                             and attr[1][-4:] != '.asp': 
                            print '[INFO] href = ', attr[1]
                            with open(store_url, 'a') as writing_file:
                                writing_file.write(attr[1] + '\n');
                        elif attr[1][0:1] != '#' and attr[1][0:5] != 'https'\
                             and attr[1][0:] != '/':
                            if attr[1][0:1] == '/':
                                if self.url[7:].index('/') != (len(self.url[7:])-1):
                                    with open(store_url, 'a') as writing_file:
                                        writing_file.write('http://' + self.url[7:][:self.url[7:].index('/')] + attr[1] + '\n');
                                else:
                                    print '[INFO] href = ', attr[1]
                                    with open(store_url, 'a') as writing_file:
                                        writing_file.write(self.url + attr[1][1:] + '\n');


    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        if self.get_url == False:
            if tag == 'a':
                 self.found_a = False
            if tag == 'h1':
                self.found_h1 = False
            if tag == 'h2':
                self.found_h2 = False
            if tag == 'h3':
                self.found_h3 = False
            if tag == 'h4':
                self.found_h4 = False
            if tag == 'h5':
                self.found_h5 = False
            if tag == 'h6':
                self.found_h6 = False
        else:
            if tag == 'li':
                self.found_li = False
            if tag == 'a':
                self.found_a = False
        
    def handle_data(self, data):
        # print "Encountered some data  :", data
        if self.get_url == False:
            if (self.found_a == True and ( \
                    (self.found_h1 == True)\
                 or (self.found_h2 == True)\
                 or (self.found_h3 == True)\
                 or (self.found_h4 == True)\
                 or (self.found_h5 == True)\
                 or (self.found_h6 == True))):
                
                # "print" can only output ascii encoded normal String
                # ,so use "encode()" method to return ascii normal String.
                print '[INFO] Data = ', data.encode ('utf-8').strip()

                with open (store_topic, 'a') as writing_file:
                    # Use "encode()" method to return ascii normal String 
                    writing_file.write (data.encode('utf-8').strip())
                    writing_file.write ('\n');

        else:
            if self.found_li == True and self.found_a == True:
                # print 'Link data = ', data
                pass

    def handle_decl(self, data):
        # print "Decl     :", data
        pass

def main():

    # Clean the processing files
    open (store_url, 'w').close ()
    open (store_topic, 'w').close ()

    #url = raw_input('Enter an url : ')
    # if url[-1:] != '/':
    #    url += '/'
    # (DEBUGGING..)
    url = 'http://www.reuters.com/finance/markets/'

    # Generate a file from the url (replace the old ones if file existed)
    urllib.urlretrieve (url, store_homepage)

    # Make sure to use urlopen to open html file(unicode)
    homeHandle = urllib.urlopen (url)
    # "read()" return ascii encoded normal String(htmltxt)
    htmltxt = homeHandle.read ()
    homeHandle.close ()
    
    parser = MyHTMLParser (True, url)
    # "feed" method's parameter had better be unicode
    # ,so use decode('utf-8') to restore to unicode string.
    parser.feed (htmltxt.decode ('utf-8'))

    # read urls from the url recording file.
    i = 0;
    with open (store_url, 'r') as reading_file:
        for pageUrl in reading_file:
            store_html_path = store_html + str(i) + '.html'
            print '[INFO] Processing: ', pageUrl, ' to ', store_html_path

            fHandle = urllib.urlopen (pageUrl)
            # "read()" return ascii encoded normal String(htmltxt)
            htmltxt2 = fHandle.read ()
            
            # 'w' will overwrite the original file with a new one
            with open (store_html_path, 'w') as retPage:
                retPage.write (htmltxt2)

            parser = MyHTMLParser (False, url)
            # "feed" method's parameter had better be unicode
            # ,so use decode('utf-8') to restore to unicode string.
            parser.feed (htmltxt2.decode ('utf-8'))

            parser.close ()
            fHandle.close ()

            i += 1

if __name__ == '__main__' :
    main()

