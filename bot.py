import time
import pprint
import telepot
import requests
from bs4 import BeautifulSoup
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from dbManager import dbManager

def generate_string(word):
	return '+'.join(word.lower().split(' '))

def mark_it_down(text):
	text = text.replace("<br>", "")
	text = text.replace("</br>", "")
	text = text.replace("<i>", "_")
	text = text.replace("</i>", "_")
	return text	

def get_data(req):
	URL = 'http://search.azlyrics.com/search.php?q=' + req
	resp = requests.get(URL)
	bs4 = BeautifulSoup(resp.content, 'html.parser')

	table = bs4.find_all('table')

	if len(table) == 0:
		return [], [], [], [], [], False

	table = table[len(table) - 1]

	song_names = []
	meta_infos = []
	artist_names = []
	song_links = []
	keyboard = []

	counter = 1

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
		keyboard.append([str(counter) + ". - " + a.string + '|' +td.contents[3].string])
		db.new_lyriqs(a.string, td.contents[3].string, a['href'])
		counter = counter + 1
		# text = a.string + td.contents[2] + ' ' + td.contents[3].string
		# href = 'href://' + a['href']
		# keyboard.append([InlineKeyboardButton(text=text, callback_data='alert')])

	return song_names, meta_infos, artist_names, song_links, keyboard, True

def show_lyriqs(msg, chat_id):
	msg = msg.split('|')
	song_name = msg[0]
	artist_name = msg[1]

	link = db.get_lyriqs_link(song_name, artist_name)

	print("Getting - " + link)
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	resp = requests.get(link, headers=headers)
	bs4 = BeautifulSoup(resp.content, 'html.parser')

	divs = bs4.find_all('div')

	text = divs[22].contents[2] + str(divs[22].contents[3])

	hide_keyboard = {'hide_keyboard': True}
	print("Sending message")
	bot.sendMessage(chat_id, mark_it_down(text), reply_markup=hide_keyboard, parse_mode="markdown")



def handle(msg):
	pprint.pprint(msg)
	pprint.pprint('\n')
	chat_id = msg['chat']['id']
	if 'entities' in msg:
		# Bot Command
		print('Bot comand')
		return
	message = msg['text']
	if '/start' in message:
		hide_keyboard = {'hide_keyboard' : True}
                text = 'Hi, :raised_hand::smiley:. I\'m Libretto. Just type the *name* or *artist name* to find the lyrics you want'
                bot.sendMessage(chat_id, text, reply_markup=hide_keyboard, parse_mode="markdown")
		return

	if '. - ' in message:
		show_lyriqs(message[5:], chat_id)
		return
	req = generate_string(message)
	song_names, meta_infos, artist_names, song_links, keyboard, found = get_data(req)

	if not found:
		hide_keyboard = {'hide_keyboard' : True}
		text = 'Unfortunately, your search returned *no result*.\n Try to _check spelling_ or _compose less restrictive search query_'
		bot.sendMessage(chat_id, text, reply_markup=hide_keyboard, parse_mode="markdown")
		return
		

	show_keyboard = {'keyboard' : keyboard}
	bot.sendMessage(chat_id, 'Choose the lyriqs you need, from below',reply_markup=show_keyboard)

ACCESS_TOKEN = '226162312:AAFCLYFSBaMwaHsV5LWsmkNIDDNKKlP4yeM'

bot = telepot.Bot(ACCESS_TOKEN)
bot.message_loop(handle)
print ('Listening ...')

connection = sqlite3.connect('lyriqs.db', check_same_thread=False)
db = dbManager(connection)


while 1:
	time.sleep(10)
