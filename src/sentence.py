# -*- coding: utf-8 -*-
import nltk
import spacy

from neuralcoref import Coref

from utils import *
from subject import Subject

#from predicate import Predicate
#from text import Text

class Sentence():
    def __init__(self, content, pos_tag, pos_in_text, number):
        self.content = content
        self.pos_tag = pos_tag
        self.pos_in_text = pos_in_text
        self.number = number
        self.context = []
        self.content_resolved = None
        self.subject = None  # the raw subject in the sentence
        self.predicate = None # the raw predicate verb/phrase in the sentence

    def get_context(self, clean_text_content):

        '''
        for now, the context is just all sentences appearing beforehead
        '''

        all_sent = nltk.sent_tokenize(clean_text_content)
        self.context = ''.join(all_sent[:self.pos_in_text])


        # print("[INFO]context for sentence " + self.content + " is: \n" + self.context)


    def coreference_resolution(self):

        '''
        output: a string: the resolved content of this sentence
        '''

        coref = Coref()
        # clusters = coref.one_shot_coref(utterances = unicode(self.content, "utf-8"), context = unicode(self.context, "utf-8"))
        clusters = coref.one_shot_coref(utterances = self.content, context = self.context)

        '''
        @ problem here: the resolution result is not accurate enough, especially when the sentences are complicated!
        '''
        resolved_utterance_text = coref.get_resolved_utterances()

        self.content_resolved = str(resolved_utterance_text)

        print("[INFO] the concise sentence we want to query is : " + self.content_resolved)

    def extract_subject(self, title, alpha=0.65):

        '''
        nltk pos_tag list:
            https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
        extract all Ns
        if (title in Ns -> sim > 0.8)
            s = title
        else
            s = npacy 'nsubj'
        '''

        nlp = spacy.load('en')

        # here, we re-do the tagging using the *resolved* content, just ignore the previous pos_tag
        tokens = nltk.word_tokenize(self.content_resolved)
        tagged = nltk.pos_tag(tokens)

        for (key, value) in tagged:
            if value[0][0] == 'N' and sim_entity(title, key) > alpha: # if it's a N
                self.subject = title
                return Subject(self.subject)

        doc = nlp(self.content_resolved)

        self.subject = str([tok for tok in doc if (tok.dep_ == "nsubj")][0])
        return Subject(self.subject)

    def extract_predicate():
        pass


if __name__ == "__main__":

    '''
    example paragraph:

    Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1,601 days).
    Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic.
    The body's observation arc begins at Heidelberg, the night after its official discovery observation.

    '''

    s = 'Kepler orbits the Sun once every 4 years and 5 months (1,601 days). Its orbit has an eccentricity of 0.47 and an inclination of 15° with respect to the ecliptic. The body\'s observation arc begins at Heidelberg, the night after its official discovery observation.'
    text = Text(s, '1134 Kepler')

    sentences = text.sentence_extractor()

    for sentence in sentences:
        sentence.get_context()
