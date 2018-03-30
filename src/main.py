# -*- coding: utf-8 -*-

from ctypes import *

from neuralcoref import Coref
import nltk

from text import Text
from utils import *


if __name__ == "__main__":

# first, get one example to run smooothly
    '''
    example paragraph:

    Kepler orbits the Sun once every 4 years and 5 months (1,601 days). 
    Its orbit has an eccentricity of 0.47 with respect to the ecliptic. 
    The body's observation arc begins at Heidelberg, the night after its official discovery observation.

    '''
    s = 'Peking University (abbreviated PKU or Beida) is a major Chinese research university located in Beijing and a member of the C9 League. Founded as the Imperial University of Peking in 1898 as a replacement of the ancient Guozijian (Imperial College), it is the first modern institution established for higher education in China.'
    text = Text(s, 'Peking University')

    text.preprocessing()
    sentences = text.sentence_extractor()

    for sentence in sentences:
              
        sentence.get_context(text.clean_content)
        sentence.coreference_resolution()
        sub = sentence.extract_subject(text.title)
        print("[INFO] the subject of sentence " + sentence.content_resolved + " is: \n" + sentence.subject)
        pred = sentence.extract_predicate()
        
        sub.expand()
        sub_mapped = sub.map()
        print("[INFO] candidate subjects are: ", sub_mapped)


        pred.expand()
        pred_mapped = pred.map()
        print("[INFO] candidate predicates are: ", pred_mapped)
        

        sparqls = SPARQL_construction(sub_mapped, pred_mapped)
        for sparql in sparqls:
            print(" [INFO] the sparql is: ", sparql)
            print(' ')





