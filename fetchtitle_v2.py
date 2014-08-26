# (TODO..) Make sure to get all urls within a webpage including relive path and absolute path
#          (including start with a '/')
# (TODO..) Generate the hashcode of all urls and "mod 1000" to seperate a number of buckets

import urllib
from HTMLParser import HTMLParser
# from htmlentitydefs import name2codepoint

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
                        if attr[1][0:7] == 'http://':
                            print 'href = ', attr[1]
                            with open(store_url, 'a') as writing_file:
                                writing_file.write(attr[1] + '\n');
                        elif attr[1][0:1] != '#' and attr[1][0:5] != 'https'\
                             and attr[1][0:] != '/': 
                            if attr[1][0:1] == '/':
                                print 'href = ', attr[1]
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
                
                #print 'Original Data = ', data
                #data = unicode (data.strip ())
                print 'Data = ', data.strip().decode ('utf-8', errors = 'ignore')

                with open (store_topic, 'a') as writing_file:
                    writing_file.write (data)
                    writing_file.write ('\n'.encode ('utf-8'));

        else:
            if self.found_li == True and self.found_a == True:
                # print 'Link data = ', data
                pass

    def handle_decl(self, data):
        # print "Decl     :", data
        pass

    # def handle_comment(self, data):
    #     if self.get_url == False:
    #         pass
    #     else:
    #         pass

    # def handle_entityref(self, name):
    #     c = unichr(name2codepoint[name])
    #     print "Named ent:", c
    # def handle_charref(self, name):
    #     if name.startswith('x'):
    #         c = unichr(int(name[1:], 16))
    #     else:
    #         c = unichr(int(name))
    #     print "Num ent  :", c


def main():

    # clean the processing file.
    open (store_url, 'w').close ()
    open (store_topic, 'w').close ()

    #url = raw_input('Enter an url : ')
    #if url[-1:] != '/':
    #    url += '/'
    url = 'http://www.reuters.com/'
    urllib.urlretrieve (url, store_homepage)
    # htmltxt = unicode ('')

    homeHandle = urllib.urlopen (url)
    htmltxt = homeHandle.read ()
    homeHandle.close ()
    
    parser = MyHTMLParser (True, url)
    parser.feed (htmltxt.decode ('utf-8'))

    # read urls from the url recording file.
    #urls = []
    i = 0;

    with open (store_url, 'r') as reading_file:
        for pageUrl in reading_file:

            # Will replace the old ones if file name is the same
            store_html_path = store_html + str(i) + '.html'
            print 'Processing: ', pageUrl, ' to ', store_html_path

            fHandle = urllib.urlopen (pageUrl)
            htmltxt2 = fHandle.read ()

            try:
                htmltxt2.decode ('utf-8')
            except:
                print '[ERROR] Decode error: ' + pageUrl
                continue
            
            with open (store_html_path, 'w') as retPage:
                retPage.write (htmltxt2)


            parser = MyHTMLParser (False, url)

            try:
                parser.feed (htmltxt2)
            except:
                print '[ERROR] Parsing error: ' + pageUrl
                continue

            parser.close ()
            fHandle.close ()

            i += 1

if __name__ == '__main__' :
    main()

