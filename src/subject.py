from ctypes import *

from utils.thesaurus import Word
from math import sqrt

class Subject():
    def __init__(self, sub, top_k=2):
        self.raw = sub
        self.top_k = top_k
        self.raw_expanded = [sub]
        self.candidates = []

    def expand(self):

        raw_word = Word(self.raw)

        for relevance in range(1, 4):
            synsets = raw_word.synonyms('all', relevance=relevance, form='common')
            for synset in synsets:
                for word in synset:
                    self.raw_expanded.append((word, (1.0 - sqrt((4.0 - relevance) * 1600) / 3) / 100));

        for i in range(len(self.raw_expanded)):
            self.raw_expanded[i][0].replace(" ", "_")

        print("subjects after expanding are: ", self.raw_expanded)

    def map(self):

        '''
        the sub and pred in the external file is with urls

        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p]
        sim.find.restype = POINTER(c_char_p)

        for p in self.raw_expanded:
            res = sim.find(p.encode(), b"/home/litian/dbpedia/predicate.text")
            self.candidates.append(res[0].decode())
            self.candidates.append(res[1].decode())
        '''

        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p, c_int]
        sim.find.restype = POINTER(c_char_p)

        for s in self.raw_expanded:
            print("[INFO] start to map ", s[0])
            res = sim.find(s[0].encode(), b"/home/litian/dbpedia/subject.txt", self.top_k)
            #res_ = res
            tmp1 = res[0].decode()
            tmp2 = res[1].decode()

            self.candidates.append(tmp1)
            self.candidates.append(tmp2)

        '''
        for s in self.raw_mapped:
            #s = s[s.rfind('/'), -1].replace('_', ' ')
            first_max = second_max = 0
            for idx, item in enumerate(subs):
                tmp = sim_entities_large(s, item)
                if tmp > first_max:
                    second_max = first_max
                    first_max = idx
                elif tmp > second_max:
                    second_max = idx
                else:
                    pass

            self.candidates.append(subs[first_max])
            self.candidates.append(subs[second_max])
        '''

