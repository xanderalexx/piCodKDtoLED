import time
import requests
import json
import RPi.GPIO as g
g.setmode(g.BCM)

status1 = 2
red1 = 21
red2 = 20
yellow1 = 16
yellow2 = 12
white1 = 11
white2 = 7
blue1 = 8
blue2 = 25
green1 = 24
green2 = 23
time.sleep(1)
g.setup(status1, g.OUT)
g.output(status1, g.LOW)
g.setup(red1, g.OUT)
g.output(red1, g.LOW)
g.setup(red2, g.OUT)
g.output(red2, g.LOW)
g.setup(yellow1, g.OUT)
g.output(yellow1, g.LOW)
g.setup(yellow2, g.OUT)
g.output(yellow2, g.LOW)
g.setup(white1, g.OUT)
g.output(white1, g.LOW)
g.setup(white2, g.OUT)
g.output(white2, g.LOW)
g.setup(blue1, g.OUT)
g.output(blue1, g.LOW)
g.setup(blue2, g.OUT)
g.output(blue2, g.LOW)
g.setup(green1, g.OUT)
g.output(green1, g.LOW)
g.setup(green2, g.OUT)
g.output(green2, g.LOW)
x = 0
while x < 5:
	g.output(status1, g.HIGH)
	g.output(red1, g.HIGH)
        g.output(red2, g.HIGH)
        g.output(yellow1, g.HIGH)
        g.output(yellow2, g.HIGH)
        g.output(white1, g.HIGH)
        g.output(white2, g.HIGH)
        g.output(blue1, g.HIGH)
        g.output(blue2, g.HIGH)
        g.output(green1, g.HIGH)
        g.output(green2, g.HIGH)
	time.sleep(1)
	g.output(status1, g.LOW)
	g.output(red1, g.LOW)
        g.output(red2, g.LOW)
        g.output(yellow1, g.LOW)
        g.output(yellow2, g.LOW)
        g.output(white1, g.LOW)
        g.output(white2, g.LOW)
        g.output(blue1, g.LOW)
        g.output(blue2, g.LOW)
        g.output(green1, g.LOW)
        g.output(green2, g.LOW)
	x = x + 1

def allLEDSoff():
	g.output(red1, g.LOW)
        g.output(red2, g.LOW)
        g.output(yellow1, g.LOW)
        g.output(yellow2, g.LOW)
        g.output(white1, g.LOW)
        g.output(white2, g.LOW)
        g.output(blue1, g.LOW)
        g.output(blue2, g.LOW)
        g.output(green1, g.LOW)
        g.output(green2, g.LOW)

def setLEDS(i):
	allLEDSoff()
	g.output(status1, g.HIGH)
	time.sleep(0.5)
	g.output(status1, g.LOW)
	time.sleep(0.5)
	g.output(status1, g.HIGH)
	time.sleep(0.5)
	g.output(status1, g.LOW)
	time.sleep(1)
	if i >= 0.2:
		g.output(red1, g.HIGH)
	if i >= 0.4:
		g.output(red2, g.HIGH)
	if i >= 0.6:
		g.output(yellow1, g.HIGH)
	if i >= 0.8:
		g.output(yellow2, g.HIGH)
	if i >= 1:
		g.output(white1, g.HIGH)
	if i >= 1.2:
		g.output(white2, g.HIGH)
	if i >= 1.4:
		g.output(blue1, g.HIGH)
	if i >= 1.6:
		g.output(blue2, g.HIGH)
	if i >= 1.8:
		g.output(green1, g.HIGH)
	if i >= 2:
		g.output(green2, g.HIGH)

urlGET = "https://profile.callofduty.com/cod/login"
urlPOST = "https://profile.callofduty.com/do_login?new_SiteId=cod"
urlGETid = "https://www.callofduty.com/api/papi-client/crm/cod/:version/identities"
urlGETfriends = "https://my.callofduty.com/api/papi-client/codfriends/:version/compendium"
urlGETmatches = "https://my.callofduty.com/api/papi-client/crm/cod/:version/title/:game/platform/:platform/gamer/:username/matches/mp/start/:start/end/:end/details"


def Average(lst):
    return sum(lst) / len(lst)

game = 'cw'
platform = 'battle'
#battleusername = 'NAUJS%2311554'
#battleusername = 'YnApollo%231312'
battleusername = 'blazebuddyTV%231323'
#battleusername = 'DimStarWhite%231250'
#battleusername = 'Alex%23118855'
username = 'EMAIL'
password = 'PASSWORD'
#initial get auth
finalaverage = 0
abc=0
times=0
print("battleusername = " + battleusername)
while abc<=10:
	kdarray = []

	client = requests.session()
	client.get(urlGET)
	_csrf = client.cookies['XSRF-TOKEN']
	#initial post auth
	payload = {'username':username, 'password':password, 'remember_me':'true', '_csrf':_csrf}

	client.post(urlPOST, data=payload)
	print('successful login!')
	ACT_SSO_COOKIE = client.cookies['ACT_SSO_COOKIE']
	ACT_SSO_COOKIE_EXPIRY = client.cookies['ACT_SSO_COOKIE_EXPIRY']
	atkn = client.cookies['atkn']
	#get matches
	payload = {'ACT_SSO_COOKIE':ACT_SSO_COOKIE, 'ACT_SSO_COOKIE_EXPIRY':ACT_SSO_COOKIE_EXPIRY, 'atkn':atkn}
	r = client.get('https://my.callofduty.com/api/papi-client/crm/cod/v2/title/cw/platform/battle/gamer/' + battleusername + '/matches/mp/start/0/end/0/details', data=payload)
	print('getting match data...')
	data = json.loads(r.text)
	data_ = data['data']
	match_data = data_['matches']
	compare = finalaverage

	o = 0
	for i in match_data:
		hmmm = i['playerStats']
		kdarray.append(hmmm['kdRatio'])
		o = o + 1
		if o == 3:
			break
	average = Average(kdarray)
	finalaverage = round(average, 2)
	if finalaverage != compare:
		setLEDS(finalaverage)
		print('Change in KD detected!!!, new average KD is ' + str(finalaverage))
		times = 0
	else:
		times = times+1
		print("no change found, " + str(times) + " checks since last change")
		g.output(status1, g.HIGH)
		time.sleep(0.5)
		g.output(status1, g.LOW)
	time.sleep(4.5)
