# -*- coding: utf-8 -*-

import os, sys

from text import Text
from utils.utils import SPARQL_construction, SPARQL_request


def main():
    if len(sys.argv) <= 2:
        print("Usage: python main.py [title] [content]")
        return

    text = Text(sys.argv[1], sys.argv[2])
    text.preprocessing()
    sentences = text.sentence_extractor()

    for sentence in sentences:

        sentence.get_context(text.clean_content)
        sentence.coreference_resolution()

        sentence.extract_subject(text.title)
        print("[INFO] the subject of the sentence %s is: \n" % sentence.content_resolved, sentence.subject)
        print("[INFO] candidate subjects are: ", sentence.subject)

        sentence.extract_predicate()
        print("[INFO] candidate predicates are: ", sentence.predicate)


        sparqls = SPARQL_construction(sentence.subject, sentence.predicate)
        for sparql in sparqls:
            print(" [INFO] the sparql is: ", sparql)
            #print(" [INFO] the results of above sparql are: ", SPARQL_request(sparql))
            print()


if __name__ == "__main__":
    main()

# first, get one example to run smooothly
    '''
    example paragraph:

    Kepler orbits the Sun once every 4 years and 5 months (1,601 days).
    Its orbit has an eccentricity of 0.47 with respect to the ecliptic.
    The body's observation arc begins at Heidelberg, the night after its official discovery observation.

    '''

    #s = 'Peking University (abbreviated PKU or Beida) is a major Chinese research university located in Beijing and a member of the C9 League. Founded as the Imperial University of Peking in 1898 as a replacement of the ancient Guozijian (Imperial College), it is the first modern institution established for higher education in China.'







