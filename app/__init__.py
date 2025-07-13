from flask import Flask, request
from peewee import *
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# MySQL Database Connection
db = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

# Define the TimelinePost model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Create the Flask app
def create_app():
    app = Flask(__name__)

    # Connect and create the timeline_post table
    db.connect()
    db.create_tables([TimelinePost])

    @app.route("/api/timeline_post", methods=["POST"])
    def post_timeline_post():
        name = request.form["name"]
        email = request.form["email"]
        content = request.form["content"]
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)

    @app.route("/api/timeline_post", methods=["GET"])
    def get_timeline_post():
        timeline_posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        return {"timeline_posts": [model_to_dict(post) for post in timeline_posts]}

    return app

app = create_app()
