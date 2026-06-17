import os
import markdown
from flask import Flask, render_template, request
from dotenv import load_dotenv

from app.portfolio_data import *

load_dotenv()
app = Flask(__name__)

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
    ])

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Amandaleeanne Schock",
        url=os.getenv("URL"),
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        skills=SKILLS,
        personal_projects=PERSONAL_PROJECTS,
    )

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map")


@app.route('/experience')
def work():
    return render_template(
        'work.html',
        title="Experience",
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
    )
