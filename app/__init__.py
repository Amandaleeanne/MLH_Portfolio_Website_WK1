import os
from flask import Flask, render_template
from dotenv import load_dotenv

from app.portfolio_data import ABOUT_TEXT, EDUCATION, HOBBIES, WORK_EXPERIENCES

load_dotenv()
app = Flask(__name__)

# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
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
