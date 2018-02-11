 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil,plugintools
from resources.modules import client,control,tools,shortlinks
from resources.ivue import ivuesetup
from datetime import date
import xml.etree.ElementTree as ElementTree
import difflib
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.gentv'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))

username     = control.setting('Username')
password     = control.setting('Password')
adultset     = control.setting('Adult.Set')
adultpwset      = control.setting('Adult.PWSet')
adultpw = control.setting('Adult.PW')

host         = 'http://durextv.vodiptv.org'
port         = '83'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(host,port,username,password)
vodfiles     = 'http://files1.vodiptv.org'

#CATEGORIES
All='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
Armenia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3195'%(host,port,username,password)
Kids_Movies_247='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4846'%(host,port,username,password)
Kids_Tv_Shows_247='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4847'%(host,port,username,password)
Movies_247='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4843'%(host,port,username,password)
TV_247='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4244'%(host,port,username,password)
MUSIC_CHOICE='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4844'%(host,port,username,password)
AUSTRALIA_NZ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4245'%(host,port,username,password)
NCAAB_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4246'%(host,port,username,password)
SD_UK_All='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4247'%(host,port,username,password)
Test='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4248'%(host,port,username,password)
Philippines='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4249'%(host,port,username,password)
International_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3231'%(host,port,username,password)
Work_in_Progress='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3224'%(host,port,username,password)
MLS_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3227'%(host,port,username,password)
NCAAF_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3228'%(host,port,username,password)
Polish='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3222'%(host,port,username,password)
IRISH='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3213'%(host,port,username,password)
ADULTS2='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3217'%(host,port,username,password)
Latin='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3219'%(host,port,username,password)
China='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3197'%(host,port,username,password)
Czech_Republic='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3198'%(host,port,username,password)
Belgium='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3196'%(host,port,username,password)
EX_YU='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3199'%(host,port,username,password)
Greek='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3200'%(host,port,username,password)
Indonesia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3201'%(host,port,username,password)
Iran='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3202'%(host,port,username,password)
Israel='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3203'%(host,port,username,password)
Italy='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3204'%(host,port,username,password)
Japan='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3205'%(host,port,username,password)
Korea='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3206'%(host,port,username,password)
Netherlands='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3207'%(host,port,username,password)
Spain='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3208'%(host,port,username,password)
Sweden_Denmark='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3209'%(host,port,username,password)
Switzerland='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3210'%(host,port,username,password)
UK_Entertainment='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=47'%(host,port,username,password)
UK_Documentaries='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=52'%(host,port,username,password)
UK_Music='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=50'%(host,port,username,password)
UK_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=45'%(host,port,username,password)
UK_Movies='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=49'%(host,port,username,password)
UK_Kids='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=48'%(host,port,username,password)
UK_News='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=51'%(host,port,username,password)
US_Entertainment='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=63'%(host,port,username,password)
US___CA_SPORTS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2813'%(host,port,username,password)
USA_Local_News='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3194'%(host,port,username,password)
LIVE_Football_LIVE='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2497'%(host,port,username,password)
Turkish='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3212'%(host,port,username,password)
Extra_3PM_Links='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=57'%(host,port,username,password)
PPV___LIVE_EVENTS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=38'%(host,port,username,password)
Thailand='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=3211'%(host,port,username,password)
Adults_Only='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2843'%(host,port,username,password)
NHL_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2825'%(host,port,username,password)
NFL_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=409'%(host,port,username,password)
MLB_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=58'%(host,port,username,password)
NBA_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=59'%(host,port,username,password)
AFRICA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2830'%(host,port,username,password)
ALBANIA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2831'%(host,port,username,password)
BRAZIL='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2832'%(host,port,username,password)
CANADA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2833'%(host,port,username,password)
HUNGARY='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2836'%(host,port,username,password)
FRANCE='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2834'%(host,port,username,password)
INDIA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2838'%(host,port,username,password)
RUSSIA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2842'%(host,port,username,password)
ROMANIA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2841'%(host,port,username,password)
Macedonia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2845'%(host,port,username,password)
German='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2846'%(host,port,username,password)
Bulgaria='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2847'%(host,port,username,password)
Pakistan='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2848'%(host,port,username,password)
Portugal='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2849'%(host,port,username,password)
ARAB='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=2850'%(host,port,username,password)
NBC_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=4845'%(host,port,username,password)
Bahamas='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=5485'%(host,port,username,password)

