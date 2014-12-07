# generic imports
import sys
import time
import shutil
import urllib.request
from subprocess import call


# HTML parser implementation
from html.parser import HTMLParser

class MainPageParser (HTMLParser):
    # data members
    m_isInVideoArea = False
    
    # data members for multi-page
    m_isInPageArea  = False
    m_isMultiPageEnabled = False
    m_isInCurrentPage = False
    
    m_foundVideoList = list()
    m_foundPageList  = list()
    m_foundEpsNameList = list()
        
    # Methods
    def __init__ (self, vidList, nameList, pageList):
        HTMLParser.__init__ (self)                
        self.m_foundVideoList.append (vidList)
        self.m_foundPageList.append (pageList)
        self.m_foundEpsNameList.append (nameList)
        
    def handle_starttag (self, tag, attrs):
        if tag == 'a':
            if self.m_isInVideoArea == True:             
                for name, value in attrs:                
                    # Get the real data!
                    if name == 'href':
                        try:
                            self.m_foundVideoList[0].index (value)
                        except ValueError:
                            # new episode found, added to the list
                            self.m_foundVideoList[0].append (value)
                            # print (value)
                        except:
                            raise                            
                            
            elif self.m_isInPageArea == True:                
                b_skipTitle = False;                
                for name, value in attrs:
                    if name == 'title':
                        b_skipTitle = True;
                
                for name, value in attrs:                    
                    if name == 'href':
                        if b_skipTitle == False:
                            try:
                                self.m_foundPageList[0].index (value)                                    
                            except ValueError:
                                self.m_foundPageList[0].append (value)
                            except:
                                raise
                                                                                                                    
        elif tag == 'ul':            
            # check if we are in the video link sections
            for name, value in attrs:
                if name == 'class' and value == 'video':                    
                    self.m_isInVideoArea = True
                    
        elif tag == 'div':                    
            for name, value in attrs:                
                # handle multi-page behaviors
                if name == 'class' and value == 'pagination':
                    self.m_isMultiPageEnabled = True
                    self.m_isInPageArea = True
        
        elif tag == 'span':
            if self.m_isMultiPageEnabled == True:
                for name, value in attrs:
                    if name == 'class' and value == 'current':
                        self.m_isInCurrentPage = True
                    
    def handle_endtag (self, tag):                        
        if tag == 'ul' and self.m_isInVideoArea == True:
            self.m_isInVideoArea = False
            self.m_foundVideoList[0].reverse ()            
                    
        elif tag == 'div' and self.m_isInPageArea == True:    
            self.m_isInPageArea = False
            self.m_foundPageList[0].reverse ()
                
        elif tag == 'span' and self.m_isInCurrentPage == True:
            self.m_isInCurrentPage = False
            
    # inherited method -> used to extract episode info
    def handle_data (self, data):
        if self.m_isInCurrentPage == True:
            try:
                self.m_foundPageList[0].index ("USER_URL")
            except ValueError:
                self.m_foundPageList[0].append ("USER_URL")                        
            except:
                raise
        return
                
    # customized method -> customer can use it to query the multipage scenario
    def isMultiPageSeries (self):
        return self.m_isMultiPageEnabled
                                                                    
# class MainPageParser (end)

class EpisodePageParser (HTMLParser):
    # properties
    m_epiPath = ""
    m_foundEpiPath = False

    # methods
    def __init__ (self):
        HTMLParser.__init__ (self)                    
                
    def handle_starttag (self, tag, attrs):         
        # print (tag, attrs)
        if tag == "source":             
            for name, value in attrs:
                if name == 'src':
                    if self.m_foundEpiPath == False :
                        self.m_epiPath = value
                    else :
                        sys.exit ("Holly Shit - 2 Paths are found")
                    
                    # print (value)

    def retrieve_epiPath (self):
        return self.m_epiPath
# class EpisodePageParser (end)  

# Utility func
def retrieve_files_single_idx_page (a_foundPages):      
    idxVidPages = 1

    for x in a_foundPages:
        print ("Fetching Episode ", idxVidPages, " @ http://v.ck101.com" + x)
        # time.sleep (15)
        urlData = urllib.request.urlopen ("http://v.ck101.com" + x)
        urlContent = urlData.read().decode ('utf-8')
        urlData.close()

        epParser = EpisodePageParser ()
        epParser.feed (urlContent)
        
        # actual fetch operations (call curl)
        stdLogFD = open ("__stdoutlog"+str(idxVidPages)+".txt", "w")
        errLogFD = open ("__stderrlog"+str(idxVidPages)+".txt", "w")
            
        # print ("Fetching the video file...")
        # ret_code = call (["curl", epParser.retrieve_epiPath(), "-o", ("ep"+str(idxVidPages)+".mp4")], stdout = stdLogFD, stderr = errLogFD)
        # print ("curl", epParser.retrieve_epiPath(), "-o", ("ep"+str(idxVidPages)+".mp4"))
        idxVidPages += 1
        
        stdLogFD.close ()
        errLogFD.close ()    
        
        # TODO: need to check if the file transfer works or not
        
        # sleep 30 minutes to do another episode -> preventing from being blocked by ck101.com
        # time.sleep (30*60)                    
                                                    
# main program starts here
# Preliminary checks
# check 1. check PY version
if sys.hexversion < 0x03030000:
    sys.exit ("PYTHON version is too old - needs ")

# check 2. check curl
check_curl_exist = shutil.which ("curl")
if check_curl_exist == "" :
    sys.exit ("You need to install curl to run this script");

# Let's go
foundVidPages = list ()
foundEpsNames = list ()
foundIdxPages = list ()

print ("Fetching: ", sys.argv[1])

# Fetch the user defined url contents
# time.sleep (15)
urlData = urllib.request.urlopen (sys.argv[1])
urlContent = urlData.read().decode ('utf-8')
urlData.close()

# Parsing the user defined url contents & retrieve the episode pages
mainPage = MainPageParser (foundVidPages, foundEpsNames, foundIdxPages)
mainPage.feed (urlContent)

# debug
print (foundIdxPages)

if mainPage.isMultiPageSeries () == True :
    
    print ("Multi Page Mode");    
    # do multiple page processing    
    curProcessPage = 0
        
    for page in foundIdxPages:                
        if page == 'USER_URL':            
            print (sys.argv[1])
            print (foundVidPages)   
            retrieve_files_single_idx_page (foundVidPages)            
        else:
            vidIdxPage = "http://v.ck101.com" + page      
            print (vidIdxPage)              
                    
            # stupid variable name. Forgive me, God.
            foo_foundVidPages = list()
            foo_foundIdxPages = list()
                    
            try:
                #time.sleep (15)
                urlData = urllib.request.urlopen (vidIdxPage)                
                urlContent = urlData.read().decode ('utf-8')
                urlData.close()
            except:
                raise

            # Parsing the user defined url contents & retrieve the episode pages
            foo_mainPage = MainPageParser (foo_foundVidPages, foo_foundIdxPages)
            foo_mainPage.feed (urlContent)  
            
            print (foo_foundVidPages)   
                
            retrieve_files_single_idx_page (foo_foundVidPages)                
            curProcessPage = curProcessPage + 1                
else:
    # For each episode pages, fetch the video data
    # print (foundVidPages)
    print ("Single Page Mode");
    retrieve_files_single_idx_page (foundVidPages)

    
