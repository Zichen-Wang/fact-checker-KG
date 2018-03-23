import requests

import nltk

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
    pass

def contain_number(sentence):
    '''
    input: any arbitratry sentence
    output: the number if the sentence contains one number that we want, else false
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

if __name__ == '__main__':
    #sentence = 'Kepler orbits the Sun at a distance of 1.4-3.9 AU once every 4 years and 5 months (1601 days).' 
    sentence = 'Its orbit has an eccentricity of 0.47 and an inclination of 15 with respect to the ecliptic. '
    sentence = 'Its right bridge consists of piers, with the maximum span of 160 metres (525 ft)'
    print(contain_number(sentence))




