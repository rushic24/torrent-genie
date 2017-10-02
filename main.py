import urllib2, os, sys
from itertools import izip
from bs4 import BeautifulSoup
import re
import pprint

def get_mirrors():
    proxy_list_url = 'https://thepiratebay-proxylist.org/'
    try:
        print 'Connecting to proxy list...'
        req = urllib2.Request(proxy_list_url, headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen( req ).read()
        soup = BeautifulSoup(con, 'html.parser')
        plist=[]
        productDivs = soup.findAll('td', attrs={'title' : 'URL'})
        for div in productDivs:
            tmp= div.find('a')['href']
            print tmp
            plist.append(tmp)
            
        try_connections (plist)
    except Exception as e:
        print e

def try_connections(proxy_list_urls):
    for url in proxy_list_urls:
        try:
            print 'Trying to connect to '+ url
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            con = urllib2.urlopen(req)
            print 'Connected succssfuly to '+ url

            create_query(url)
            
            break
        except(urllib2.HTTPError):
            print 'Could not connect to proxy list'


def create_query(ur):
    user_input = raw_input('Search query:\n')
    q = user_input.replace(" ", "+")
    global url
    url = ur + "/s/?q="+q+"&page=0&orderby=99"
    


def fetchLinkAndTitle():
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req).read()
    global soup
    soup = BeautifulSoup(con, 'html.parser')
    productDivs = soup.findAll('div', attrs={'class' : 'detName'})
    i=0
    sds=[]
    title=[]
    hrefs=[]
    for div in productDivs:
        #print div.find('a')['title'][12:]
        title.append(div.find('a')['title'][12:])
        hrefs.append("https://thebay.tv"+(div.find('a')['href']))
        i=i+1
    print i
    #print title[0]
    #print hrefs[0]
    return title,hrefs

def createdict(title,sl,uploaded,link):
    dic={}
    dic["title"]=title
    dic["seeders , leechers "]=sl
    dic["uploaded"]=uploaded
    dic["link"]=link
    return dic
def make_dict_list(t_ar,sl_ar,up_ar,link_ar):
    mlist=[]
    for i in range(len(t_ar)):
        dic=createdict(t_ar[i],sl_ar[i],up_ar[i],link_ar[i])
        mlist.append(dic)
    return mlist

def myprint(i):
    print title[i]
    print u[i]
    print sl[i]
    print link[i]

def fetchUploader():
    uploader=[]
    productDivs = soup.findAll('font', attrs={'class' : 'detDesc'})
    for div in productDivs:
        uploader.append(div.text)
        #print(div.text)
    print "done"
    return uploader

def fetchSeeders():
    seederNleecher=[]
    productDivs = soup.findAll('tr')
    for div in productDivs:
        tmp = str(div.findAll('td',attrs={'align' : 'right'}))
        #print tmp
        f=[int(x) for x in re.findall("\d+",tmp)]
        seederNleecher.append(f)
    del(seederNleecher[0])
    #print seederNleecher
    print "done"
    return seederNleecher

def fetchMagnet(url):
    magn=[]
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req).read()
    soup = BeautifulSoup(con, 'html.parser')
    productDivs = soup.findAll('div', attrs={'class' : 'download'})

    for div in productDivs:
        tmp=div.find('a')['href']
        print(tmp)


if __name__ == "__main__":
    get_mirrors()
    print url
    title,link=fetchLinkAndTitle()
    u=fetchUploader()
    sl=fetchSeeders()

    mydict=make_dict_list(title,sl,u,link)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(mydict)
    
    fetchMagnet(link[0])#0 is the title index which movie we want to download
    

