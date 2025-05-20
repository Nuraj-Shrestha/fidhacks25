from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import random
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key')  # Use environment variable with fallback

# Configure OpenAI
client = OpenAI(api_key=os.getenv('_API_KEY'))

# === Landing Page ===
@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/set-name', methods=['POST'])
def set_name():
    session['name'] = request.form['name']
    return redirect('/goalsetting')

@app.route('/goalsetting')
def goalsetting():
    name = session.get('name', 'Friend')
    return render_template('goals.html', name=name)

@app.route('/save-goals', methods=['POST'])
def save_goals():
    name = request.form['name']
    goals = {
        "goal1": request.form['goal1'],
        "goal2": request.form['goal2'],
        "goal3": request.form['goal3']
    }

    data = load_json('data/goals.json')
    data[name] = goals

    with open('data/goals.json', 'w') as f:
        json.dump(data, f)

    session['name'] = name
    return redirect('/main')

@app.route('/main')
def main():
    name = session.get('name', None)
    if not name:
        return redirect('/')

    goals = load_json('data/goals.json').get(name, {})
    return render_template('main.html', name=name, goals=goals)

# === Forum Page ===
@app.route('/forum')
def forum():
    posts = load_json('data/forum.json')
    return render_template("forum.html", posts=posts)

@app.route('/add-forum-post', methods=['POST'])
def add_forum_post():
    post = {"name": request.form['name'], "message": request.form['message']}
    append_json('data/forum.json', post)
    return redirect('/forum')

# === Resources Page ===
@app.route('/resources')
def resources():
    return render_template("resources.html")

@app.route('/get-resources')
def get_resources():
    with open('data/resources.json') as f:
        return jsonify(json.load(f))

@app.route('/get-goal-steps', methods=['POST'])
def get_goal_steps():
    try:
        goal = request.json.get('goal', '')
        name = session.get('name', 'Friend')
        
        # Create a prompt for ChatGPT
        prompt = f"""As a supportive mentor, provide 5 specific, actionable steps to help {name} achieve their goal: {goal}
        Return ONLY a JSON array of 5 strings, each string being one step.
        Make the steps specific, measurable, and achievable.
        Example format: [\"Step 1\", \"Step 2\", \"Step 3\", \"Step 4\", \"Step 5\"]
        Do not include any other text in your response."""
        
        # Make the API call to ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive mentor providing actionable steps for goal achievement. Always respond with a valid JSON array of exactly 5 strings."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # Get the response content
        steps_text = response.choices[0].message.content.strip()
        
        # Ensure the response is a valid JSON array
        try:
            steps = json.loads(steps_text)
            if not isinstance(steps, list) or len(steps) != 5:
                raise Exception('Invalid steps')
        except Exception:
            # More creative fallback steps
            step_templates = [
                f"Write down why '{goal}' matters to you and how it will impact your life.",
                f"Find and connect with someone who has already achieved '{goal}' for advice.",
                f"Break '{goal}' into 3-5 mini-goals and set a reward for each.",
                f"Schedule time on your calendar this week to work on '{goal}'.",
                f"List the resources or skills you need to accomplish '{goal}'.",
                f"Share your goal '{goal}' with a friend or family member for accountability.",
                f"Visualize yourself achieving '{goal}' every morning for motivation.",
                f"Identify one obstacle to '{goal}' and brainstorm how to overcome it.",
                f"Track your progress towards '{goal}' in a journal or app.",
                f"Celebrate each small win as you move closer to '{goal}'.",
                f"Research a new strategy or technique to help with '{goal}'.",
                f"Create a vision board or digital collage for '{goal}'.",
                f"Commit to a daily habit that supports '{goal}'.",
                f"Reflect weekly on what's working and what you can improve for '{goal}'.",
                f"Set a specific deadline for achieving '{goal}' and mark it on your calendar."
            ]
            steps = random.sample(step_templates, 5)
        
        return jsonify({
            'steps': steps
        })
    except Exception as e:
        print(f"Error in get-goal-steps: {str(e)}")  # Add logging
        # Fallback in case of total failure
        fallback_templates = [
            f"Write down why '{goal}' matters to you and how it will impact your life.",
            f"Find and connect with someone who has already achieved '{goal}' for advice.",
            f"Break '{goal}' into 3-5 mini-goals and set a reward for each.",
            f"Schedule time on your calendar this week to work on '{goal}'.",
            f"List the resources or skills you need to accomplish '{goal}'.",
            f"Share your goal '{goal}' with a friend or family member for accountability.",
            f"Visualize yourself achieving '{goal}' every morning for motivation.",
            f"Identify one obstacle to '{goal}' and brainstorm how to overcome it.",
            f"Track your progress towards '{goal}' in a journal or app.",
            f"Celebrate each small win as you move closer to '{goal}'.",
            f"Research a new strategy or technique to help with '{goal}'.",
            f"Create a vision board or digital collage for '{goal}'.",
            f"Commit to a daily habit that supports '{goal}'.",
            f"Reflect weekly on what's working and what you can improve for '{goal}'.",
            f"Set a specific deadline for achieving '{goal}' and mark it on your calendar."
        ]
        steps = random.sample(fallback_templates, 5)
        return jsonify({'steps': steps})

