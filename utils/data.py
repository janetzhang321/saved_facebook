import pymongo
from pymongo import MongoClient
client = MongoClient()


connection = MongoClient("127.0.0.1")

db = connection['test_database']

post = {}

def save_article(link):
    post['link'] = link

save_article('facebook.com')

db.test_collection.insert(post)
cursor = db.test_collection.find({})
