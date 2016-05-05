import time
import pprint
import telepot
import requests
from bs4 import BeautifulSoup

def generate_string(word):
	return '+'.join(word.lower().split(' '))

def get_data(req):
	URL = 'http://search.azlyrics.com/search.php?q=' + req
	resp = requests.get(URL)
	bs4 = BeautifulSoup(resp.content, 'html.parser')

	table = bs4.find('table')

	song_names = []
	meta_infos = []
	artist_names = []
	song_links = []
	keyboard = []

	for tr in table.find_all('tr'):
        	td = tr.find('td')
	        if len(td.contents) < 2:
        	        continue
	        a = td.find('a')
	        song_links.append(a['href'])
	        b = td.find('b')
	        song_names.append(a.string)
	        meta_infos.append(td.contents[2])
	        artist_names.append(td.contents[3].string)
		keyboard.append([a.string + td.contents[2] + ' ' + td.contents[3].string])

	return song_names, meta_infos, artist_names, song_links, keyboard

def handle(msg):
	pprint.pprint(msg)
	pprint.pprint('\n')
	chat_id = msg['chat']['id']
	message = msg['text']
	req = generate_string(message)
	song_names, meta_infos, artist_names, song_links, keyboard = get_data(req)
	
	show_keyboard = {'keyboard' : keyboard}
	bot.sendMessage(chat_id, 'Choose the song you want',reply_markup=show_keyboard)
	
	

ACCESS_TOKEN = '226162312:AAFCLYFSBaMwaHsV5LWsmkNIDDNKKlP4yeM'

bot = telepot.Bot(ACCESS_TOKEN)
bot.message_loop(handle)
print ('Listening ...')

while 1:
	time.sleep(10)

