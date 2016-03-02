# TWEETS

def destroy_tweets(): 
	tweets = twitter.statuses.user_timeline(screen_name='anybdywannapnut', count=200)
	for t in tweets:
		twitter.statuses.destroy(id=t['id'])

# TMBG

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