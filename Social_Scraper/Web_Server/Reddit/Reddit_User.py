from Social_Scraper.Web_Server.Network.Node import Node
from Social_Scraper.Web_Server.Reddit.Reddit_Conn import Reddit_Conn
from praw.models import Redditor
from Social_Scraper import db

class Reddit_User(Node):
    def __init__(self, url, author, bio):
        super().__init__(identifier=str(author), description=str(bio),type=str('Reddit_User'))
        self.author = str(author)
        self.bio = str(bio)
        self.url = url
        rc = Reddit_Conn(url=url)
        self.reddit = rc.connection()
        self.redditor = self.reddit.redditor(self.author)

        reddit_author = db.reddit_author
        reddit_author.insert({'author_details': str(self)})

    def __str__(self):
        attr = {}
        attr['author'] = self.author
        attr['bio'] = self.bio
        attr['url'] = self.url
        return str(attr)

        #for comment in self.redditor.comments.new(limit=10):
        #    print(comment.body.split("\n", 1)[0][:79])
