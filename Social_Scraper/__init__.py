from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
import redis
from rq import Queue
import time
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo()
app.app_context().push()
#pp.config.from_object('social_scraper.settings')
app.config['MONGO_URI'] = 'mongodb+srv://admin:WJtSkMFcbXsRg2F@cluster0.fszpg.mongodb.net/Cluser0?retryWrites=true&w=majority'
mongo.init_app(app)
app.config['SECRET_KEY'] = '46199a8a2ffb4be7eeab69688c3b8a79'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True
r = redis.Redis()
q = Queue(connection=r)

db = mongo.db
#client = pymongo.MongoClient("mongodb+srv://admin:<password>@cluster0.fszpg.mongodb.net/<dbname>?retryWrites=true&w=majority")
#db = client.test
#test = mongo.

#db = SQLAlchemy(app)

from Social_Scraper import routes
