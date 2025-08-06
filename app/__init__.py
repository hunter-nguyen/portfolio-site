import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
import re
import hashlib
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',
                         uri=True)
else:
    mydb=MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects", url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    
    # Validate name
    name = request.form.get('name', '').strip()
    if not name:
        return "Invalid name", 400
    
    # Validate email
    email = request.form.get('email', '').strip()
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(email_regex, email):
        return "Invalid email", 400
    
    # Validate content
    content = request.form.get('content', '').strip()
    if not content:
        return "Invalid content", 400
    
    new_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(new_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    timeline_posts = []
    for post in TimelinePost.select().order_by(TimelinePost.created_at.desc()):
        post_dict = model_to_dict(post)
        email_hash = hashlib.md5(post.email.strip().lower().encode('utf-8')).hexdigest()
        post_dict['gravatar'] = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
        timeline_posts.append(post_dict)

    return {"timeline_posts": timeline_posts}

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    TimelinePost.delete().where(TimelinePost.id == request.form['id']).execute()
    return {}