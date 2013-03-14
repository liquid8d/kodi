import urllib,urllib2,re,xbmcplugin,xbmcgui

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

addLink('420p (640x360 @700k)', 'http://b_kpnx-f.akamaihd.net/KPNX_1_1_700@72415?videoId=1724204566001&lineUpId=&pubId=29901534001&playerId=1659202266001&affiliateId=&accountid=29901534001&v=2.11.3&fp=WIN%2011%2C6%2C602%2C171&r=XXXXX&g=XXXXXXXXXXXX&v=2.11.3&fp=WIN%2011,6,602,171&r=FFVXN&g=DJPKDWELYOYC', 'DefaultVideo.png')
addLink('720p (1280x720 @1500k)', 'http://b_kpnx-f.akamaihd.net/KPNX_1_1_1500@72415?videoId=1724204566001&lineUpId=&pubId=29901534001&playerId=1659202266001&affiliateId=&accountid=29901534001&v=2.11.3&fp=WIN%2011%2C6%2C602%2C180&r=XXXXX&g=XXXXXXXXXXXX&v=2.11.3&fp=WIN%2011,6,602,180&r=KPWQU&g=SHCFVXJLVNSS', 'DefaultVideo.png')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
