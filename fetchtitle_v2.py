#!/usr/bin/env python2.6

""" @package default
[TODO]
(1) Filter the data that contains html original text(i.e. html tag), using formal way.
(2) To process large-scale data efficiently:
To generate the hashCode of all urls and titles, and "mod 1024" to separate into 1024 buckets, and avoid duplicate
collision of data as much as possible.
(3) Retrieve data from Ajax as well.
(4) Retrieve data inside the tag <i> and <b>

More details..
"""

"""
[DEBUG]
(step 1) python fetchtitle_v2.py | tee debug.txt
(step 2) (only if necessary) grep 'ERROR' debug.txt > error.txt
"""

import urllib
from HTMLParser import HTMLParser
# from htmlentitydefs import name2codepoint


# store path variables:
store_html = 'res/url_'
store_homepage = 'res/home_.html'
store_topic = 'topic/all_topics.txt'
store_url = 'url/all_urls.txt'

# debug variables:
DEBUG = False
debug_url = 'http://www.huffingtonpost.com/syndication/'
debug_storepath = 'debug/debug_page.html'


def welcome_text():
    print ''
    print '========================================================='
    print '            Crawl URL and title from Web tool            '
    print '========================================================='
    print '---------------------------------------------------------'
    print '[DEVELOPER MODE]'
    print 'Step 1: python fetchtitle_v2.py | tee debug.txt'
    print 'Step 2: (IF NECESSARY) grep "ERROR" debug.txt > error.txt'
    print '---------------------------------------------------------'

class CrawlTitlesAndUrls(HTMLParser):
    """
    MyHTMLParser class:

    Subclass HTMLParser, crawl urls and titles (support all character encoding) and eliminate all duplicates.
    """
    url_list = []
    topic_list = []

    def __init__(self, get_url, url):
        """ (self, bool, str)
        MyHTMLParser class constructor:

        :param get_url:  Determine whether crawl urls or titles.
        """
        # call super constructor
        HTMLParser.__init__(self)
        self.get_url = get_url
        self.url = url
        self.found_a = False
        self.found_h1 = False
        self.found_h2 = False
        self.found_h3 = False
        self.found_h4 = False
        self.found_h5 = False
        self.found_h6 = False
        self.found_li = False

    def handle_starttag(self, tag, attrs):
        if not self.get_url:
            if tag == 'a':
                self.found_a = True
            elif tag == 'h1':
                self.found_h1 = True
            elif tag == 'h2':
                self.found_h2 = True
            elif tag == 'h3':
                self.found_h3 = True
            elif tag == 'h4':
                self.found_h4 = True
            elif tag == 'h5':
                self.found_h5 = True
            elif tag == 'h6':
                self.found_h6 = True
        elif self.get_url:
            if tag == 'li':
                self.found_li = True
            elif tag == 'a' and self.found_li:
                self.found_a = True
                for attr in attrs:
                    if attr[0] == 'href':
                        url = attr[1]
                        if url[-1:] != '/':
                            url += '/'
                        # If the url starting with 'http://'.
                        if url[0:7] == 'http://' and url[-4:] != '.pdf' \
                                and url[-4:] != '.asp':
                            # Eliminate duplicated url.
                            if not url in CrawlTitlesAndUrls.url_list:
                                print '[INFO] href = ', url
                                with open(store_url, 'a') as writing_file:
                                    writing_file.write(url + '\n')
                                CrawlTitlesAndUrls.url_list.append(url + '/')
                            else:
                                print '[DUPLICATE] href = ', url
                                # If other url starting without 'http://'.
                        elif url[0:1] != '#' and url[0:5] != 'https' \
                                and url[0:] != '/' and url[0:10] != 'javascript':
                            # If the url is a absolute path.
                            if url[0:1] == '/':
                                # If '/' is not the final character.
                                if self.url[7:].index('/') != (len(self.url[7:]) - 1):
                                    if not url in CrawlTitlesAndUrls.url_list:
                                        print '[INFO] href = ', url
                                        with open(store_url, 'a') as writing_file:
                                            writing_file.write('http://' + self.url[7:][:self.url[7:].index('/')]
                                                               + url + '\n')
                                        CrawlTitlesAndUrls.url_list.append(url)
                                    else:
                                        print '[DUPLICATE] href = ', url
                                # If '/' is the final character.
                                else:
                                    if not url in CrawlTitlesAndUrls.url_list:
                                        print '[INFO] href = ', url
                                        with open(store_url, 'a') as writing_file:
                                            writing_file.write(self.url + url[1:] + '\n')
                                        CrawlTitlesAndUrls.url_list.append(url)
                                    else:
                                        print '[DUPLICATE] href = ', url
                            # If the url is a relative path.
                            else:
                                if not url in CrawlTitlesAndUrls.url_list:
                                    print '[INFO] href = ', url
                                    with open(store_url, 'a') as writing_file:
                                        writing_file.write(self.url + url + '\n')
                                    CrawlTitlesAndUrls.url_list.append(url)
                                else:
                                    print '[DUPLICATE] href = ', url

    def handle_endtag(self, tag):
        if not self.get_url:
            if tag == 'a':
                self.found_a = False
            elif tag == 'h1':
                self.found_h1 = False
            elif tag == 'h2':
                self.found_h2 = False
            elif tag == 'h3':
                self.found_h3 = False
            elif tag == 'h4':
                self.found_h4 = False
            elif tag == 'h5':
                self.found_h5 = False
            elif tag == 'h6':
                self.found_h6 = False
        elif self.get_url:
            if tag == 'li':
                self.found_li = False
            elif tag == 'a':
                self.found_a = False

    def handle_data(self, data):
        if DEBUG or CrawlTitlesAndUrls.filter(data):
            if not self.get_url:
                # @formatter:off
                if self.found_a and (
                   self.found_h1 or self.found_h2 or
                   self.found_h3 or self.found_h4 or
                   self.found_h5 or self.found_h6):
                    # Eliminate duplicated topics.
                    # @formatter:on
                    if not data.encode('utf-8').strip() in CrawlTitlesAndUrls.topic_list:
                        # The "print" can only output Ascii encoded normal Str
                        # ,so use "encode()" method to return Ascii normal Str.
                        print '[INFO] Data = ', data.encode('utf-8').strip()
                        with open(store_topic, 'a') as writing_file:
                            # Use "encode()" method to return Ascii normal Str
                            writing_file.write(data.encode('utf-8').strip())
                            writing_file.write('\n')
                        CrawlTitlesAndUrls.topic_list.append(data.encode('utf-8').strip())
                    else:
                        print '[DUPLICATE] Data = ', data.encode('utf-8').strip()

    def handle_decl(self, data):
        print '[INFO] DOCTYPE = ', data

    def handle_charref(self, name):
        # Print the decimal number of special character in HTML(i.e. '&#number' or '#name').
        print '[INFO] special character = ', name
        self.handle_entityref(name)

    def handle_entityref(self, name):
        # Print the symbol of special character in HTML(i.e. '&#number' or '#name').
        self.handle_data(self.unescape('&#{};'.format(name)))

    @staticmethod
    def filter(origin_data):
        # Eliminate general topic word.
        if len(origin_data.split()) > 1:
            # Eliminate words like "more politics", "more health", etc.
            if (origin_data.split()[0].lower() == 'more') and (len(origin_data.split()) <= 2):
                return False
            # Eliminate JavaScript codes
            elif len(origin_data.split()) > 30:
                return False
            else:
                return True
        # Keep one word, which might be a person's name.
        elif len(origin_data.split()) == 1 and origin_data.split()[0][0:1].isupper() \
                and origin_data.split()[0][1:].islower():
            return True
        else:
            return False


