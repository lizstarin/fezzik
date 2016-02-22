import sqlite3
from flask import Flask

DATABASE = '/tmp/words.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def query_db(lst):
	capital_lst = [str(el.upper()) for el in lst]
	db = connect_db()
	req_string = 'select word, pronunciation from words where word in (' + str(capital_lst).strip("[]") + ')' 
	dictionary_cursor = db.execute(req_string)
	return dict(dictionary_cursor.fetchall())

def build_db():
	db = connect_db()
	db.execute('delete from words')
	raw_data = open('static/cmudict.txt').readlines()
	for el in raw_data:
		line = el.split('  ')
		db.execute('insert into words (word, pronunciation) values (?, ?)', [line[0], line[1]])
		db.commit()
		print 'building'
	print 'done'

