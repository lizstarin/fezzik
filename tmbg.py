from bs4 import BeautifulSoup
import urllib2
import sqlite3
import ast
from flask import Flask

DATABASE = '/tmp/tmbg.db'

app = Flask(__name__)
app.config.from_object(__name__)

def clean_data():
	data = open('static/tmbg_songs.txt').readlines()
	f = open('static/tmbg_songs_cleaned.txt', 'w')

	cleaned = [d.strip() for d in data if not d[-2] == ')']
	for line in cleaned:
		f.write(line + '\n')

def build_slugs():
	data = open('static/tmbg_songs_cleaned.txt').readlines()
	f = open('static/tmbg_slugs.txt', 'w')

	slugs = ['_'.join(d.split()) for d in data]
	for line in slugs:
		f.write(line + '\n')

def get_songs():
	f = open('static/tmbg_song_lines.txt', 'w')

	slugs = open('static/tmbg_slugs.txt').readlines()
	return [get_song(slug, f) for slug in slugs]

def get_song(slug, songfile):
	title = ' '.join(slug.split('_')).strip()
	print title
	url = 'http://tmbw.net/wiki/Lyrics:' + slug

	try: 
		html_page = urllib2.urlopen(url)
		
		soup = BeautifulSoup(html_page, 'lxml')
		for el in ['br', 'b', 'i']:
			for e in soup.find_all(el):
				e.extract()

		song = [line.get_text() for line in soup.find('div', {'class' : 'lyrics-table'}).find_all('p')]
		song = [line.strip() for line in ''.join(song).split('\n') if line != '']

		songfile.write('("' + title + '",' + str(song) + ')\n')
		return (title, song)
	except:
		print 'EXCEPTION'
		songfile.write('("' + title + '",' + '[])\n')
		return (title, [])

def get_songs_from_file():
	return [ast.literal_eval(song) for song in open('static/tmbg_song_lines.txt').readlines()]
	# todo: fix edge cases - chokes on double quotes that contain double quotes

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def clear_db():
	try:
		db.execute('delete from tmbg')
	except:
		pass

def make_db_entry(song, db):
	song_title = unicode(song[0], 'utf-8')
	lines = song[1]
	for lyne in lines:
		db.execute('insert into tmbg (lyne, song_title) values (?, ?)', [lyne, song_title])
		db.commit()
	print 'building'

def query_db():
	db = connect_db()
	req_string = 'select lyne from tmbg where song_title = "Anaheim"'
	cursor = db.execute(req_string)
	print cursor.fetchall()

def run():
	clear_db()
	songs = get_songs()
	# songs = get_songs_from_file()
	db = connect_db()
	for song in songs:
		make_db_entry(song, db)
	print 'done'

query_db()



