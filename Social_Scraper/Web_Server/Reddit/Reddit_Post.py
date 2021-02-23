import praw
import pprint
from datetime import datetime
import re
import string
import sqlite3
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
import numpy as np
from nltk import Tree
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from Social_Scraper import db
from Social_Scraper.Web_Server.Reddit.Sentence import Sentence, Token
from Social_Scraper.Web_Server.Network.Node import Node
from Social_Scraper.Web_Server.Reddit.Reddit_User import Reddit_User

class Post(Node):
    def __init__(self, sub_name):
        self.attr = {}
        self.attr['sub_name'] = sub_name
    def set_attributes(self, id, author, score, upvote_ratio, title, selftext, selftext_html, all_comments, created_utc, edited, url):
        self.attr['id'] = id
        self.attr['author'] = author
        self.attr['score'] = score
        self.attr['upvote_ratio'] = upvote_ratio
        self.attr['title'] = title
        super().__init__(identifier=self.attr['id'], description=self.attr['title'][:79], type=str(type(self)))
        self.attr['selftext'] = selftext
        self.attr['selftext_html'] = selftext_html
        self.attr['all_comments'] = all_comments
        self.attr['num_comments'] = len(all_comments)
        self.attr['upvotes'] = self.attr['score']/ float(self.attr['upvote_ratio'])
        self.attr['downvotes'] = self.attr['upvotes'] - self.attr['score']
        self.attr['comment_to_vote_ratio'] = self.attr['num_comments'] / (self.attr['upvotes'] + self.attr['downvotes'])
        self.attr['created_utc'] = created_utc
        self.attr['url'] = url
        self.attr['edited'] = edited
        self.derive_attributes()
        return
    def derive_attributes(self):
        self.save_db()

    def set_topic(self, topics):
        self.attr['topic'] = []
        text = self.attr['title'].lower() + self.attr['selftext'].lower() #get rid of punctuation
        text = [Sentence(s) for s in sent_tokenize(text)]
        for itm in text:
            if itm.text in topics:
                self.attr['topic'].append(itm)

    def self_print(self, contraversial ,hide):
        print('Post Retrieved: ' + str(datetime.now()))
        for k,v in self.attr.items():
            if k not in hide:
                if contraversial:
                    if self.attr['contraversial']: print(f'{k}: {v}')
                else:
                    print(f'{k}: {v}')
        print('\n\n')

    def save_db(self):
        reddit_submission = db.reddit_submission
        reddit_submission.insert({'submission_contents': str(self.attr)})

        #conn = sqlite3.connect(f'{sub_name}.db')
        #c = conn.cursor()
        #print(f"INSERT INTO {sub_name} VALUES ({self.attr['id']}, {self.attr['author']}, {self.attr['score']}, {self.attr['upvote_ratio']}, {self.attr['title']}, {self.attr['selftext']}, {self.attr['selftext_html']}, {self.attr['all_comments']}, {self.attr['num_comments']},{self.attr['upvotes']}, {self.attr['downvotes']}, {self.attr['comment_to_vote_ratio']}, {self.attr['created_utc']}, {self.attr['url']})")
        #c.execute(f"INSERT INTO {sub_name} VALUES ({self.attr['id']}, {self.attr['author']}, {self.attr['score']}, {self.attr['upvote_ratio']}, '{self.attr['title']}', {self.attr['selftext']}, {self.attr['selftext_html']}, {self.attr['all_comments']}, {self.attr['num_comments']},{self.attr['upvotes']}, {self.attr['downvotes']}, {self.attr['comment_to_vote_ratio']}, {self.attr['created_utc']}, {self.attr['url']})")
        #conn.close()

        #self.tokens += ['\\n']

class Joke:
    def __init__(self, setup, punchline):
        self.setup =  [Sentence(s) for s in sent_tokenize(setup)]
        self.punchline =  [Sentence(s) for s in sent_tokenize(punchline)]
        #self.ps = PorterStemmer()
        self.suprise = self.interpret_suprise()


    def interpret_suprise(self):
        setup_words = [token for s in self.setup for token in s.tokens if token.text not in string.punctuation]
        punchline_words = [token for s in self.punchline for token in s.tokens if token.text not in string.punctuation]
        print(setup_words)

    def __repr__(self):
        setup = ''
        punchline = ''
        for s in self.setup:
            setup += str(s)
        for p in self.punchline:
            punchline += str(p)

        return f'\n\nSetup: \n\n {setup} \n\n----------------\n\nPunchline: \n\n {punchline} \n\n=========================================='

class JokePost(Post):
    def __init__(self, sub_name, threshold):
        super().__init__(sub_name)
        self.threshold = threshold


    def derive_attributes(self):
        self.attr['setup'] = self.attr['title']
        self.attr['punchline'] = self.attr['selftext']
        self.joke = Joke(self.attr['setup'], self.attr['punchline'])
        self.attr['punchline_ext'] = self.attr['selftext_html']
        if self.attr['upvote_ratio'] > self.threshold :
            self.attr['contraversial'] = False
        else:
            self.attr['contraversial'] = True
        self.save_db()
        return


    def __repr__(self):
        return str(self.joke)