Guide = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gentv/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gentv/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

USER_DATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USER_DATA,'addon_data'))
durextvfol = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.gentv'))
durextvset = xbmc.translatePath(os.path.join(ADDON_DATA,'settings.xml'))
ini          =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gentv/resources/ivue','addons_index.ini'))
inizip       = 	xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gentv/resources/ivue','addons_index.zip'))
tmpini       =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ivuetarget   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/'))
ivueaddons2ini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/addons2.ini'))
ivuecreate   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/'))
ivuecreateini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/addons_index.ini'))
PVRSimple   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))
databasePath = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
subPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/ini')
pyPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/subs')
setupPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups')
drxaddons2ini = xbmc.translatePath('special://profile/addon_data/script.ivueguide/addons2.ini')
dialog = xbmcgui.Dialog()
#########################################
def start():
	if username=="":
		user = userpopup()
		passw= passpopup()
		control.setSetting('Username',user)
		control.setSetting('Password',passw)
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		if auth == "":
			line1 = "[COLOR red]Incorrect Login Details![/COLOR]"
			line2 = "Please Re-enter" 
			line3 = "To purchase account email:[COLOR red] genuineiptv@gmail.com[/COLOR]" 
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', line1, line2, line3)
			start()
		else:
			line1 = "[COLOR lime]Login Successfull![/COLOR]"
			line2 = "Welcome to [COLOR red]Genuine [COLOR white]IPTV[/COLOR]" 
			line3 = ('[COLOR blue]%s[/COLOR]'%user)
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', line1, line2, line3)
			addonsettings('ADS2','')
			adult_settings()
			SIMPLEtvguidesetup()
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		if not auth =="":
			tools.addDir('[COLOR red]--------[B][/COLOR][COLOR red]Genuine[/COLOR] [COLOR white]IPTV[/COLOR][COLOR red][/B]--------[/COLOR]','','',icon,fanart,'')
			tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,icon,fanart,'')
			tools.addDir('[COLOR red]Live TV[/COLOR]','live',21,icon,fanart,'')
			if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				tools.addDir('[COLOR blue]TV Guide[/COLOR] [COLOR gray](Simple PVR Client)[/COLOR]','pvr',7,icon,fanart,'')
			if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				tools.addDir('[COLOR violet]Channels Guide[/COLOR] [COLOR gray](Simple PVR Client)[/COLOR]','pvr',45,icon,fanart,'')
			tools.addDir('[COLOR limegreen]Video on Demand[/COLOR]','url',41,icon,fanart,'')
			tools.addDir('[COLOR orange]24/7[/COLOR]','url',46,icon,fanart,'')
			tools.addDir('[COLOR skyblue]Music[/COLOR]',MUSIC_CHOICE,25,icon,fanart,'')
			if adultset == "false":
				tools.addDir('[COLOR pink]Adult (18+)[/COLOR]','url',48,icon,fanart,'')
			tools.addDir('[COLOR red]----------[B][COLOR white]TOOLS[/COLOR][/B]----------[/COLOR]','','',icon,fanart,'')
			tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
			tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
			#tools.addDir('[COLOR white]Search VOD[/COLOR]','url',43,icon,fanart,'')
			tools.addDir('[COLOR white]Setup Simple PVR[/COLOR]','tv',11,icon,fanart,'')
			tools.addDir('[COLOR white]Extras[/COLOR]','url',16,icon,fanart,'')
			tools.addDir('[COLOR white]Settings[/COLOR]','url',8,icon,fanart,'')
			#tools.addDir('[COLOR gray]Test Area[/COLOR]','url',37,icon,fanart,'')
			plugintools.set_view( plugintools.LIST )
