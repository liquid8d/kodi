import urllib,urllib2,re,xbmcplugin,xbmcgui
import json

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,2,thumbnail)

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for url in match:
                addLink(name,url,'')

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

#addLink('Feeds', 'http://ichunk.livestream.com/212.54/livestreamiphone/bigbrothercanada4-secretlocationdev000020130304-182952-high_1756/playlist.m3u8?wowzasessionid=133706173', 'DefaultVideo.png')

#get info for camera
#http://new.livestream.com/api/accounts/6388794/events/2701984/viewing_info

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def download(url, ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1'):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', ua)
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        return data
    except:
        logger.error('Error downloading: ' + url)
    return None

print('BBCALiveFeeds: Getting camera info')
cam_event_ids = ['2596592', '2701973', '2701980', '2701984', '2712276']
count = 0
for x in cam_event_ids:
    try:
        count += 1
        data = download('http://new.livestream.com/api/accounts/6388794/events/' + x + '/viewing_info')
        stream = str(json.loads(data)['streamInfo']['rtsp_url'])
        #id = find_between(m3u8, '/i/', '_1@')
        #link = 'http://player.livestream-f.akamaihd.net/i/' + id + '_1@156550/master.m3u8'
        #mobile = 'rtsp://212-125.livestream.com:8080/livestreamiphone/' + id + '_1_150@156550'
        addLink('Camera ' + str(count), stream, 'DefaultVideo.png')
        #addLink('Camera ' + str(count) + ' (mobile alt)', mobile, 'DefaultVideo.png')
    except:
        print('error retrieving for camera ' + str(count));

xbmcplugin.endOfDirectory(int(sys.argv[1]))
