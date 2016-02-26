import sqlite3
from flask import Flask
import poetry

DATABASE = '/tmp/poems.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def build_db():
	db = connect_db()
	db.execute('delete from poems')
	poetry.get_poems()


	raw_data = open('static/cmudict.txt').readlines()
	for el in raw_data:
		line = el.split('  ')
		db.execute('insert into words (word, pronunciation) values (?, ?)', [line[0], line[1]])
		db.commit()
		print 'building'
	print 'done'

