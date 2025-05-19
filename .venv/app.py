from flask import Flask, render_template, request, redirect, session
import json, random

app = Flask(__name__)
app.secret_key = "your-secret"

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/set-name', methods=['POST'])
def set_name():
    session['name'] = request.form['name']
    return redirect('/home')

@app.route('/home')
def home():
    name = session.get('name', 'Friend')
    affirmation = get_daily_affirmation()
    accomplishments = load_json('data/accomplishments.json')
    return render_template("home.html", name=name, affirmation=affirmation, accomplishments=accomplishments)

@app.route('/add-accomplishment', methods=['POST'])
def add_accomplishment():
    new_item = request.form['accomplishment']
    append_json('data/accomplishments.json', new_item)
    return redirect('/home')

@app.route('/forum')
def forum():
    posts = load_json('data/forum.json')
    return render_template("forum.html", posts=posts)

@app.route('/add-forum-post', methods=['POST'])
def add_forum_post():
    post = {"name": request.form['name'], "message": request.form['message']}
    append_json('data/forum.json', post)
    return redirect('/forum')

@app.route('/resources')
def resources():
    return render_template("resources.html")

# Helper functions
def get_daily_affirmation():
    with open('data/affirmations.json') as f:
        affirmations = json.load(f)
    return random.choice(affirmations)

def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)

def append_json(filepath, item):
    data = load_json(filepath)
    data.append(item)
    with open(filepath, 'w') as f:
        json.dump(data, f)
