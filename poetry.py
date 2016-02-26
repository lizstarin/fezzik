from bs4 import BeautifulSoup
import urllib2

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

f = open('static/poems.txt', 'w')
toc_base_url = 'http://www.poetryfoundation.org/browse/#page='
slugs = []

def get_poems():
	for s in slugs:
		get_poem(s)
		print 'building'
	print 'done'

def get_poem_slugs():
	for i in range(1,676): # last page is 675, so range ends in 676
		open_page(toc_base_url + str(i))
	write_slugs_to_file()

def open_page(url):
	wd = webdriver.PhantomJS()
	wd.get(url)
	WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'resultcount')))
	html_page = wd.page_source
	print wd.title
	wd.quit()
	parse_page_for_slugs(html_page)

def parse_page_for_slugs(html_page):
	soup = BeautifulSoup(html_page, 'lxml') 
	titles = soup.find_all('a', {'class' : 'title'})
	slugs.extend(map(lambda t: t.get('href'), titles))

def write_slugs_to_file():
	slugfile = open('static/slugs.txt', 'a')
	for s in slugs:
		slugfile.write(s + '\n')

def get_poem(slug):
	url = 'http://www.poetryfoundation.org' + slug
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page, 'lxml')
	poem = soup.find('div', {'id' : 'poemwrapper'})
	parse_poem(poem)

def parse_poem(poem):
	poem_author = find_author_name(poem.find('span', {'class' : 'author'}))
	poem_title = poem.h1.string
	poem_text = poem.find('div', {'class' : 'poem'})
	poem_lines = map(lambda l: unicode(l.string).encode('ascii', 'replace').strip(), poem_text.find_all('div'))
	write_entry({
		'author': str(poem_author),
		'title': str(poem_title),
		'lines': str(poem_lines)
	})

def find_author_name(div):
	return div.a.string.strip() if div.a else div.string[4:]

def write_entry(poem):
	entry = poem['author'] + ', ' + poem['title'] + ', ' + poem['lines'] + '\n'
	f.write(entry)

get_poem_slugs()
# get_poems()

