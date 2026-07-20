import datetime
import os
import re

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

from app.portfolio_data import ABOUT_TEXT, EDUCATION, HOBBIES, WORK_EXPERIENCES

# A "does this look like an email" shape: something, an @, something,
# a dot, something. It won't catch every fake address, but it stops the
# obviously wrong ones from ever reaching the database.
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

load_dotenv()
app = Flask(__name__)

# Tests flip TESTING=true so they get a throwaway in-memory database instead
# of talking to the real MySQL server — nothing written during a test run
# can ever leak into (or depend on) production data.
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
        {"label": "Timeline", "endpoint": "timeline"},
    ],
    url=os.getenv("URL") # reads from .env — will be localhost:5000 locally,
                         # real domain in production when MLH deploys in future weeks
    )


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        about_text=ABOUT_TEXT,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
    )


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)


@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map")


@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template(
        'timeline.html',
        title="Timeline",
        timeline_posts=[model_to_dict(post) for post in posts],
    )


@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    # .get(..., '') instead of ['...'] so a missing field gives us an empty
    # string to reject below, rather than crashing the whole request.
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return 'Invalid name', 400
    if not EMAIL_PATTERN.match(email):
        return 'Invalid email', 400
    if not content:
        return 'Invalid content', 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return {"message": "Timeline post deleted successfully."}, 200
    except TimelinePost.DoesNotExist:
        return {"error": "Timeline post not found."}, 404