def home():
	tools.addDir('[COLOR red]--------[B][/COLOR][COLOR red]Genuine[/COLOR] [COLOR white]IPTV[/COLOR][COLOR red][/B]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,icon,fanart,'')
	tools.addDir('[COLOR red]Live TV[/COLOR]','live',21,icon,fanart,'')
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		tools.addDir('[COLOR blue]TV Guide[/COLOR] [COLOR gray](Simple PVR Client)[/COLOR]','pvr',7,icon,fanart,'')
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		tools.addDir('[COLOR violet]Channels Guide[/COLOR] [COLOR gray](Simple PVR Client)[/COLOR]','pvr',45,icon,fanart,'')
	tools.addDir('[COLOR limegreen]Video on Demand[/COLOR]','url',41,icon,fanart,'')
	tools.addDir('[COLOR red]24/7[/COLOR]','url',46,icon,fanart,'')
	tools.addDir('[COLOR skyblue]Music[/COLOR]',MUSIC_CHOICE,25,icon,fanart,'')
	if adultset == "false":
		tools.addDir('[COLOR pink]Adult (18+)[/COLOR]','url',48,icon,fanart,'')
	tools.addDir('[COLOR red]----------[B][COLOR white]TOOLS[/COLOR][/B]----------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	#tools.addDir('[COLOR white]Search VOD[/COLOR]','url',43,icon,fanart,'')
	tools.addDir('[COLOR white]Setup Simple PVR[/COLOR]','tv',11,icon,fanart,'')
	tools.addDir('[COLOR white]Extras[/COLOR]','url',16,icon,fanart,'')
	tools.addDir('[COLOR white]Settings[/COLOR]','url',8,icon,fanart,'')
	#tools.addDir('[COLOR gray]Test Area[/COLOR]','url',37,icon,fanart,'')
	plugintools.set_view( plugintools.LIST )
	setView()
	
def NEW_MENU():
	tools.addDir('[COLOR red]------------------------[B][COLOR white]LIVE TV[/COLOR][/B]------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]All Channels[/COLOR]',All,2,icon,fanart,'')
	tools.addDir('[COLOR skyblue]PPV/Live Events[/COLOR]',PPV___LIVE_EVENTS,25,icon,fanart,'')
	tools.addDir('[COLOR red]US[/COLOR]',url,22,icon,fanart,'')
	tools.addDir('[COLOR blue]UK[/COLOR]',url,23,icon,fanart,'')
	tools.addDir('[COLOR limegreen]International[/COLOR]',url,24,icon,fanart,'')
	tools.addDir('[COLOR gray]Original Playlist[/COLOR]','live',1,icon,fanart,'')
	tools.addDir('[COLOR red]---------------------------------------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()

	
def US():
	tools.addDir('[COLOR red]-----------[/COLOR][COLOR red][B]US LIVE[/B][/COLOR][COLOR red]-----------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]US Entertainment[/COLOR]',US_Entertainment,25,icon,fanart,'')
	tools.addDir('[COLOR white]US Local News[/COLOR]',USA_Local_News,25,icon,fanart,'')
	tools.addDir('[COLOR red]--------[/COLOR][COLOR red][B]US SPORTS[/B][/COLOR][COLOR red]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]US Sports[/COLOR]',US___CA_SPORTS,25,icon,fanart,'')
	tools.addDir('[COLOR white]NFL[/COLOR]',NFL_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]NBA[/COLOR]',NBA_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]NHL[/COLOR]',NHL_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]MLB[/COLOR]',MLB_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]MLS[/COLOR]',MLS_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]NCAAF[/COLOR]',NCAAF_Package,25,icon,fanart,'')
	tools.addDir('[COLOR white]NCAAB[/COLOR]',NCAAB_Package,25,icon,fanart,'')
	tools.addDir('[COLOR red]-------------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()
	
def UK():
	tools.addDir('[COLOR red]----------[/COLOR][COLOR blue][B]UK LIVE[/B][/COLOR][COLOR red]----------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]UK Entertainment[/COLOR]',UK_Entertainment,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK (SD) Standard Definition[/COLOR]',SD_UK_All,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Movies[/COLOR]',UK_Movies,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Documentaries[/COLOR]',UK_Documentaries,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK News[/COLOR]',All,34,icon,fanart,'')
	tools.addDir('[COLOR white]UK Kids[/COLOR]',UK_Kids,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Music[/COLOR]',UK_Music,25,icon,fanart,'')
	tools.addDir('[COLOR red]--------[/COLOR][COLOR blue][B]UK SPORTS[/B][/COLOR][COLOR red]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]UK Sports[/COLOR]',UK_Sports,25,icon,fanart,'')
	tools.addDir('[COLOR white]Football[/COLOR]',LIVE_Football_LIVE,25,icon,fanart,'')
	tools.addDir('[COLOR white]NBC Premiere League[/COLOR]',NBC_Package,25,FOOTBALLimg,fanart,'')
	tools.addDir('[COLOR white]Extra 3pm Links[/COLOR]',Extra_3PM_Links,25,icon,fanart,'')
	tools.addDir('[COLOR red]-------------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()
	
def INT():
	tools.addDir('[COLOR red]--------[/COLOR][B][COLOR limegreen][B]INTERNATIONAL[/B][/COLOR][COLOR red]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]International Sports[/COLOR]',International_Sports,25,icon,fanart,'')
	tools.addDir('[COLOR white]Latin[/COLOR]',Latin,25,icon,fanart,'')
	tools.addDir('[COLOR white]Canada[/COLOR]',CANADA,25,icon,fanart,'')
	tools.addDir('[COLOR white]France[/COLOR]',FRANCE,25,icon,fanart,'')
	tools.addDir('[COLOR white]Africa[/COLOR]',AFRICA,25,icon,fanart,'')
	tools.addDir('[COLOR white]Albania[/COLOR]',ALBANIA,25,icon,fanart,'')
	tools.addDir('[COLOR white]Arab[/COLOR]',ARAB,25,icon,fanart,'')
	tools.addDir('[COLOR white]Armenia[/COLOR]',Armenia,25,icon,fanart,'')
	tools.addDir('[COLOR white]Australia-New Zealand[/COLOR]',AUSTRALIA_NZ,25,icon,fanart,'')
	tools.addDir('[COLOR white]Bahamas[/COLOR]',Bahamas,25,icon,fanart,'')
	tools.addDir('[COLOR white]Belgium[/COLOR]',Belgium,25,icon,fanart,'')
	tools.addDir('[COLOR white]Brazil[/COLOR]',BRAZIL,25,icon,fanart,'')
	tools.addDir('[COLOR white]Bulgaria[/COLOR]',Bulgaria,25,icon,fanart,'')
	tools.addDir('[COLOR white]China[/COLOR]',China,25,icon,fanart,'')
	tools.addDir('[COLOR white]Czech Republic[/COLOR]',Czech_Republic,25,icon,fanart,'')
	tools.addDir('[COLOR white]EX YU[/COLOR]',EX_YU,25,icon,fanart,'')
	tools.addDir('[COLOR white]Germany[/COLOR]',German,25,icon,fanart,'')
	tools.addDir('[COLOR white]Greek[/COLOR]',Greek,25,icon,fanart,'')
	tools.addDir('[COLOR white]Hungary[/COLOR]',HUNGARY,25,icon,fanart,'')
	tools.addDir('[COLOR white]India[/COLOR]',INDIA,25,icon,fanart,'')
	tools.addDir('[COLOR white]Indonesia[/COLOR]',Indonesia,25,icon,fanart,'')
	tools.addDir('[COLOR white]Iran[/COLOR]',Iran,25,icon,fanart,'')
	tools.addDir('[COLOR white]Ireland[/COLOR]',IRISH,25,icon,fanart,'')
	tools.addDir('[COLOR white]Israel[/COLOR]',Israel,25,icon,fanart,'')
	tools.addDir('[COLOR white]Italy[/COLOR]',Italy,25,icon,fanart,'')
	tools.addDir('[COLOR white]Japan[/COLOR]',Japan,25,icon,fanart,'')
	tools.addDir('[COLOR white]Korea[/COLOR]',Korea,25,icon,fanart,'')
	tools.addDir('[COLOR white]Macedonia[/COLOR]',Macedonia,25,icon,fanart,'')
	tools.addDir('[COLOR white]Netherlands[/COLOR]',Netherlands,25,icon,fanart,'')
	tools.addDir('[COLOR white]Pakistan[/COLOR]',Pakistan,25,icon,fanart,'')
	tools.addDir('[COLOR white]Philippines[/COLOR]',Philippines,25,icon,fanart,'')
	tools.addDir('[COLOR white]Polish[/COLOR]',Polish,25,icon,fanart,'')
	tools.addDir('[COLOR white]Portugal[/COLOR]',Portugal,25,icon,fanart,'')
	tools.addDir('[COLOR white]Romania[/COLOR]',ROMANIA,25,icon,fanart,'')
	tools.addDir('[COLOR white]Russia[/COLOR]',RUSSIA,25,icon,fanart,'')
	tools.addDir('[COLOR white]Spain[/COLOR]',Spain,25,icon,fanart,'')
	tools.addDir('[COLOR white]Sweden-Denmark[/COLOR]',Sweden_Denmark,25,icon,fanart,'')
	tools.addDir('[COLOR white]Switzerland[/COLOR]',Switzerland,25,icon,fanart,'')
	tools.addDir('[COLOR white]Thailand[/COLOR]',Thailand,25,icon,fanart,'')
	tools.addDir('[COLOR red]-------------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()
	
def ALL_247():
	tools.addDir('[COLOR red]----------[/COLOR][COLOR red][B]24/7[/B][/COLOR][COLOR red]----------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Movies[/COLOR]',Movies_247,47,icon,fanart,'')
	tools.addDir('[COLOR white]TV Shows[/COLOR]',TV_247,47,icon,fanart,'')
	tools.addDir('[COLOR white]Kids Movies[/COLOR]',Kids_Movies_247,47,icon,fanart,'')
	tools.addDir('[COLOR white]Kids TV Shows[/COLOR]',Kids_Tv_Shows_247,47,icon,fanart,'')
	tools.addDir('[COLOR red]-------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()
	
def ALL_ADULT():
	tools.addDir('[COLOR red]----------[/COLOR][COLOR pink][B]ADULT[/B][/COLOR][COLOR red]----------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Adult (18+) #1[/COLOR]',ADULTS2,25,icon,fanart,'')
	tools.addDir('[COLOR white]Adult (18+) #2[/COLOR]',Adults_Only,25,icon,fanart,'')
	tools.addDir('[COLOR red]-------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,icon,fanart,'')
	setView()
	
def extras():
	tools.addDir('[COLOR white]Create a Short M3U & EPG URL[/COLOR]','url',17,icon,fanart,'')
	tools.addDir('[COLOR white]Run a Speed Test[/COLOR]','ST',10,icon,fanart,'')
	tools.addDir('[COLOR blue]iVue TV Guide[/COLOR]','pvr',44,icon,fanart,'')
	tools.addDir('[COLOR white]Setup iVue TV Guide -Old-[/COLOR]','tv',15,icon,fanart,'')
	#tools.addDir('[COLOR white]Setup iVue TV Guide -New-[/COLOR]','tv',36,icon,fanart,'')
	tools.addDir('[COLOR white]iVue TV Guide Settings[/COLOR]','tv',38,icon,fanart,'')
	tools.addDir('[COLOR white]Reboot iVue TV Guide[/COLOR]','url',20,icon,fanart,'')
	setView()
		
def settingsmenu():
	tools.addDir('Settings','tv',39,icon,fanart,'')
	tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
	tools.addDir('Log Out','LO',10,icon,fanart,'')
	setView()	

	

	
def US_ALL():
	US = [" US ", " us "]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in US:
			if item in name:
				if " IN " in name:
					pass
				else:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
	
def US_NEWS():
	US_NEWS = ["News", "NEWS", "FOX 25", "CNN", "Bloomberg", "CNBC", "MSN", "MSNBC"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in US_NEWS:
			if item in name:
				if " US " in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
				else:
					pass
	plugintools.set_view( plugintools.EPISODES )
	
def UK_NEWS():
	UK_NEWS = ["News", "NEWS", "ITV UK"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in UK_NEWS:
			if item in name:
				if " UK " in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
				else:
					pass
	plugintools.set_view( plugintools.EPISODES )
					
def MUSIC_ALL():
	MUSIC = ["MUSIC", "music", "Music", "MTV", "VH1"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in MUSIC:
			if item in name:
				tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.LIST )		
def SPORTS_ALL():
	SPORTS =["Sport", "SPORT", "Sports", "SPORTS", "NHL", "MLB", "NBA", "NFL", "PAC", "TSN", "ESPN", "Fox", "Golf", "Tennis", "Football", "UFC", "moto", "celtic tv", "rangers tv", "LFC TV", "boxnation", "NCAA", "MLS"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in SPORTS:
			if item in name:
				tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )				

				
	
	
def UK_ALL():
	UK = [" UK ", " uk "]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in UK:
			if item in name:
				if " IN " in name:
					pass
				else:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
					
					
def SoftReset():
	clearFiles = ["guides.ini", "addons.ini", "guide.xml", "amylist.xml", "teamexpat.xml", "otttv.xml", "guide2.xml", "uk3.xml", "guide3.xmltv", "master.xml"]
	for root, dirs, files in os.walk(databasePath,topdown=True):
		dirs[:] = [d for d in dirs]
		for name in files:
			if name in clearFiles:
				try:
					os.remove(os.path.join(root,name))
				except:
					dialog.ok('Soft Reset', 'Error Removing ' + str(name),'')
					pass
			else:
				continue
	dialog.ok('Ivue guide Soft reset', 'Please restart iVue TV Guide ','for changes to take effect.')
	home()

def DESTROY_PATH(path):
    shutil.rmtree(path, ignore_errors=True)

def exit():
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    if os.path.exists(durextvfol):   
        DESTROY_PATH(durextvfol)

		
def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		tools.addDir(name,url1,2,icon,fanart,'')
		plugintools.set_view( plugintools.LIST )
		
def Livelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.LIST )
	
def LiveInfolist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
	
def LiveTitlelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name.title(),url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
		
	
def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fanart,'')
			plugintools.set_view( plugintools.LIST )
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
		
		
##########################################



def ivuetvguide():
	if xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		if not os.path.exists(drxaddons2ini):
			IVUEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('RunAddon(script.ivueguide)')
		
def simpletvguide():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		if not os.path.exists(PVRSimple):
			SIMPLEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('ActivateWindow(TVGuide)')
			
def simplechannels():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		if not os.path.exists(PVRSimple):
			SIMPLEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('ActivateWindow(TVChannels)')
			
def EXIT():
	xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	
				
def stream_video(url):
	if adultpwset == "true":
		a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx'
		if any(s in name for s in a):
			text = control.inputDialog(heading='Enter Adult Password:')
			if text ==control.setting('Adult.PW'):
				url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
				liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
				liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
				liz.setProperty('IsPlayable','true')
				liz.setPath(str(url))
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			else:
				xbmc.executebuiltin((u'XBMC.Notification("Parental Lock", "Incorrect Password!", 2000)'))
				return
		else:
			url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
			liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(url))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		
	else:
		url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
		liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
		liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
		liz.setProperty('IsPlayable','true')
		liz.setPath(str(url))
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def searchdialog():
	search = control.inputDialog(heading='Search [COLOR red]Genuine [COLOR white]IPTV[/COLOR]:')
	if search=="":
		return
	else:
		return search
	
def search():
	if mode==3:
		return False
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
		return
	xbmc.log(str(text))
	open = tools.OPEN_URL(panel_api)
	all_chans = tools.regex_get_all(open,'{"num":','epg')
	for a in all_chans:
		name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
		url  = tools.regex_from_to(a,'"stream_id":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if text in name.lower():
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')
		elif text not in name.lower() and text in name:
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')

	

def addonsettings(url,description):
	if   url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','3GB Ram or Higher (Nvidia Shield) AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','3GB Ram or Higher (Nvidia Shield)'])
		if dialog==0:
			advancedsettings('stick')
			
		elif dialog==1:
			advancedsettings('firetv')
			
		elif dialog==2:
			advancedsettings('lessthan')
			
		elif dialog==3:
			advancedsettings('morethan')
			
		elif dialog==4:
			advancedsettings('shield')
			
	elif url =="tv":
		ivueint()

	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.gentv/resources/modules/speedtest.py")')
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	
		
def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
def pvrsetup():
	correctPVR()
	killxbmc()
	return
		
		
def asettings():
	choice = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

def adultpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Adult Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	data = json.load(urllib2.urlopen(panel_api))
	null = ["0", " " , "null"]
	today = datetime.date.today()
	x=data['user_info']
	Username = x['username']
	Status = x['status']
	Creation = x['created_at']
	Created = datetime.datetime.fromtimestamp(int(Creation)).strftime('%H:%M %m/%d/%Y')
	Current = x['active_cons']
	Max = x['max_connections']
	Expiry = x['exp_date']
	if Expiry == None:
		Expired = 'Never'
	else:
		Expired = datetime.datetime.fromtimestamp(int(Expiry)).strftime('%H:%M %m/%d/%Y')
	tools.addDir('[COLOR red]--------[COLOR red]Genuine[/COLOR] [COLOR white]IPTV[/COLOR] [COLOR white]ACCOUNT INFO[/COLOR][COLOR red]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Username :[/COLOR] '+Username,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Expire Date:[/COLOR] '+Expired,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Account Status :[/COLOR] '+Status,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Current Connections:[/COLOR] '+Current,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Allowed Connections:[/COLOR] '+Max,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Created:[/COLOR] '+Created,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Please e-mail [COLOR red]genuineiptv@gmail.com[/COLOR] to renew account.[/COLOR]',All,2,icon,fanart,'')
	plugintools.set_view( plugintools.LIST )

	
def correctPVR():

	addon = xbmcaddon.Addon('plugin.video.gentv')
	username_text = addon.getSetting(id='Username')
	password_text = addon.getSetting(id='Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = "http://durextv.vodiptv.org:83/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"
	EPGurl     = "http://durextv.vodiptv.org:83/xmltv.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	
def ivueint():
	ivuesetup.iVueInt()
	xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'iVue Integration Complete')
	xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.IVUEcreator/update_addon/plugin.video.gentv",return)')
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	
def ivueint2():
	ivuesetup.iVueInt2()
	xbmcgui.Dialog().ok('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]', 'iVue Integration Complete')
	home()
	
	
def SIMPLEtvguidesetup():
	dialog = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]','Would you like to setup Simple PVR Client TV Guide?')
	if dialog:
		pvrsetup()
	else:
		home()
		
def IVUEtvguidesetup():
	dialog = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]','Would you like to setup iVue TV Guide?')
	if dialog:
		ivueint()
	else:
		home()
		
def adult_settings():
	dialog = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]','Would you like to setup iVue TV Guide?')
	if dialog:
		ivueint()
	else:
		home()
		
adultset     = control.setting('Adult.Set')
adultpwset      = control.setting('Adult.PWSet')
adultpw = control.setting('Adult.PW')


def adult_settings():
	dialog = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]','Would you like to HIDE [COLOR pink]Adult Menu[/COLOR]?', 'You can always change this in settings later on.')
	if dialog:
		control.setSetting('Adult.Set','true')
		pass
	else:
		control.setSetting('Adult.Set','false')
		pass
	dialog = xbmcgui.Dialog().yesno('[COLOR red]Genuine [COLOR white]IPTV[/COLOR]','Would you like to PASSWORD PROTECT [COLOR pink]Adult Channels[/COLOR]?', 'You can always change this in settings later on.')
	if dialog:
		control.setSetting('Adult.PWSet','true')
		adulter = adultpopup()
		control.setSetting('Adult.PW',adulter)
	else:
		control.setSetting('Adult.PWSet','false')
		pass
		
def ivue_settings():
	xbmc.executebuiltin("Addon.OpenSettings(script.ivueguide)")

def drx_settings():
	xbmc.executebuiltin("Addon.OpenSettings(plugin.video.gentv)")

	
def setView():
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
def killxbmc(over=None):
	killdialog = xbmcgui.Dialog().yesno('Force Close Kodi', '[COLOR white]You are about to close Kodi', 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Force Close Kodi[/COLOR][/B]')
	if killdialog:
		os._exit(1)
	else:
		home()
		

def testarea():
	durextvcat   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.gentv/categories.db'))
	channels = []
	
	if os.path.isfile(durextvcat):
		os.remove(durextvcat)

	
	list_a = tools.OPEN_URL(live_url)
	all_chan = tools.regex_get_all(list_a,'<channel>','</channel>')
	for a in all_chan:
			name = tools.regex_from_to(a,'<title>','</title>')
			name = base64.b64decode(name)
			name = re.sub(' ','_',name)
			name = re.sub('&','_',name)
			name = re.sub('\/','_',name)
			name = re.sub('\+','_',name)
			xbmc.log(str(name))
			try:
				name = re.sub('\[.*?min ','-',name)
			except:
				pass
			catnum  = tools.regex_from_to(a,'<category_id>','</category_id>')
			line = "%s = %s\n"%(name, catnum)
			channels.append(line)
					
	for item3 in channels:
		f = open(durextvcat, mode='a')
		f.write(item3)
		f.close()
		
def vod_open(url):
	list_a = tools.OPEN_URL(vodfiles)
	all_files = tools.regex_get_all(list_a,'<A HREF','<br>')
	for a in all_files:
		name = tools.regex_from_to(a,'">','</A>')
		url1 = tools.regex_from_to(a,'<A HREF="','">')
		url2 = 'http://files1.vodiptv.org' + url1
		tools.addDir(name,url2,42,icon,fanart,'')
		
def vod_open2(url):
	play = ['.mp4', '.mkv', '.avi', '.ts', '.flv', '.vob', '.wmv', '.m4v', '.m4p', '.mpg', '.mpeg', '.m2v', '.3gp', '.3g2', '.flv','.f4v', '.f4p', '.f4a', '.f4b']
	dontplay = ['.jpg', '.nfo', '.srt', 'web.config', '.png', '.gif']
	list_a = tools.OPEN_URL(url)
	all_files = tools.regex_get_all(list_a,'<A HREF','<br>')
	for a in all_files:
		name = tools.regex_from_to(a,'">','</A>')
		url1 = tools.regex_from_to(a,'<A HREF="','">')
		url2 = 'http://files1.vodiptv.org' + url1
		
		if any(x in url1 for x in play):
			tools.addDir(name.replace('.',' '),url2,4,icon,fanart,'')
		else:
			if any(d in url2 for d in dontplay):
				pass
			else:
				tools.addDir(name,url2,42,icon,fanart,'')
		
def searchvod():
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
		return
	xbmc.log(str(text))
	foundname = []
	foundurl = []
	list_a = tools.OPEN_URL(vodfiles)
	all_files = tools.regex_get_all(list_a,'<A HREF','<br>')
	for a in all_files:
		catname = tools.regex_from_to(a,'">','</A>')
		url1 = tools.regex_from_to(a,'<A HREF="','">')
		url2 = 'http://files1.vodiptv.org' + url1
		list_b = tools.OPEN_URL(url2)
		all_filesb = tools.regex_get_all(list_b,'<A HREF','<br>')
		for b in all_filesb:
			name = tools.regex_from_to(a,'">','</A>')
			urla = tools.regex_from_to(a,'<A HREF="','">')
			urlb = 'http://files1.vodiptv.org' + urla
			if text in name.lower():
				foundname.append(name)
				foundurl.append(urlb)
			elif text not in name.lower() and text in name:
				foundname.append(name)
				foundurl.append(urlb)
	for x in foundname and y in foundurl:
		tools.addDir(x,y,4,icon,fanart,'')
		

		
		
def changenumbers(s):

    numbers = {'1' : 'one' ,'2' : 'two', '3' : 'three', '4':'four', '5' : 'five' ,'6' : 'six' ,
               '7' : 'seven', '8' : 'eight', '9':'nine', '10' : 'ten', '11':'eleven', '12' : 'twelve',}

    for src, target in numbers.iteritems():
        if src in s:
            s = s.replace(src, target)

    return s

def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
setView()
params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
	vod(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	simpletvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	
elif mode==10:
	addonsettings(url,description)
	
elif mode==11:
	SIMPLEtvguidesetup()
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	listcatchup2()
	
elif mode==15:
	ivueint()
	
elif mode==16:
	extras()
	
elif mode==17:
	shortlinks.Get()

elif mode==18:
	footballguidesearch(description)
	
elif mode==19:
	get()
	
elif mode==20:
	SoftReset()
	
elif mode==21:
	NEW_MENU()
	
elif mode==22:
	US()
	
elif mode==23:
	UK()
	
elif mode==24:
	INT()
	
elif mode==25:
	LiveInfolist(url)

elif mode==26:
	NFL()
	
elif mode==27:
	NHL()
	
elif mode==28:
	LIVE_FOOTBALL()	
	
elif mode==29:
	US_ALL()
	
elif mode==30:
	UK_ALL()
	
elif mode==31:
	MUSIC_ALL()
	
elif mode==32:
	SPORTS_ALL()
	
elif mode==33:
	US_NEWS()
	
elif mode==34:
	UK_NEWS()
	
elif mode==35:
	NEWS_ALL()
	
elif mode==36:
	ivueint2()
	
elif mode==37:
	testarea()

elif mode==38:
	ivue_settings()

	
elif mode==39:
	drx_settings()
	
elif mode==40:
	simpletvguide()
	
elif mode==41:
	vod_open(url)
	
elif mode==42:
	vod_open2(url)
	
elif mode==43:
	searchvod()
	
elif mode==44:
	ivuetvguide()
	
elif mode==45:	
	simplechannels()
	
elif mode==46:		
	ALL_247()

elif mode==47:		
	LiveTitlelist(url)
	
elif mode==48:		
	ALL_ADULT()
	
	





xbmcplugin.endOfDirectory(int(sys.argv[1]))