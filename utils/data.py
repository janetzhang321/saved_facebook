import pymongo
from pymongo import MongoClient
client = MongoClient()


connection = MongoClient("127.0.0.1")

db = connection['test_database']


def save_article(link,source, msg):
    post = {'link': link, 'name': source, 'msg': msg}
    db.test_collection.insert(post)

def fetch_articles():
    articles = list(db.test_collection.find())
    return articles
#save_article('facebook.com')

#db.test_collection.insert(post)
cursor = db.test_collection.find({})
