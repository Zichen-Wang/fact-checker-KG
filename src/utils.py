import requests
from difflib import SequenceMatcher

import nltk
import spacy

def SPARQL_request(sparql):

    keep = {'http://www.w3.org/2001/XMLSchema#integer',
            'http://www.w3.org/2001/XMLSchema#double',
            'http://dbpedia.org/datatype/inch',
            'http://dbpedia.org/datatype/perCent',
            'http://dbpedia.org/datatype/usDollar',
            'http://www.w3.org/2001/XMLSchema#positiveInteger',
            'http://www.w3.org/2001/XMLSchema#float'
            }

    url = 'http://dbpedia.org/sparql/'
    payload = {'default-graph-uri': 'http://dbpedia.org',
               'query': sparql,
               'format': 'application/sparql-results+json'
               }

    try:
        r = requests.get(url, params=payload)
        result_dict = r.json()

    except:
        print('SPARQL_requests_error')
        return False

    #print(r.url)
    variable_name = result_dict['head']['vars'][0]
    results = result_dict['results']['bindings']

    ans = []

    for res in results:
        if res[variable_name]['datatype'] in keep:
            ans.append(res[variable_name]['value'])

    return ans


# WARNING: The character of a newline is '\r\n' not '\n'
def SPARQL_construction(subjects, predicates):
    '''
    assume that the numbers appear in the object part

    input (with urls):
    [s1,s1,...]
    [p1,p2,...]

    output:
    [SPARQL1, SPARQL2, SPARQL3,...]

    '''
    num_sub = len(subjects)
    num_pred = len(predicates)
    SPARQLs = []
 
    for s in subjects:
        for p in predicates:
            sparql = "select ?x where {\r\n" # WARNING '\n' -> '\r\n'
            sparql = sparql + s.replace(' ' ,'_') + " " + p.replace(' ','_') + " ?x .\r\n}\r\n"  # attention!  ' ' -> '_'
            print(sparql)
            SPARQLs.append(sparql)

    return SPARQLs


def contain_number(sentence):

    '''
    input: any arbitratry sentence
    output: the pos_tag along with the number if the sentence contains one number that we want, else false
    entity types, see: https://stackoverflow.com/questions/40480839/nltk-relation-extraction-returns-nothing
    '''

    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    namedEnt = nltk.ne_chunk(tagged)

    for item in namedEnt.subtrees():
        if item.label() == 'DURATION' or item.label() == 'DATE' or item.label() == 'MONEY':
            return [], False

    for (key, value) in tagged:
        if value == "CD":
            tags = [tag[1] for tag in tagged]
            return tags, key

    return [], False


def sim_entity(en1, en2, alpha=0.2):

    '''
    the similarity measure can be further improved using the context information
    '''

    nlp = spacy.load('en')
    semantic_sim = nlp(en1).similarity(nlp(en2))
    string_sim = SequenceMatcher(None, en1, en2).ratio()

    return alpha * semantic_sim + (1 - alpha) * string_sim

def sim_predicate(pred1, pred2, beta=0.8):

    '''
    the similarity measure can be further improved using the context information
    '''
    
    nlp = spacy.load('en')
    semantic_sim = nlp(pred1).similarity(nlp(pred2))
    string_sim = SequenceMatcher(None, pred1, pred2).ratio()

    return beta * semantic_sim + (1 - beta) * string_sim


'''
the two following similarity measurements are used for the mapping process in Subject and Predicate

def sim_entities_large(en1, en2):
    string_sim = SequenceMatcher(None, en1, en2).ratio()
    return string_sim

def sim_predicates_large(pred1, pred2):
    string_sim = SequenceMatcher(None, pred1, pred2).ratio()
    return string_sim
'''

if __name__ == '__main__':

    # sentence = 'Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1601 days).'
    # sentence = 'Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic. '
    # sentence = 'Its right bridge consists of piers, with the maximum span of 160 metres (525 ft)'
    # print(contain_number(sentence))
    # s = ['Peking_University']
    # p = ['established']
    # SPARQL_construction(s, p)
    
    print(sim_entity("1134 Kepler", "Kepler"))
    print(sim_predicate("establised", "found"))
    #pass



