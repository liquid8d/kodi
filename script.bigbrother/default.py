import xbmc, xbmcgui, xbmcaddon
import urllib, urllib2, cookielib, json
import datetime, calendar, time

# Script constants
__scriptname__ = "Big Brother"
__author__     = "liquid8d"
__url__        = "http://github.com/liquid8d/BigBrother"
__addon__   = xbmcaddon.Addon(id='script.bigbrother')
__cwd__        = __addon__.getAddonInfo('path')
__icon__        = __addon__.getAddonInfo('icon')

#xbmc.executebuiltin('RunScript("' + __cwd__ + '/window.py' + '")')

ACTION_PARENT_DIR = 9
ACTION_STOP = 13
ACTION_PREVIOUS_MENU = 10
ACTION_NUMBER_1 = 59
ACTION_NUMBER_2 = 60
ACTION_NUMBER_3 = 61
ACTION_NUMBER_4 = 62
ACTION_NUMBER_5 = 63
ACTION_BACKSPACE = 110

#the player we will use
class MyPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self, xbmc.PLAYER_CORE_AUTO)

class BigBrother(xbmcgui.WindowXMLDialog):
    #setup urllib2 with cookies
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    #init player
    Player = MyPlayer()

    #init class
    def __init__(self, *args, **kwargs):
        
        #setup variables
        self.isLoggedIn = False
        self.season = 15
        self.fbMonth = 6
        self.fbDay = 26
        self.fbHour = 9
        self.fbMin = 0
        
        #get default camera
        defCam = __addon__.getSetting('defaultcam')
        if defCam=='Cam 1':
            self.camera = 1
        elif defCam=='Cam 2':
            self.camera = 2
        elif defCam=='Cam 3':
            self.camera = 3
        elif defCam=='Cam 4':
            self.camera = 4
        else:
            self.camera = 5
        
        #get default quality
        defCam = __addon__.getSetting('quality')
        if defCam=='Low':
            self.quality = 300
        elif defCam=='Medium':
            self.quality = 500
        elif defCam=='High':
            self.quality = 800
        else:
            #highest
            self.quality = 1200

        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
        self.doModal()
        
    def onInit(self):
        #gui startup stuff
        self.login()
        
    def onAction(self, action):
        if action == ACTION_NUMBER_1:
            self.switchCamera(1)
        if action == ACTION_NUMBER_2:
            self.switchCamera(2)
        if action == ACTION_NUMBER_3:
            self.switchCamera(3)
        if action == ACTION_NUMBER_4:
            self.switchCamera(4)
        if action == ACTION_NUMBER_5:
            self.switchCamera(5)
        if action == ACTION_PREVIOUS_MENU:
            self.Player.stop()
            self.end()
        if action == ACTION_PARENT_DIR:
            self.Player.stop()
            self.end()
        if action == ACTION_BACKSPACE:
            self.Player.stop()
            self.end()

    def onClick(self, controlID):
        #self.notify('button', 'You clicked button ' + str(controlID), 3)
        if controlID==151:
            self.switchCamera(1)
        elif controlID==152:
            self.switchCamera(2)
        elif controlID==153:
            self.switchCamera(3)
        elif controlID==154:
            self.switchCamera(4)
        elif controlID==155:
            self.switchCamera(5)
        elif controlID==156:
            self.Player.stop()
            self.end()
        
    def onFocus(self, controlID):
        pass

    def showFlashback(self):
        self.getControl(210).setVisible(true)

    #switch cams
    def switchCamera(self, cam):
        if not self.isLoggedIn:
            self.loginError()
        self.camera = cam
        if cam==1:
            self.getControl(111).setLabel('Cam 1')
        elif cam==2:
            self.getControl(111).setLabel('Cam 2')
        elif cam==2:
            self.getControl(111).setLabel('Cam 3')
        elif cam==2:
            self.getControl(111).setLabel('Cam 4')
        else:
            self.getControl(111).setLabel('Quad Cam')

        self.Player.play(self.getStream())

    #login to CBS to verify permission to access
    def login(self):
        #this is the text shown from the signin page if you are not logged in
        loginText = '"success":true'
        #this is the login url
        url = 'https://cbs.com/account/login/'
        #this is the post data that is sent
        data = urllib.urlencode({'j_username': __addon__.getSetting('cbs_username'), 'j_password': __addon__.getSetting('cbs_password')})
        #print('Logging in at: ' + url)
        try:
            response = urllib2.urlopen(url, data)
            html = response.read()
            response.close()
            #print('Response: ' + html)
            if not loginText in html:
                self.isLoggedIn = False
                self.loginError()
            else:
                #print('Logged into CBS')
                self.isLoggedIn = True
                #print('Downloading codes')
                self.downloadCodes()
                self.switchCamera(self.camera)
        except Exception as e:
            print('Error: ' + str(e))
            self.isLoggedIn = False

    #display error when login is not correct
    def loginError(self):
        self.message('Login Error', 'Check your CBS username and password in addon settings')

    #urls for the feeds change each day, we need some codes to get the correct day url
    def downloadCodes(self):
        #this is the stream codes url
        url = 'https://www.dropbox.com/s/ez6fbfmvztt932p/code.txt?dl=1'
        #print('Getting stream codes at: ' + url)
        try:
            progress = xbmcgui.DialogProgress()
            progress.create('One sec...', 'Downloading required files')
            response = urllib2.urlopen(url)
            html = response.read()
            response.close()
            #print('Got codes: ' + html)
            self.streamcodes = json.loads(html)
            progress.close()
        except Exception as e:
            print('Error getting codes: ' + str(e))

    #set requested season
    def setSeason(self, season):
        self.season = season

    #set requested camera
    def setCamera(self, camera):
        self.camera = camera

    #get the actual url to the stream
    def getStream(self):
        #we need the current date timestamp, but convert to PST first
        curdate = datetime.datetime.utcnow()
        bbtdate = curdate - datetime.timedelta(hours=7)
        bbtday = bbtdate.strftime('%m%d%y')
        #print 'now: %s' % (curdate)
        #print 'bbt: %s' % (bbtdate)
        #print 'bbtday: %s' % (bbtday)
        for x in range(0, len(self.streamcodes)):
            print 'Checking %s: %s' % (x, self.streamcodes[x]['date'])
            if bbtday in self.streamcodes[x]['date']:
                url = 'http://cbsbigbrother-lh.akamaihd.net/i/BBLIVE%s%s_%s@%s/index_%d_av-p.m3u8?sd=15&rebase=on' % (bbtday, self.streamcodes[x]['code'], self.camera, self.streamcodes[x]['id'], self.quality)
                print('url: ' + url)
                return url
    #notification to user
    def notify(self, title, message, sec):
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title,message, sec * 1000, __icon__))

    #message to user
    def message(self, title, msg):
        dialog = xbmcgui.Dialog()
        dialog.ok(title, msg)

    #wrap up
    def end(self):
        self.close()

# -- STARTUP PROCESS HERE --
MyWindow = BigBrother("script.bigbrother.Main.xml", __cwd__, "default")
del MyWindow