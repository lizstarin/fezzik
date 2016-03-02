from bs4 import BeautifulSoup
import urllib2

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
		print 'Exception: no lyrics'
		songfile.write('("' + title + '",' + '[])\n')
		return (title, [])