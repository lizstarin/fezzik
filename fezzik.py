from twitter import *
import os, tweet_parser

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
twitter_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

iterator = twitter_stream.statuses.sample()

potential_matches = []

def find_rhyme(tweet):
	t = tweet_parser.build_tweet_info(tweet)

	for pm in potential_matches:
		if t['last_syllable'] == pm['last_syllable'] and len(t['meter']) == len(pm['meter']) and t['last_word'] != pm['last_word']:
			create_rhyme(t, pm)
			return

	potential_matches.append(t)

def create_rhyme(t, m):
	potential_matches.remove(m)

	print t['text']
	print m['text']
	print '\n'

	twitter.statuses.retweet(_id=t['_id'])
	twitter.statuses.retweet(_id=m['_id'])

for tweet in iterator:
	try:
		if tweet['lang'] == 'en':
			find_rhyme(tweet)
	except:
		pass
