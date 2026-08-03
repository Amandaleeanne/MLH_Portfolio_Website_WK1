# Production Engineering -- Portfolio Site

Welcome to the MLH Fellowship! During Week 1, you'll be using Flask to build a portfolio site. This site will be the foundation for activities we do in future weeks so spend time this week making it your own and reflect your personality!!

Coming from week 7: This project now supports docker!

## Installation

Make sure you have python3 and pip installed

Create and activate virtual environment using virtualenv
```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies!

```bash
pip install -r requirements.txt
```

Alternatively, install and use docker build or the redeploy-site.sh to run the application.

## Usage

Create a .env file using the example.env template (make a copy using the variables inside of the template)

Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```

You should get a response like this in the terminal:
```
❯ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 

*Note: The portfolio site will only work on your local machine while you have it running inside of your terminal. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

Universal tasks are tasks that will be merged into the main branch for all other branches to update from. Portfolio tasks are custom tasks that should live in a separate branch. Each person within the group will have their own branch that contains things specific to them and their portfolio. Pull requests are still required for review and feedback.

Please make sure to update tests as appropriate.
