import requests

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

    print(r.url)
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


