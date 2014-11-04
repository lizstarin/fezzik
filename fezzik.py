from twitter import *
from wordnik import *
import random, threading, re, os, sys

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

twitter_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
iterator = twitter_stream.statuses.sample()

WORDNIK_API_URL = 'http://api.wordnik.com/v4'
WORDNIK_API_KEY = os.environ.get('WORDNIK_API_KEY')

client = swagger.ApiClient(WORDNIK_API_KEY, WORDNIK_API_URL)
wordnik = WordApi.WordApi(client)

def strip_tweet(tweet):
	return [word for word in tweet.split() if word[0] != '#' and word[0] != '@' and not re.match('http:\/\/*', word) and not re.match('^RT$', word)]

def get_pronunciation(phrase):
	# return ' '.join([wordnik.getTextPronunciations(word)[1].raw for word in phrase])
	for word in phrase:
		textPron = wordnik.getTextPronunciations(word.strip(',.-;"!'))
		try:
			print textPron[1].raw
		except:
			print "none"

def get_meter(phrase):
	pronunciation = get_pronunciation(phrase)
	return ''.join(re.findall('\d+', pronunciation))

def get_last_syllable(phrase):
	pronunciations = get_pronunciation(phrase).split()
	result = ''

	while re.findall('\d+', result) == []:
		result = pronunciations.pop() + ' ' + result

	return result

# for tweet in iterator:
# 	print "*****************************************************\n"
# 	try:
# 		if tweet['lang'] == 'en':
# 			print get_pronunciation(strip_tweet(tweet['text']))
# 	except:
# 		print "no text"

get_pronunciation([u'Just', u'because', u'I', u"don't", u'talk', u'to', u'you,', u'or', u'text', u'you', u'first,', u"doesn't", u'mean', u'I', u"don't", u'miss', u'you.', u"I'm", u'just', u'waiting', u'for', u'you', u'to', u'miss', u'me.'])