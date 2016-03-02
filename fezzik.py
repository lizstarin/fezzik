from twitter import *
import threading
import os, parser, utilities

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
twitter_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

potential_matches = []
matches = []

def find_rhyme(tweet):
	t = parser.build_tweet_info(tweet)

	for pm in potential_matches:
		if t['last_syllable'] == pm['last_syllable'] and len(t['meter']) == len(pm['meter']) and t['last_word'] != pm['last_word']:
			potential_matches.remove(pm)
			archive_rhyme(t, pm)
			print 'match found'
			print '# matches:'
			print len(matches)
			return

	potential_matches.append(t)

def archive_rhyme(t, m):
	matches.append([t, m])

def tweet_rhyme(r):
	print r[0]['text']
	print r[1]['text']
	print '\n'

	try:
		twitter.statuses.retweet(_id=r[0]['_id'])
		twitter.statuses.retweet(_id=r[1]['_id'])
	except TwitterHTTPError as e:
		print e

def tweet_rhymes():
	threading.Timer(600, tweet_rhymes).start()
  	if len(matches) > 0:
  		tweet_rhyme(matches[0])
  		matches.remove(matches[0])
  	else:
  		print 'nothing to tweet'

def iterate(iterator):
	tweet_rhymes()

	for tweet in iterator:
		if 'hangup' in tweet:
			print 'hanging up and calling again \n'
			iterate(twitter_stream.statuses.sample())
		else:
			try:
				if tweet['lang'] == 'en' and '@' not in tweet['text'] and '#' not in tweet['text']:
					find_rhyme(tweet)
			except:
				pass

iterate(twitter_stream.statuses.sample())