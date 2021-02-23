from Social_Scraper.Web_Server.Network.Node import Node
from Social_Scraper import db

class Reddit_Comment(Node):
    def __init__(self, id, author, text, score, parent_id,*args):
        super().__init__(identifier=parent_id, description=(author,text), type=type(self))
        self.id = id
        self.author = author
        self.text = text
        self.score = score
        self.parent_id = parent_id
        self.args = args

        self.save_db()

    def save_db(self):
        reddit_comment = db.reddit_comment
        reddit_comment.insert({'comment_details': str(self)})

    def __str__(self):
        attr = {}
        attr['id'] = self.id
        attr['author'] = self.author
        attr['text'] = self.text
        attr['score'] = self.score
        attr['parent_id'] = self.parent_id
        attr['args'] = self.args
        return attr
