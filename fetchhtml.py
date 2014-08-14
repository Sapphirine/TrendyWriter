import urllib

# specify url to fetch
url = 'http://weblogs.asp.net/dwahlin/video-tutorial-angularjs-fundamentals-in-60-ish-minutes'
# save path and file name
local = 'res/url01.html'

result = urllib.urlretrieve(url, local)
print result