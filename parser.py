import re, pronunciation_data_handler

def get_pronunciation(phrase):
	# Takes string, returns string
	lst = [el.strip('.,!-?/":;[]()') for el in re.split(r'[-\s]*', phrase)]
	pronunciation_dict = pronunciation_data_handler.query_db(lst)
	return ' '.join([pronunciation_dict[word.upper()].strip('\n') for word in lst])

def get_meter(phrase):
	#Takes string, returns string
	pronunciation = get_pronunciation(phrase)
	return ''.join(re.findall('\d+', pronunciation))

def get_last_syllable(phrase):
	#Takes string, returns string
	pronunciation = get_pronunciation(phrase).split()
	result = ''

	while re.findall('1', result) == []:
		result = pronunciation.pop() + ' ' + result

	return result

# FOR TWEETS

def strip_tweet(tweet):
	#Takes string, returns string
	return ' '.join([word for word in tweet.split() if word[0] != '#' and word[0] != '@' and not re.match('http:\/\/*', word) and not re.match('^RT$', word)])

def build_tweet_info(tweet):
	_id = tweet['id_str']
	text = strip_tweet(tweet['text'])
	meter = get_meter(text)
	last_syllable = get_last_syllable(text)
	last_word = text.split()[-1].strip('.,!-?/":;[]()').upper()

	return { 
		'_id': _id,
		'text': text,
		'meter' : meter,
		'last_syllable' : last_syllable,
		'last_word' : last_word
	}

# FOR POEM LINES

def build_line_info(line):
	text = line[1]
	last_syllable = get_last_syllable(text)
	last_word = text.split()[-1].strip('.,!-?/":;[]()').upper()

	return { 
		'text': text,
		'meter' : line[4],
		'last_syllable' : last_syllable,
		'last_word' : last_word
	}