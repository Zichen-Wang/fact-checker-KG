from ctypes import *

from nltk.corpus import wordnet as wn
from utils import *

class Subject():
    def __init__(self, sub):
        self.raw = sub
        self.raw_expanded = sub
        self.candidates = []
       
    def expand(self):

        tmp = wn.synsets(self.raw)
        if tmp:
            self.raw_expanded.append(tmp[0].lemma_names()[0])
        print("subjects after expanding are: ", self.raw_mapped)
        return

    def map(self):
        
        '''
        the sub and pred in the external file is with urls
        '''

        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p]
        sim.find.restype = POINTER(c_char_p)

        for p in self.raw_expanded:
            res = sim.find(p, b"/home/litian/dbpedia/subject.text")
            print(res[0])
            print(res[1])
            self.candidates.append(res[0])
            self.candidates.append(res[1])


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

        return self.candidates

