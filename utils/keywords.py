from paralleldots import set_api_key, get_api_key, keywords
import operator 
import random

api_key = "XfkatyBaYa53U7yAtEWlgpKunGS36pC2fP5QfcP7NOE"
set_api_key(api_key)
def retKeywords(text):
    keyword_dict =  keywords(str(text))['keywords']
    tempDict = {}
    for x in keyword_dict:
        print keyword_dict
        tempDict[x['keyword']] = x['confidence_score']
    selectedWords = dict(sorted(tempDict.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10])
    return random.sample(selectedWords.keys(),5)
