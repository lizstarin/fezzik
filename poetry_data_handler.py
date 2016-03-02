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
