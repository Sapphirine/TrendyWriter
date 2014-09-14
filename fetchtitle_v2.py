#!/usr/bin/env python2.6

"""
[TODO]
(0) Implement Debug Mode.
(1) Duplication of data(url?) still exists.
(2) Filter the data that contains html original text(i.e. html tag).
(3) To process large-scale data efficiently, it is necessary.
to generate the hashcode of all urls and titles, and "mod 1024" to
seperate a number of buckets, in order to eliminate duplicate urls 
and titles.
"""

"""
[DEBUG]
(step 1) python fetchtitle_v2.py | tee debug.txt
(step 2) (only if necessary) grep 'ERROR' debug.txt > error.txt
"""

def welcome_text():
    print ""
    print "================================="
    print "Fetch URL and title from Web tool"
    print "================================="
    print "--------------------------------------------------------------"
    print "[DEVELOPER MODE]"
    print "Step 1: python fetchtitle_v2.py | tee debug.txt"
    print "Step 2: (only if necessary) grep 'ERROR' debug.txt > error.txt"
    print "--------------------------------------------------------------"

import urllib
from HTMLParser import HTMLParser

from htmlentitydefs import name2codepoint 

# store path variables:
store_html = 'res/url_'
store_homepage = 'res/home_.html'
store_topic = 'topic/all_topics.txt'
store_url = 'url/all_urls.txt'

# debug variables:
DEBUG = True
debug_url = 'http://www.huffingtonpost.com/science/'
debug_storepath = 'debug/debug_page.html'

# (note) Create a subclass and override the handler methods.
class MyHTMLParser(HTMLParser): 
    url_list = []
    topic_list = []

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
                        url = attr[1] 
                        if url[-1:] != '/':
                            url += '/'
                        # If the url starting with 'http://'.
                        if url[0:7] == 'http://' and url[-4:] != '.pdf'\
                         and url[-4:] != '.asp': 
                            # Eliminate duplicated url.
                            if not url in MyHTMLParser.url_list:
                                print '[INFO] href = ', url
                                with open(store_url, 'a') as writing_file:
                                    writing_file.write(url + '\n')
                                MyHTMLParser.url_list.append(url + '/')  
                            else:
                                print '[DUPLICATE] href = ', url  
                        # If other url starting without 'http://'.
                        elif url[0:1] != '#' and url[0:5] != 'https'\
                         and url[0:] != '/' and url[0:10] != 'javascript':
                            # If the url is a absolute path.
                            if url[0:1] == '/':
                                # If '/' is not the final character.
                                if self.url[7:].index('/') != (len(self.url[7:])-1):
                                    if not url in  MyHTMLParser.url_list:
                                        print '[INFO] href = ', url
                                        with open(store_url, 'a') as writing_file:
                                            writing_file.write('http://' + self.url[7:][:self.url[7:].index('/')]\
                                             + url + '\n')
                                        MyHTMLParser.url_list.append(url)
                                    else:
                                        print '[DUPLICATE] href = ', url
                                # If '/' is the final character.
                                else:
                                    if not url in  MyHTMLParser.url_list:
                                        print '[INFO] href = ', url
                                        with open(store_url, 'a') as writing_file:
                                            writing_file.write(self.url + url[1:] + '\n')
                                        MyHTMLParser.url_list.append(url)
                                    else:
                                        print '[DUPLICATE] href = ', url
                            # If the url is a relative path.
                            else:
                                if not url in  MyHTMLParser.url_list:
                                    print '[INFO] href = ', url
                                    with open(store_url, 'a') as writing_file:
                                        writing_file.write(self.url + url + '\n')
                                    MyHTMLParser.url_list.append(url)
                                else:
                                    print '[DUPLICATE] href = ', url

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
            if (self.found_a == True and (\
                (self.found_h1 == True)\
             or (self.found_h2 == True)\
             or (self.found_h3 == True)\
             or (self.found_h4 == True)\
             or (self.found_h5 == True)\
             or (self.found_h6 == True))):
                # Eliminate duplicated topics.
                if not data.encode ('utf-8').strip() in MyHTMLParser.topic_list:
                    # The "print" can only output Ascii encoded normal String
                    # ,so use "encode()" method to return Ascii normal String.
                    print '[INFO] Data = ', data.encode ('utf-8').strip()

                    with open (store_topic, 'a') as writing_file:
                        # Use "encode()" method to return Ascii normal String 
                        writing_file.write (data.encode('utf-8').strip())
                        writing_file.write ('\n') 
                    MyHTMLParser.topic_list.append(data.encode ('utf-8').strip())
                else:
                    print '[DUPLICATE] Data = ', data.encode ('utf-8').strip()
        else:
            if self.found_li == True and self.found_a == True:
                # print 'Link data = ', data
                pass

    def handle_decl(self, data):
        # print "Decl     :", data
        pass

    def handle_charref(self, name): 

        if name.startswith('x'): 
            num = int(name[1:], 16) 
        else: 
            num = int(name, 10) 
        
        #print 'char:', repr(unichr(num)) 
        name = ' '
        self.handle_entityref (name)

    def handle_entityref(self, name): 
        #print 'char:', unichr (name2codepoint[name]).encode ('utf-8') 
        #self.handle_data (self.unescape('&#{};'.format(name)))
        name = ''
        self.handle_data (name)

