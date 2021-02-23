from flask import render_template, url_for, flash, redirect, request
from Social_Scraper import app, r, q
from Social_Scraper.Web_Server.tasks import Tasker
from Social_Scraper.Web_Server.forms import SubredditSearchForm
#from Social_Scraper.Web_Server.DBModels_Reddit import DBSubreddit, DBRedditPost, DBNode
from Social_Scraper.Web_Server.Reddit.Reddit_Conn import Reddit_Conn
from rq import get_current_job
from datetime import datetime


@app.route("/")
def home():
    jobs = q.jobs
    active_job = get_current_job()
    #reddit_connections =
    return render_template('index.html', title='Home', jobs=jobs, active_job=active_job)#, reddit_connections=reddit_connections)

@app.route("/delete_job", methods=['GET', 'POST'])
def delete_job():
    if request.args.get('id'):
        job_id = request.args.get('id')
        job = q.fetch_job(str(job_id))
        active_job = get_current_job()
        q.remove(job)
    jobs = q.jobs
    return render_template('index.html', title='Home', jobs=jobs, active_job=active_job)

@app.route("/delete_queue")
def delete_queue():
    q.delete(delete_jobs=True)
    jobs = q.jobs
    active_job = get_current_job()
    return render_template('index.html', title='Home', jobs=jobs, active_job=active_job)

@app.route("/draw_network")
def draw_network():
    tasker = Tasker('draw_network', {'top_node': 'Reddit_2020-11-24 20:03:52.288418'})
    #formatted_stmt = []
    #stmt = tasker.response
    #for s in stmt:
        #formatted_stmt.append(str(s))
    flash(f'{tasker.response}', 'success')
    return render_template('show_network.html', title='Show Network')#, stmt=formatted_stmt)

@app.route("/show_network")
def show_network():
    return render_template('show_network.html', title='Show Network', stmt='')

@app.route('/task')
def add_task():
    if request.args.get('func_name'):
        func_name = request.args.get('func_name') #FIXME
        rtrn_val = Tasker(func_name, '')
        return rtrn_val.response
    return 'error'

@app.route('/reddit_search', methods=['GET', 'POST'])
def reddit_search():
    form = SubredditSearchForm()
    tasker = None
    if form.validate_on_submit():
        if str(form.save_to_db.data) != 'NO':
            args = {'subreddit_name': form.subreddit.data, 'number_of_posts': form.number_of_posts.data, 'comment_limit': form.comments_per_post.data}
            tasker = Tasker('postreader', args)
            jobs = q.jobs
            active_job = get_current_job()
            flash(f'{tasker.response}', 'success')
        else:
            flash(f'searching r/{form.subreddit.data}...(not saving)', 'success')

        return render_template('index.html', title='Home', jobs=jobs, active_job=active_job)
    return render_template('reddit_search.html', title='Reddit Search', form=form)
