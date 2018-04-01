# -*- coding: utf-8 -*-
import os
import re
from collections import Counter

import nltk
import spacy

from neuralcoref import Coref

from utils.utils import *
from subject import Subject
from predicate import Predicate
from IE.main import stanford_ie
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

        self.subject = []  # the raw subject in the sentence
        self.predicate = [] # the raw predicate verb/phrase in the sentence

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

        self.content_resolved = str(resolved_utterance_text)[2:-2]

        print("[INFO] the concise sentence we want to query is : " + self.content_resolved)

    def extract_subject(self, title, alpha=0.55):

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
            if value[0] == 'N' and sim_entity(title, key) > alpha: # if it's a N
                self.subject = title
                return Subject(self.subject)

        doc = nlp(self.content_resolved)

        subject = Subject(str([tok for tok in doc if (tok.dep_ == "nsubj")][0]))

        subject.expand()
        subject.map()

        self.subject = subject.candidates

    def extract_predicate(self, max_gram_num=2):

        '''
        stanford Open IE -> [triple1, triple2, ...]
            if (sim(extract出的subject和triple中的subject) > \beta and 该triple中的object带数字)
                p＝triple中的predicate
            else
                - rule 1: (p) of number  (length of 3 meters)
                - rule 2: number + in + N  (3 meters in length)
                - rule 3: number + 单位 + adj (3 meters long)

                extract 3 words with the four rules and then pick up the words which appear more
        '''

        '''
        fout = open(os.path.join(os.path.abspath(os.curdir),"tmp.txt"), "w")
        fout.write(self.content_resolved + "\n")
        #os.system("echo \"" + self.content_resolved + "\" > tmp")
        fout.close()
        #triples = os.popen("python Stanford-OpenIE-Python/main.py -f ../tmp").readlines()[1]
        triples = stanford_ie(os.path.join(os.path.abspath(os.curdir),"tmp.txt"))
        print("[INFO] triples extracted using Stanford Open IE is: ", triples)
        print(type(triples))
        candidate_words=[]
        for triple in triples:
            print(triple)
            print("now cal sim between ", triple[0], self.subject)
            if sim_entity(triple[0], self.subject) > alpha:
                print(triple[1])
                candidate_words.append(triple[1])

                #return Predicate(self.predicate)

        '''

        '''
        pattern1 = "of " + self.number
        pattern2 = self.number + 一个单词 + "in "
        pattern3 = self.number + 一个单词 + adj.
        pattern4 = self.subject 最接近的N
        pattern1 = re.match('(.*) of ' + self.number + '(.*)', self.content_resolved, re.I) # re.I: 忽略大小写
        if pattern1:
            print(pattern1.group(1))
        '''

        '''
        tokens = nltk.word_tokenize(self.content_resolved)
        tagged = nltk.pos_tag(tokens)
        idx_number = [i for i, (key, value) in enumerate(tagged) if value == "CD"][0]

        candidate_words = []
        try:
            candidate_words.append(tokens[tokens.index(self.number)-2])
        except:
            pass

        try:
            candidate_words.append(tokens[tokens.index(self.number)+3])
        except:
            pass

        try:
            if tagged[tokens.index(self.number)+2][1] == "JJ":
                candidate_words.append(tokens[tokens.index(self.number)+2])
        except:
            pass

        candidate_counts = Counter(candidate_words)
        print(candidate_counts.most_common(1)[0])
        self.predicate = candidate_counts.most_common(1)[0][0]
        '''

        predicates = []
        sentence = self.content_resolved
        
        for gram_num in range(max_gram_num):
            ngrams = nltk.ngrams(sentence.split(), gram_num)
            for ngram in ngrams:
                predicates.append(Predicate(pred=' '.join(ngram)))

        all_predicates_candidates = []
        for A_predicate in predicates:
            A_predicate.expand()
            A_predicate.map()
            for c in A_predicate.candidates:
                all_predicates_candidates.append(c)


        return all_predicates_candidates





        #return Predicate(self.predicate)



if __name__ == "__main__":

    '''
    example paragraph:

    Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1,601 days).
    Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic.
    The body's observation arc begins at Heidelberg, the night after its official discovery observation.

    '''

    s = 'Kepler orbits the Sun once every 4 years and 5 months. Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic.'
    text = Text(s, '1134 Kepler')

    sentences = text.sentence_extractor()

    for sentence in sentences:
        sentence.get_context()
        sentence.coreference_resolution()
        sentence.extract_predicate()

