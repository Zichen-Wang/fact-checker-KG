# -*- coding: utf-8 -*-

from neuralcoref import Coref
import nltk

from text import Text
#import nltk
#
#
#sentence = 'Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1,601 days). Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic.'
#
#tokens = nltk.word_tokenize(sentence)
#tagged = nltk.pos_tag(tokens)
#
#namedEnt = nltk.ne_chunk(tagged)
#
#ne_in_sent = []
#
#
#
#for item in namedEnt.subtrees():
#	if (item.label() == 'ORGANIZATION'):
#		print(item.label())
#
#	print()
#	print()
#	#if subtree == 'Tree': 
#	#	ne_label = subtree.label()
#	#	ne_string = " ".join([token for token, pos in subtree.leaves()])
#	#	ne_in_sent.append((ne_string, ne_label))


if __name__ == "__main__":
    '''
    example paragraph:

    Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1,601 days). 
    Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic. 
    The body's observation arc begins at Heidelberg, the night after its official discovery observation.

    '''
    s = 'Kepler orbits the Sun once every 4 years and 5 months (1,601 days). Its orbit has an eccentricity of 0.47 and an inclination of 15° with respect to the ecliptic. The body\'s observation arc begins at Heidelberg, the night after its official discovery observation.'
    text = Text(s, '1134 Kepler')

    text.preprocessing()
    sentences = text.sentence_extractor()

    for sentence in sentences:
              
        sentence.get_context(text.clean_content)
        sentence.coreference_resolution()
        sentence.extract_subject(text.title)
        print("[INFO] the subject of sentence " + sentence.content_resolved + " is: \n" + sentence.subject)
        sentence.extract_predicate()