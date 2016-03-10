from twitter import *
import threading
import os, parser, utilities, tmbg_data_handler, poetry_data_handler

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
twitter_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

potential_matches = []
matches = []
tmbg_matches = []

def find_rhyming_tweet(tweet):
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

def find_rhyming_line(tweet):
	t = parser.build_tweet_info(tweet)
	potential_rhymes = poetry_data_handler.get_lines_by_meter_length(len(t['meter']))

	for pr in potential_rhymes:
		parsed_line = parser.build_line_info(pr)

		if t['last_syllable'] == parsed_line['last_syllable'] and t['last_word'] != parsed_line['last_word']:
			print 'match found: \n'
			print t['text']
			print parsed_line['text']
			return

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

def tweet_tmbg_rhymes():
	threading.Timer(10, tweet_rhymes).start()
  	if len(tmbg_matches) > 0:
  		tweet_rhyme(tmbg_matches[0])
  		tmbg_matches.remove(tmbg_matches[0])
  	else:
  		print 'nothing to tweet'

def iterate(iterator, rhyme_finder_function):
	for tweet in iterator:
		if 'hangup' in tweet:
			print 'hanging up and calling again \n'
			iterate(twitter_stream.statuses.sample())
		else:
			try:
				if tweet['lang'] == 'en' and '@' not in tweet['text'] and '#' not in tweet['text']:
					rhyme_finder_function(tweet)
			except:
				pass

iterate(twitter_stream.statuses.sample(), find_rhyming_line)
