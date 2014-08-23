import urllib
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

store_html = 'res/url_'
store_homepage = 'res/home_.html'
strore_path = 'topic/all_topics.txt'
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
                            # print 'href = ', attr[1]
                            with open(store_url, 'a+') as writing_file:
                                writing_file.write(attr[1] + '\n');
                        elif attr[1][0:1] != '#' and attr[1][0:5] != 'https'\
                             and attr[1][0:] != '/': 
                            if attr[1][0:1] == '/':
                                # print 'href = ', attr[1]
                                with open(store_url, 'a+') as writing_file:
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
            if (self.found_h1 == True and self.found_a == True)\
                 or (self.found_h2 == True and self.found_a == True)\
                 or (self.found_h3 == True and self.found_a == True)\
                 or (self.found_h4 == True and self.found_a == True)\
                 or (self.found_h5 == True and self.found_a == True)\
                 or (self.found_h6 == True and self.found_a == True):
                
                data = data.strip ()
                print 'Data = ', data 

                with open(strore_path, 'a+') as writing_file:
                    writing_file.write(data + '\n');
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
    url = raw_input('Enter an url : ')
    if url[-1:] != '/':
        url += '/'
    # url = 'http://www.vocativ.com/'
    result = urllib.urlretrieve(url, store_homepage)
    # print result
    htmltxt = ''    
    with open(store_homepage, 'r') as reading_file:
        htmltxt = reading_file.read()
        # print htmltxt
    parser = MyHTMLParser(True, url)
    parser.feed(htmltxt)

    urls = []
    with open(store_url, 'r') as reading_file:
        for line in reading_file:
            urls.append(line)

    for i in range(0, len(urls)):
        store_html_path = store_html + '0' + str(i) + '.html'
        # Will replace the old ones if file name is the same
        result2 = urllib.urlretrieve(urls[i], store_html_path)
        # print result2
        htmltxt2 = unicode ('')
        with open(store_html_path, 'r') as reading_file:
            htmltxt2 = unicode (reading_file.read(), errors = 'ignore')
            # (STILL FIGURING OUT..) Can't assign "encoding = 'utf-8'", 
            # htmltxt2 = unicode (reading_file.read(), encoding = 'utf-8', errors = 'ignore')
            # print htmltxt2
        # Use try catch for just in case
        try:
            parser = MyHTMLParser(False, url)
            parser.feed (htmltxt2)
            parser.close ()
        except:
           print htmltxt2
           # (FOR DEBUGGING..)
           return

if __name__ == '__main__' :
    main()