def main():
    welcome_text()
    if DEBUG:
        urllib.urlretrieve (debug_url, debug_storepath)

        debugHandle = urllib.urlopen (debug_url)
        debug_htmltxt = debugHandle.read ()
        debugHandle.close()

        url_parser = MyHTMLParser (False, debug_url)
        url_parser.feed(debug_htmltxt.decode('utf-8'))
        url_parser.close()

    else:
        # Clean the to-be-processing files.
        open (store_url, 'w').close ()
        open (store_topic, 'w').close ()

        url = raw_input('Enter an url : ')
        if url[-1:] != '/':
           url += '/'

        # Generate a file from the specified URL (replace the old ones if file existed).
        urllib.urlretrieve (url, store_homepage)

        # Make sure to use urlopen to open html file(Unicode).
        homeHandle = urllib.urlopen (url)
        # Method "read()" return Ascii encoded normal String(htmltxt).
        htmltxt = homeHandle.read ()
        homeHandle.close ()
        
        url_parser = MyHTMLParser (True, url)
        # The "feed" method's parameter had better be Unicode
        # ,so use decode('utf-8') to restore to Unicode string.
        url_parser.feed (htmltxt.decode ('utf-8'))
        url_parser.close()

        # Read each url from the url recording file.
        i = 0 
        with open (store_url, 'r') as reading_file:
            for pageUrl in reading_file:
                store_html_path = store_html + str(i) + '.html'
                print '[INFO] Processing: ', pageUrl, ' to ', store_html_path

                # Read html text from Web.
                fHandle = urllib.urlopen (pageUrl)
                # "read()" return Ascii encoded normal String(htmltxt2)
                htmltxt2 = fHandle.read ()
                
                # Store reading html text to a file.
                # (note) Parameter 'w' will overwrite the original file with a new one.
                with open (store_html_path, 'w') as retPage:
                    retPage.write (htmltxt2)

                parser = MyHTMLParser (False, url)
                # The "feed" method's parameter had better be Unicode
                # ,so use decode('utf-8') to restore to Unicode string.
                try:
                    parser.feed (htmltxt2.decode ('utf-8'))
                    
                except Exception:
                    print '[ERROR] Parsing Error: ', pageUrl , ' in ', store_html_path
                    parser.feed (unicode(htmltxt2, errors='ignore'))
                parser.close ()
                fHandle.close ()
                i += 1

if __name__ == '__main__' :
    main()

