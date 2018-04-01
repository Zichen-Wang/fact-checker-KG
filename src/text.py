# -*- coding: utf-8 -*-

import re
import string

import nltk

from sentence import Sentence
from utils import contain_number

class Text():

    def __init__(self, title, content):
        self.title = title
        self.raw_content = content
        self.clean_content = None

    def preprocessing(self):

        text = re.sub(r'\([^)]*\)', '', self.raw_content)
        self.clean_content = ''.join(list(filter(lambda x: x in string.printable, text)))
        # print(self.clean_content)

    def sentence_extractor(self):

        sen = []
        sent_text = nltk.sent_tokenize(self.clean_content)
        for idx, sent in enumerate(sent_text):
            pos_tag, number = contain_number(sent)
            if number:
                sen.append(Sentence(sent, pos_tag, idx, number))

        return sen



if __name__ == '__main__':
    content = "Kepler orbits the Sun at a distance of 1.4–3.9 AU once every 4 years and 5 months (1,601 days). Its orbit has an eccentricity of 0.47 and an inclination of 15° with respect to the ecliptic. The body's observation arc begins at Heidelberg, the night after its official discovery observation."
    title='1134 Kepler'
    text = Text(content, title)
    text.preprocessing()
    for i in text.sentence_extractor():
        print(i.content, i.pos_tag, i.pos_in_text, i.number)
        print("\n\n\n")
