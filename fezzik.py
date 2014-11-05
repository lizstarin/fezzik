from twitter import *
import os, tweet_parser

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

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

def create_rhyme(t, pm):
	potential_matches.remove(pm)
	print t['text']
	print pm['text']
	

for tweet in iterator:
	try:
		if tweet['lang'] == 'en':
			find_rhyme(tweet)
	except:
		pass
