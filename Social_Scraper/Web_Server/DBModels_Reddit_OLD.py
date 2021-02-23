from datetime import datetime
#from Social_Scraper import db

class DBSubreddit(db.Model):
    __tablename__ = 'subreddits'

    id = db.Column(db.Integer, primary_key=True)
    subreddit_name = db.Column(db.String(100), nullable=False)
    number_of_posts = db.Column(db.String(100), nullable=False)
    comment_limit = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    posts = db.relationship('DBRedditPost', backref='subreddit')
    #posts = db.relationship('db_reddit_post.subreddit', backref='subreddit', lazy='True')

    def __repr__(self):
        return f'Subreddit: {self.subreddit_name} \nComment Per Post Limit: {self.comment_limit}'

class DBRedditPost(db.Model):
    __tablename__ = 'reddit_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    #subreddit = db.Column(db.Integer, db.ForeignKey('db_subreddit.id'), nullable=False)

    subreddit_id = db.Column(db.BigInteger, db.ForeignKey('subreddits.id'))
    #subreddit = db.relationship('DBSubreddit', backref='subreddit_posts', foreign_keys=[subreddit_id])

    def __repr__(self):
        return f'Title: {self.title} \nContent: {self.content}'


class DBNode(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    #children = db.relationship('DBNode', backref=db.backref('node'))

    def __repr__(self):
        parent_id = self.parent_id
        ret_val =  f'( Description: {self.identifier} // {self.description} --->> Parent: {DBNode.query.filter_by(id=parent_id).first()} )'
        db.session.flush()
        return ret_val
    #parent = db.relationship('DBNode', backref='node')