def main():
    welcome_text()
    if DEBUG:
        urllib.urlretrieve(debug_url, debug_storepath)

        debug_handler = urllib.urlopen(debug_url)
        debug_htmltxt = debug_handler.read()
        debug_htmltxt = debug_htmltxt.replace('&#', ' ')
        debug_handler.close()

        url_parser = CrawlTitlesAndUrls(False, debug_url)
        url_parser.feed(debug_htmltxt.decode('utf-8'))
        # url_parser.feed(debug_htmltxt2.decode('utf-8'))
        url_parser.close()
    else:
        # Clean the to-process files.
        open(store_url, 'w').close()
        open(store_topic, 'w').close()

        url = raw_input('Enter an url : ')
        if url[-1:] != '/':
            url += '/'

        # Generate a ORIGINAL file from the specified URL (replace the old ones if file existed).
        urllib.urlretrieve(url, store_homepage)

        # Make sure to use urlopen to open html file(Unicode).
        home_handler = urllib.urlopen(url)
        # Method "read()" return Ascii encoded normal Str(htmltxt).
        htmltxt = home_handler.read()
        home_handler.close()

        url_parser = CrawlTitlesAndUrls(True, url)
        # The "feed" method's parameter had better be Unicode
        # ,so use decode('utf-8') to restore to Unicode string.
        url_parser.feed(htmltxt.decode('utf-8'))
        url_parser.close()

        # Read each url from the url recording file.
        i = 0
        with open(store_url, 'r') as reading_file:
            for pageUrl in reading_file:
                store_html_path = store_html + str(i) + '.html'
                print '[INFO] Processing: ', pageUrl, ' to ', store_html_path

                # Read html text from Web.
                fetch_handler = urllib.urlopen(pageUrl)
                # "read()" return Ascii encoded normal Str(htmltxt2)
                htmltxt2 = fetch_handler.read()

                # (TMP) TEMPORARY SOLUTION..
                # @formatter:off
                # (TODO) Still need to get rid of  number and(or) ';' following by the next word without any space..
                htmltxt2 = htmltxt2.replace('&#', ' ').replace(';', ' ').replace('039', ' ').replace('8217', ' ')\
                                   .replace('039', ' ').replace('8217', ' ').replace('8216', ' ').replace('39', ' ')
                # @formatter:on
                # (NOTE) Parameter 'w' will overwrite the original file with a new one.
                # Store reading html text to a file.
                with open(store_html_path, 'w') as retPage:
                    retPage.write(htmltxt2)

                parser = CrawlTitlesAndUrls(False, url)
                # The "feed" method's parameter had better be Unicode
                # ,so use decode('utf-8') to restore to Unicode string.
                try:
                    parser.feed(htmltxt2.decode('utf-8'))
                except Exception:
                    print '[ERROR] Parsing Error: ', pageUrl, ' in ', store_html_path
                    parser.feed(unicode(htmltxt2, encoding='ISO-8859-1', errors='ignore'))
                parser.close()
                fetch_handler.close()
                i += 1


if __name__ == '__main__':
    main()