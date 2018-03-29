from ctypes import *

from nltk.corpus import wordnet as wn
from utils import *


class Predicate():
    def __init__(self, pred):
        self.raw = pred
        self.raw_expanded = [pred]
        self.candidates = []
    
    def expand(self):

        tmp = wn.synsets(self.raw)
        if tmp:
            if tmp[0].lemma_names()[0] not in self.raw_expanded:
                self.raw_expanded.append(tmp[0].lemma_names()[0])
        print("[INFO] predicates after expanding are: ", self.raw_expanded)
        return

    def map(self):

        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p]
        sim.find.restype = POINTER(c_char_p)

        for p in self.raw_expanded:
            res = sim.find(p.encode(), b"/home/litian/dbpedia/predicate.text")
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
        
        return self.candidates