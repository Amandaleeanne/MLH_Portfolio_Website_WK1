import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# context_processor injects variables into EVERY template automatically.
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        # "index" matches the function name below: def index()
        # If we add blueprints later, this becomes "main.index" (blueprint_name.function_name)
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
    ])

# @app.route() maps a URL path to a Python function — equivalent to app.get() in Express.
# The function name becomes the "endpoint" name used in url_for() and context_processor above.
@app.route('/')
def index():
    # render_template() finds the file in templates/, runs Jinja substitution,
    # returns HTML. Keyword args become variables available in the template.
    # os.getenv("URL") reads from .env via python-dotenv
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies")

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map")