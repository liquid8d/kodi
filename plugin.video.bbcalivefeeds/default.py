import urllib,urllib2,re,xbmcplugin,xbmcgui

#http://xbigbrothercanada1x.api.channel.livestream.com/3.0/playlist.m3u8
#http://xbigbrothercanada2x.api.channel.livestream.com/3.0/playlist.m3u8
#http://xbigbrothercanada3x.api.channel.livestream.com/3.0/playlist.m3u8
#http://xbigbrothercanada4x.api.channel.livestream.com/3.0/playlist.m3u8


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

addLink('Camera1', 'http://xbigbrothercanada1x.api.channel.livestream.com/3.0/playlist.m3u8', 'DefaultVideo.png')
addLink('Camera1 ALT', 'rtsp://mobilestr.livestream.com/livestreamiphone/bigbrothercanada1', 'DefaultVideo.png')
addLink('Camera2', 'http://xbigbrothercanada2x.api.channel.livestream.com/3.0/playlist.m3u8', 'DefaultVideo.png')
addLink('Camera2 ALT', 'rtsp://mobilestr.livestream.com/livestreamiphone/bigbrothercanada2', 'DefaultVideo.png')
addLink('Camera3', 'http://xbigbrothercanada3x.api.channel.livestream.com/3.0/playlist.m3u8', 'DefaultVideo.png')
addLink('Camera3 ALT', 'rtsp://mobilestr.livestream.com/livestreamiphone/bigbrothercanada3', 'DefaultVideo.png')
addLink('Camera4', 'http://xbigbrothercanada4x.api.channel.livestream.com/3.0/playlist.m3u8', 'DefaultVideo.png')
addLink('Camera4 ALT', 'rtsp://mobilestr.livestream.com/livestreamiphone/bigbrothercanada4', 'DefaultVideo.png')

xbmcplugin.endOfDirectory(int(sys.argv[1]))