@app.route('/get-affirmation')
def get_affirmation():
    try:
        # Get user's name and goals
        name = session.get('name', '')
        goals = []
        try:
            with open('data/goals.json', 'r') as f:
                goals_data = json.load(f)
                goals = goals_data.get('goals', [])
        except:
            pass

        # Base affirmations that can be combined
        base_affirmations = [
            "I am capable of achieving anything I set my mind to",
            "Every day I grow stronger and more confident",
            "I am worthy of success and happiness",
            "I have the power to create positive change",
            "I am becoming the best version of myself",
            "I trust in my ability to overcome challenges",
            "I am surrounded by love and support",
            "I am making progress every single day",
            "I believe in my dreams and my ability to achieve them",
            "I am resilient and can handle any situation",
            "I am in charge of my own happiness",
            "I choose to be confident and self-assured",
            "I am worthy of all good things",
            "I am stronger than my challenges",
            "I am creating my own success story"
        ]

        # Select random affirmation without seeding
        affirmation = random.choice(base_affirmations)
        
        # If user has goals, incorporate them into the affirmation
        if goals:
            goal = random.choice(goals)
            goal_phrases = [
                f"as I work towards {goal}",
                f"while pursuing {goal}",
                f"on my journey to {goal}",
                f"as I strive for {goal}",
                f"in my pursuit of {goal}",
                f"as I focus on {goal}",
                f"while working on {goal}",
                f"as I progress in {goal}"
            ]
            affirmation += f" {random.choice(goal_phrases)}"

        # Add a personal touch with the user's name
        if name:
            name_phrases = [
                f", {name}",
                f", dear {name}",
                f", {name}!",
                f", {name}!",
                f", {name} - you've got this!",
                f", {name} - keep shining!"
            ]
            affirmation += random.choice(name_phrases)

        return jsonify({'affirmation': affirmation})
    except Exception as e:
        print(f"Error in get-affirmation: {str(e)}")
        return jsonify({'affirmation': "I am becoming the best version of myself."})

@app.route('/get-motivational-summary', methods=['POST'])
def get_motivational_summary():
    try:
        name = session.get('name', '')
        accomplishments = request.json.get('accomplishments', [])

        # Create a prompt for ChatGPT
        prompt = f"""Create a short, motivational summary for {name} based on their accomplishments:
        {accomplishments}
        
        The summary should:
        - Acknowledge their achievements
        - Highlight their capabilities and strengths
        - Encourage them to keep going
        - Be positive and uplifting
        - Be no more than 3-4 sentences
        - Include specific references to their accomplishments
        
        Return ONLY the summary text, nothing else."""

        # Make the API call to ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive mentor creating personalized motivational summaries based on accomplishments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({'summary': summary})
    except Exception as e:
        print(f"Error in get-motivational-summary: {str(e)}")
        return jsonify({
            'summary': f"Keep going, {name}! Every accomplishment, no matter how small, is a step forward in your journey. You're doing great!"
        })

@app.route('/add-accomplishment', methods=['POST'])
def add_accomplishment():
    try:
        name = session.get('name', '')
        accomplishment = request.form['accomplishment']
        
        # Load existing accomplishments
        try:
            with open('data/accomplishments.json', 'r') as f:
                accomplishments_data = json.load(f)
        except:
            accomplishments_data = {}
        
        # Add new accomplishment
        if name not in accomplishments_data:
            accomplishments_data[name] = []
        accomplishments_data[name].append(accomplishment)
        
        # Save updated accomplishments
        with open('data/accomplishments.json', 'w') as f:
            json.dump(accomplishments_data, f)
        
        return redirect('/main')
    except Exception as e:
        print(f"Error in add-accomplishment: {str(e)}")
        return redirect('/main')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        name = session.get('name', 'Friend')
        prompt = f"You are a supportive, motivational, and inspiring mentor named HerWayBot. Always answer in a positive, encouraging, and uplifting way. Address the user as {name}. If they ask for advice, motivation, or have any question, respond with empathy and actionable inspiration."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.8
        )
        bot_reply = response.choices[0].message.content.strip()
        return jsonify({'reply': bot_reply})
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({'reply': "I'm here for you! If you have any questions or need motivation, just ask."})

@app.route('/get-mood-affirmation', methods=['POST'])
def get_mood_affirmation():
    try:
        name = session.get('name', 'Friend')
        mood = request.json.get('mood', 'neutral')
        prompt = f"You are a supportive, motivational mentor. The user is currently feeling {mood}. Write a short, powerful affirmation or advice for {name} that is tailored to this mood. Be positive, empathetic, and uplifting."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.8
        )
        affirmation = response.choices[0].message.content.strip()
        return jsonify({'affirmation': affirmation})
    except Exception as e:
        print(f"Error in get-mood-affirmation: {str(e)}")
        return jsonify({'affirmation': "No matter how you feel right now, you are strong and capable of amazing things."})

# === Utility Functions ===
def load_json(filepath):
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def append_json(filepath, item):
    data = load_json(filepath)
    data.append(item)
    with open(filepath, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true')
