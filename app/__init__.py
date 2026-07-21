import os
import re
import markdown
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime


load_dotenv()
app = Flask(__name__)

from app.portfolio_data import EDUCATION, HOBBIES, WORK_EXPERIENCES, PLACES, SKILLS, PERSONAL_PROJECTS

# A "does this look like an email" shape: something, an @, something,
# a dot, something. It won't catch every fake address, but it stops the
# obviously wrong ones from ever reaching the database.
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

#db
# Tests flip TESTING=true so they get a throwaway in-memory database instead
# of talking to the real MySQL server — nothing written during a test run
# can ever leak into (or depend on) production data.
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)
#debug
print(mydb)
# --- Classes --- 
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])
# ------------------ Routes ------------------

# ---- Timeline API Routes ----
@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
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
    return{
        
        "timeline_posts": [
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
    
# --- General Routes --- 
# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        # "index" matches the function name below: def index()
        # If we add blueprints later, this becomes "main.index" (blueprint_name.function_name)
        {"label": "Experience", "endpoint": "work"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
        {"label": "Timeline", "endpoint": "timeline"},
        {"label": "Dev-Blog", "endpoint": "blog"},
        ],
        url=os.getenv("URL") # reads from .env — will be localhost:5000 locally,
                         # real domain in production when MLH deploys in future weeks
    )

@app.route('/')
def index():
    # render about.md to HTML for the landing page
    about_path = os.path.join(app.root_path, 'Markdown', 'about.md')
    if os.path.exists(about_path):
        with open(about_path, encoding='utf-8') as f:
            about_md = f.read()
        about_html = markdown.markdown(about_md, extensions=['extra', 'sane_lists'])

    return render_template(
        'index.html',
        title="Amandaleeanne Schock",
        url=os.getenv("URL"),
        about_html=about_html,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        skills=SKILLS,
        personal_projects=PERSONAL_PROJECTS,
    )

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)

# A bit complex, but uses plotly to take data and plot markers on the map. Thanks Gemini.
@app.route('/travel')
def travel():
    df = pd.DataFrame(PLACES)
    # Include Alaska and the full United States area, while excluding overseas points.
    df = df[df['lon'].between(-170, -50) & df['lat'].between(18, 72)]
    df['text'] = df['name']
    fig = px.scatter_geo(
        df,
        lon='lon',
        lat='lat',
        scope='usa',
        text='text',
        hover_data={'note': True, 'lon': False, 'lat': False, 'text': False},
        size_max=12,
        projection='albers usa',
    )
    fig.update_traces(
        marker=dict(size=10, color='#d1495b', line=dict(width=1, color='white')),
        textposition='top center',
        textfont=dict(color='#0f2c4f', size=11),
        hovertemplate='<b>%{text}</b><br>%{customdata[0]}<extra></extra>',
        customdata=df[['note']].values,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='white'),
        hoverlabel=dict(bgcolor='white', bordercolor='#d1495b', font_size=12, font_family='Roboto'),
    )
    plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return render_template('travel.html', title="Travel Map", plot_html=plot_html)

@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", timeline_posts=[model_to_dict(post) for post in posts])

@app.route('/blog')
def blog():
    return render_template('blog.html', title="Dev-Blog")

@app.route('/experience')
def work():
    return render_template(
        'work.html',
        title="Experience",
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
    )
