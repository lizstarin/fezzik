import parser, poetry_data_handler, random, itertools

def find_rhyme(line):
	parsed_original_line = parser.build_line_info(line)

	potential_rhymes = poetry_data_handler.get_lines_by_meter(parsed_original_line['meter'])

	try:
		for pr in potential_rhymes:
			parsed_line = parser.build_line_info(pr)

			if parsed_original_line['last_syllable'] == parsed_line['last_syllable'] and parsed_original_line['last_word'] != parsed_line['last_word']:
				return (parsed_original_line['text'], parsed_line['text'])
	except: 
		return (parsed_original_line['text'], parsed_original_line['text'])

def build_sonnet():
	potential_lines = poetry_data_handler.get_lines_by_meter('0101010101')
	sonnet = []

	for _ in itertools.repeat(None, 3):
		rhyme_1 = find_rhyme(random.choice(potential_lines))
		rhyme_2 = find_rhyme(random.choice(potential_lines))

		sonnet.append(rhyme_1[0])
		sonnet.append(rhyme_2[0])
		sonnet.append(rhyme_1[1])
		sonnet.append(rhyme_2[1])

	rhyme = find_rhyme(random.choice(potential_lines))
	
	sonnet.append(rhyme[0])
	sonnet.append(rhyme[1])

	print '\n'.join(sonnet)

build_sonnet()

