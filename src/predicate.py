from ctypes import *

from utils.thesaurus import Word
from math import sqrt


class Predicate():
    def __init__(self, pred, confidence=1.0, top_k=2):
        self.raw = pred
        self.confidence = confidence
        self.top_k = top_k
        self.raw_expanded = [(pred, confidence)]
        self.candidates = []

    def expand(self):

        raw_word = Word(self.raw)

        for relevance in range(1, 4):
            synsets = raw_word.synonyms('all', relevance=relevance, form='common')
            for synset in synsets:
                for word in synset:
                    self.raw_expanded.append((word, self.confidence * (1.0 - sqrt((4.0 - relevance) * 1600 / 3) / 100)));

        for i in range(len(self.raw_expanded)):
            for j in range(len(self.raw_expanded[i][0])):
                if (self.raw_expanded[i][0][j] == ' ') and ('a' <= self.raw_expanded[i][0][j + 1] <= 'z'):
                    self.raw_expanded[i][0][j + 1] = self.raw_expanded[i][0][j + 1] - 'a' + 'A'

                self.raw_expanded[i][0].replace(" ", "")


        print("[INFO] predicates after expanding are: ", self.raw_expanded)


    def map(self):

        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p]
        sim.find.restype = POINTER(c_char_p)

        for p in self.raw_expanded:
            print("[INFO] start to map ", p[0])
            res = sim.find(p[0].encode(), b"/home/litian/dbpedia/predicate.txt", self.top_k)
            print(res[0].decode())
            self.candidates.append(res[0].decode())
            self.candidates.append(res[1].decode())

        '''
        fin = open("../dbpedia/predicate.txt", 'r')
        preds = [line.strip()[line.rfind('/'): -1].replace('_', ' ') for line in fin]

        for p in self.raw_mapped:
            first_max = second_max = 0
            for idx, item in enumerate(preds):
                tmp = sim_predicates_large(p, item)
                if tmp > first_max:
                    second_max = first_max
                    first_max = idx
                elif tmp > second_max:
                    second_max = idx
                else:
                    pass

            self.candidates.append(preds[first_max])
            self.candidates.append(preds[second_max])

        print("predicate after mapping is: ", self.candidates)
        '''



