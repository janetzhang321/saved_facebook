import pymongo
from pymongo import MongoClient
client = MongoClient()


connection = MongoClient("127.0.0.1")

db = connection['test_database']

def save_article(link, msg, keywords, source):
    post = {'link': link, 'msg': msg, 'keywords': keywords, 'source': source}
    db.test_collection.insert(post)

def fetch_articles():
    articles = list(db.test_collection.find())
    return articles

def fetch_article(ID):
    article = list(db.test_collection.find({"link": ID}))
    return article
#save_article('facebook.com')

#db.test_collection.insert(post)
cursor = db.test_collection.find({})
