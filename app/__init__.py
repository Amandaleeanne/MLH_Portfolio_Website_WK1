import os
from flask import Flask, render_template
from dotenv import load_dotenv

from app.portfolio_data import SOCIAL_LINKS, ABOUT_TEXT, TECH_PROJECTS, WEBSITE_URL, EDUCATION, HOBBIES_ART, HOBBIES_MUSIC, WORK_EXPERIENCES, LOCATIONS

load_dotenv()
app = Flask(__name__)
# Note: currently using flat pattern (app created at module level).
# Should refactor to application factory pattern (create_app() + config.py)
# in future weeks when we have multiple environments (dev/test/prod) and Docker.

# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
    ],
    url=os.getenv("URL") # reads from .env — will be ocalhost:5000 locally,
                         # real domain in production when MLH deploys in future weeks
    )

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Cynthia Lee Wong",
        social_links=SOCIAL_LINKS,
        about_text=ABOUT_TEXT,
        website_url=WEBSITE_URL,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        tech_projects=TECH_PROJECTS
    )

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies_art=HOBBIES_ART, hobbies_music=HOBBIES_MUSIC)

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map", locations=LOCATIONS)
