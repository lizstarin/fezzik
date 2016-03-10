import parser

def find_rhyme(line):
	meter = parser.get_meter(line)
	last_syllable = parser.get_last_syllable(line)

	