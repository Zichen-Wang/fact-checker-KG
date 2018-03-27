from nltk.corpus import wordnet as wn
from utils import *

class Predicate():
    def __init__(self, pred):
        self.raw = pred
        self.raw_mapped = pred
        self.candidates = []
    
    def expand(self):

        tmp = wn.synsets(self.raw)
        if tmp:
            self.raw_mapped.append(tmp[0].lemma_names()[0])
        print("predicate after expaning is: ", self.raw_mapped)
        return

    def map(self):
        
        fin = open("../dbpedia/predicate.txt", 'r')
        preds = [line.strip()[line.rfind('/'): -1].replace('_', ' ') for line in fin]

        for p in self.raw_mapped:
            #p = p[p.rfind('/'), -1].replace('_',' ')
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
        return self.candidates