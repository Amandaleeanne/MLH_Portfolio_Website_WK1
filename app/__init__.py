import os
from flask import Flask, render_template
from dotenv import load_dotenv

from app.portfolio_data import ABOUT_TEXT, CONTACT, EDUCATION, HOBBIES, WORK_EXPERIENCES

load_dotenv()
app = Flask(__name__)

# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
    ])

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Maninder (Kaurman) Kaur",
        url=os.getenv("URL"),
        about_text=ABOUT_TEXT,
        contact=CONTACT,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
    )

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map")
