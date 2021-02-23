import praw
from praw.models import MoreComments
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
from Social_Scraper.Web_Server.Reddit.Reddit_Post import *
from Social_Scraper.Web_Server.Reddit.Reddit_Conn import Reddit_Conn
from Social_Scraper.Web_Server.Network.Network import Network
from Social_Scraper.Web_Server.Network.Edge import Edge
from Social_Scraper.Web_Server.Reddit.Reddit_Comment import Reddit_Comment
from Social_Scraper.Web_Server.Reddit.Subreddit import Subreddit
#from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer

'''-----------------------------'''
'''Lets Look at unpopular things'''
'''-----------------------------'''

class PostReader:
    def __init__(self, sub_name):
        self.network = Network('Reddit_' + str(datetime.now()))
        #self.network.save_to_db()
        self.sub_name = sub_name
        #self.stop_words = set(stopwords.words("english"))
        self.sub = Subreddit(sub_name=sub_name, description=sub_name)
        self.rc = Reddit_Conn(url=self.sub.url)
        self.reddit = self.rc.connection()

        self.create_network_edge(start=self.sub, end=self.network, type=type(self.network))#, network=self.network)

        self.posts = []
        self.users = []
        self.edges = []
        '''
        conn = sqlite3.connect(f'Network_{str(datetime.now())}.db')
        c = conn.cursor()
        try:
            c.execute(fCREATE TABLE {sub_name}
             (id text, author text, score text, upvote_ratio text, title blob, selftext text, selftext_html blob, all_comments blob, num_comments real, upvotes real, downvotes real, comment_to_vote_ratio real, created_utc blob, url blob))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            conn.close()
        '''
    #def add_subreddit(self, sub_name):
        #self.reddit.multireddit('contraversial', sub_name).add(self.reddit.subreddit(sub_name))

    def set_topic_list(self, topic_list):
        self.topic_list = topic_list

    def collect_posts(self, count, comment_limit, threshold):
        subreddit = self.reddit.subreddit(self.sub_name)
        sub_name = self.sub_name
        self.comment_limit = comment_limit

        for submission in subreddit.top(limit=count):
            sub = self.sub
            post = None
            author = self.reddit.redditor(str(submission.author))

            #Save Post Data
            #reddit_submission = db.reddit_submission
            #reddit_submission.insert({'submission_contents': str(submission.selftext_html)})

            if author is None: continue

            #Save Author Data
            #reddit_author = db.reddit_author
            #reddit_author.insert({'author_details': str(author)})

            user = Reddit_User(f'https://www.reddit.com/u/{submission.author.name}' ,submission.author, (author.link_karma,author.comment_karma))

            if sub_name.upper() == 'JOKES':
                post = JokePost(sub_name, threshold)
            else:
                post = Post(sub_name)

            post.set_attributes(id=submission.id, author=submission.author, score=submission.score, upvote_ratio=submission.upvote_ratio, title=submission.title, selftext=submission.selftext, selftext_html=submission.selftext_html, all_comments=submission.comments.list(), created_utc=submission.created_utc, edited=submission.edited, url=submission.url)
            post.set_topic(self.topic_list)
            #post.save_db(self.sub_name)
            #self.posts.append(post)
            #self.users.append(user)

            '''
            FIXME HERE: DRAW OUT NEWORK TO SET FOREIGN KEYS

            set parent node when creating edge:: parent is the end's mongo_id
            '''

            self.create_network_edge(start=post,end=self.sub,type=type(sub))#,network=self.network)


            '''
            FIXME HERE
            '''
            self.create_network_edge(start=user, end=post, type=type(post))#, network=sub)

            #add comment to graph



            for i, comment in enumerate(submission.comments.list()[:self.comment_limit]):
                #MoreComments
                if not isinstance(comment, MoreComments):

                    comm = self.reddit.comment(comment)
                    comm_args = {}
                    comm_args['id'] = comm.id
                    comm_args['body'] = comm.body
                    comm_args['score'] = comm.score
                    comm_args['parent_id'] = comm.submission.id
                    author = comm.author

                    reddit_comment = db.reddit_comment
                    reddit_comment.insert({
                        'comment_author' : str(author)  ,
                        'comment_details': str(comm_args)
                    })


            """    try:
                    link_karma = getattr(author, 'link_karma')
                    comment_karma = getattr(author, 'comment_karma')
                    ru = Reddit_User(author, (link_karma,comment_karma))
                except Exception as e:
                    link_karma = 0
                    comment_karma = 0
                    continue"""


                    #redd_comm = Reddit_Comment(id=comm.id, author=ru, text=comm.body, score=comm.score ,parent_id=comm.submission.id)

                    #print(i, comm.author, comm.body)
                #com = Comment()
                    #self.create_network_edge(start=ru,end=redd_comm,type=type(redd_comm), network_name=comm.submission.id)

            post.self_print(contraversial=True, hide=['all_comments','selftext_html','punchline_ext'])
            #self.network.show_graph()
            #print(post)
        return f'returning from {self}'

    def create_network_edge(self, start, end, type):#, network):
        if str(type) == "<class 'Reddit_Comment.Reddit_Comment'>":
            weight = end.score
        elif str(type) == "<class 'Reddit_Post.JokePost'>":
            weight = end.attr['score']
        else:
            weight = -1
        edge = Edge(sender=start,receiver=end,weight=weight,type=type)#, network=network)
        self.network.add_edge(edge)

if __name__ == '__main__':
    pr = PostReader()
    #pr.add_subreddit(sub_name='Jokes')
    pr.set_topic_list(['trump', 'republican', 'republicans', 'biden', 'democrat', 'democrats'])
    '''
    I Found that it took roughly a 70% upvote rate to enter the top 1000 posts -> usually more contraversial posts.
    There was one with a value as low as 0.63 -> I believe it was political.

    If we find that there are only contraversial political posts in one direction (i.e. left -> right or right -> left)
    We can assume that the platform has some bias if contraversial posts from both sides aren't present relatively similairly.
    '''
    pr.collect_posts(sub_name='Jokes', count=1000, threshold=0.8)
