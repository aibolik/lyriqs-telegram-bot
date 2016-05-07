import sqlite3

class dbManager:
	def __init__(self, connection):
		self.connection = connection
		connection.execute('''CREATE TABLE IF NOT EXISTS LYRIQS
       			(ID	INTEGER	PRIMARY	KEY	NOT NULL,
			NAME	TEXT    		NOT NULL,
       			ARTIST	TEXT     		NOT NULL,
       			LINK	TEXT         		NOT NULL,
			UNIQUE (NAME, ARTIST) ON CONFLICT REPLACE);''')
		self.cursor = connection.cursor()

	def new_lyriqs(self, song_name, artist_name, link):
		self.connection.execute("INSERT INTO LYRIQS (NAME, ARTIST, LINK) \
				VALUES ('" + song_name + "', '" + artist_name + "', '" + link + "')")
		self.connection.commit()

	def get_lyriqs_link(self, song_name, artist_name):
		self.cursor.execute("SELECT LINK FROM LYRIQS WHERE NAME = ? AND ARTIST = ?", (song_name, artist_name))
		links = self.cursor.fetchall()
		return links[0][0]
