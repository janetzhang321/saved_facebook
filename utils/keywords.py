from paralleldots import set_api_key, get_api_key, keywords
import operator 
import random


test = [{u'keyword': u'Friends', u'confidence_score': 0.525636}, {u'keyword': u'us tomorrow', u'confidence_score': 0.956888}, {u'keyword': u'great line', u'confidence_score': 0.965009}, {u'keyword': u'SECOND', u'confidence_score': 0.658226}, {u'keyword': u'LAST FRIDAY', u'confidence_score': 0.674397}, {u'keyword': u'CRYPT', u'confidence_score': 0.781744}]

api_key = "XfkatyBaYa53U7yAtEWlgpKunGS36pC2fP5QfcP7NOE"
set_api_key(api_key)

def retKeywords(text):
    keyword_dict =  keywords(str(text))['keywords']
    tempDict = {}
    for x in keyword_dict:
        tempDict[x['keyword']] = x['confidence_score']
    selectedWords = dict(sorted(tempDict.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10])
    print "IN RET KEYWORDS"
    return random.sample(selectedWords.keys(),3)
