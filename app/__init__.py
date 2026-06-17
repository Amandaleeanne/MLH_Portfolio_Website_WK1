import os
import markdown
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request
from dotenv import load_dotenv

from app.portfolio_data import ABOUT_TEXT, EDUCATION, HOBBIES, WORK_EXPERIENCES, PLACES, SKILLS, PERSONAL_PROJECTS

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
    # render about.md to HTML for the landing page
    about_path = os.path.join(app.root_path, 'Markdown', 'about.md')
    about_html = ABOUT_TEXT
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


@app.route('/experience')
def work():
    return render_template(
        'work.html',
        title="Experience",
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
    )
