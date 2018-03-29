from ctypes import *

from nltk.corpus import wordnet as wn
from utils import *

class Subject():
    def __init__(self, sub):
        self.raw = sub
        self.raw_mapped = sub
        self.candidates = []
       
    def expand(self):

        tmp = wn.synsets(self.raw)
        if tmp:
            self.raw_mapped.append(tmp[0].lemma_names()[0])
        print("subject after expanding is: ", self.raw_mapped)
        return

    def map(self):
        
        '''
        the sub and pred in the external file is with urls
        '''

        fin = open("../dbpedia/subject.txt", 'r')
        subs = [line.strip()[line.rfind('/') : -1].replace('_', ' ') for line in fin]  # with urls
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
        sim = cdll.LoadLibrary("c_lib/libsim.so")
        sim.find.argtypes = [c_char_p, c_char_p]
        sim.find.restypes = c_char_p

        res = sim.find(b"1134 Kepler", b"/home/litian/dbpedia/subject.text")
        print(res.decode("utf-8"))
        print("subject after mapping is: ", self.candidates)

        return self.candidates

