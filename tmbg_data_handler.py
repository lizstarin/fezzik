import sqlite3
import ast
import pronunciation_data_handler, parser, tmbg_scraper
from flask import Flask

DATABASE = '/tmp/tmbg.db'

app = Flask(__name__)
app.config.from_object(__name__)

def get_songs_from_file():
	return [ast.literal_eval(song) for song in open('static/tmbg_song_lines.txt').readlines()]

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
		try:
			meter = parser.get_meter(lyne)
			db.execute('insert into tmbg (lyne, song_title, meter) values (?, ?, ?)', [lyne, song_title, meter])
			db.commit()
		except:
			pass
	print 'building'

def build_db(datafile_exists):
	clear_db()

	if datafile_exists:
		songs = get_songs_from_file()
	else:
		songs = tmbg_scraper.get_songs()

	db = connect_db()
	for song in songs:
		make_db_entry(song, db)
	print 'done'

def query_db():
	db = connect_db()
	req_string = 'select * from tmbg where song_title = "Anaheim"'
	cursor = db.execute(req_string)
	print cursor.fetchall()
	# line = cursor.fetchall()[0][0]
	# print pronunciation_data_handler.query_db(line.split(' '))



