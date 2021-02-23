from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SubredditSearchForm(FlaskForm):
    subreddit = StringField('subreddit', validators=[DataRequired()])
    number_of_posts = StringField('number_of_posts', validators=[DataRequired()])
    comments_per_post = StringField('comments_per_post', validators=[DataRequired()])
    save_to_db = StringField('save_to_db', validators=[DataRequired()])
    submit = SubmitField('Go')
