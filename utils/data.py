import pymongo
from pymongo import MongoClient
client = MongoClient()


connection = MongoClient("127.0.0.1")

db = connection['test_database']

def save_article(link, msg, keywords, source):
    post = {'link': link, 'msg': msg, 'keywords': keywords, 'source': source}
    db.test_collection.insert(post)

#i = 0 = default
#i = 1 = A-Z
#i = 2 = Z-A
def fetch_articles(i):
    articles = list(db.test_collection.find())
    if i == 0:
        return articles
    elif i == 1:
        return sorted(articles, key=lambda k: k['source'])
    else:
        return sorted(articles, key=lambda k: k['source'], reverse=True) 


def fetch_article(ID):
    article = list(db.test_collection.find({"link": ID}))
    return article
#save_article('facebook.com')

#db.test_collection.insert(post)
cursor = db.test_collection.find({})
