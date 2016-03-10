import sqlite3
from flask import Flask
import ast
import pronunciation_data_handler, parser

DATABASE = '/tmp/poems.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def parse_poem(poem):
	chopped = poem.split('|')
	return {
		'author' : chopped[0],
		'title'  : chopped[1],
		'lines'  : chopped[2:]
	}

def build_db():
	db = connect_db()
	try:
		db.execute('delete from poems')
	except:
		pass

	poems = [parse_poem(poem) for poem in open('static/poems.txt').readlines()]
	for poem in poems: 
		make_db_entry(poem, db)

def make_db_entry(poem, db):
	title = poem['title']
	author = poem['author']
	lines = poem['lines']

	print title
	for lyne in lines:
		try: 
			meter = parser.get_meter(unicode(lyne))
		except:
			meter = ''

		try:
			db.execute('insert into poems (lyne, author, title, meter) values (?, ?, ?, ?)', [unicode(lyne), unicode(author), unicode(title), unicode(meter)])
			db.commit()
		except Exception, e:
			pass

def query_db(req_string):
	db = connect_db()
	cursor = db.execute(req_string)
	return cursor.fetchall()

def get_lines_by_meter(meter):
	return query_db('select * from poems where meter = "' + meter + '"')

def get_lines_by_meter_length(num):
	return query_db('select * from poems where length(meter) = ' + str(num))

def get_lines_by_poem(title):
	return query_db('select * from poems where title = "' + title + '"')

def say_hello():
	print 'hello world'





