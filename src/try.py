# This file is used to try different usage of NLP libraries

import nltk


sentence = 'Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1,601 days). Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic.'

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

namedEnt = nltk.ne_chunk(tagged)

ne_in_sent = []



for item in namedEnt.subtrees():
	if (item.label() == 'ORGANIZATION'):
		print(item.label())

	print()
	print()
	#if subtree == 'Tree': 
	#	ne_label = subtree.label()
	#	ne_string = " ".join([token for token, pos in subtree.leaves()])
	#	ne_in_sent.append((ne_string, ne_label))


