from bs4 import BeautifulSoup
import urllib2

f = open('static/poems.txt', 'w')

def get_poems():
	slugs = open('static/slugs.txt').readlines()
	return [get_poem(slug) for slug in slugs]

def get_poem(slug):
	print slug
	url = 'http://www.poetryfoundation.org' + slug

	try: 
		html_page = urllib2.urlopen(url)
		
		soup = BeautifulSoup(html_page, 'lxml')
		poem = soup.find('div', {'id' : 'poemwrapper'})
		parse_poem(poem)
	except Exception, e:
		print 'exception'
		print e

def parse_poem(poem):
	poem_author = find_author_name(poem.find('span', {'class' : 'author'}))
	poem_title = ''.join([bit for bit in poem.h1.stripped_strings])
	poem_text = poem.find('div', {'class' : 'poem'})
	poem_lines = [' '.join([bit for bit in text.stripped_strings]) for text in poem_text.find_all('div')]

	write_entry({
		'author': poem_author.encode('utf-8'),
		'title': poem_title.encode('utf-8'),
		'lines': [line.encode('utf-8') for line in poem_lines] 
	})

def find_author_name(div):
	return div.a.string.strip() if div.a else div.string[4:]

def write_entry(poem):
	entry = poem['author'] + '|' + poem['title'] + '|' + '|'.join(poem['lines']) + '\n'
	f.write(entry)

get_poems()


