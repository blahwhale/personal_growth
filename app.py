from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# Data storage paths
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)

# Routes
@app.route('/')
def index():
    return render_template('index.html', now=datetime.now())

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/api/todos', methods=['GET', 'POST'])
def handle_todos():
    if request.method == 'POST':
        todos = load_data('todos.json')
        new_todo = request.json
        new_todo['id'] = str(len(todos) + 1)
        new_todo['completed'] = False
        todos[new_todo['id']] = new_todo
        save_data('todos.json', todos)
        return jsonify(new_todo)
    else:
        return jsonify(load_data('todos.json'))

@app.route('/gratitude')
def gratitude():
    return render_template('gratitude.html')

@app.route('/api/gratitude', methods=['GET', 'POST'])
def handle_gratitude():
    if request.method == 'POST':
        entries = load_data('gratitude.json')
        new_entry = request.json
        new_entry['id'] = str(len(entries) + 1)
        new_entry['date'] = datetime.now().isoformat()
        entries[new_entry['id']] = new_entry
        save_data('gratitude.json', entries)
        return jsonify(new_entry)
    else:
        return jsonify(load_data('gratitude.json'))

@app.route('/habits')
def habits():
    return render_template('habits.html')

@app.route('/api/habits', methods=['GET', 'POST', 'PUT'])
def handle_habits():
    if request.method == 'POST':
        habits = load_data('habits.json')
        new_habit = request.json
        new_habit['id'] = str(len(habits) + 1)
        new_habit['streak'] = 0
        new_habit['created_at'] = datetime.now().isoformat()
        habits[new_habit['id']] = new_habit
        save_data('habits.json', habits)
        return jsonify(new_habit)
    elif request.method == 'PUT':
        habits = load_data('habits.json')
        habit_id = request.json['id']
        if habit_id in habits:
            habits[habit_id]['streak'] += 1
            habits[habit_id]['last_completed'] = datetime.now().isoformat()
            save_data('habits.json', habits)
            return jsonify(habits[habit_id])
    return jsonify(load_data('habits.json'))

@app.route('/weekly')
def weekly():
    return render_template('weekly.html')

@app.route('/api/weekly', methods=['GET', 'POST'])
def handle_weekly():
    if request.method == 'POST':
        reviews = load_data('weekly_reviews.json')
        new_review = request.json
        new_review['id'] = str(len(reviews) + 1)
        new_review['date'] = datetime.now().isoformat()
        reviews[new_review['id']] = new_review
        save_data('weekly_reviews.json', reviews)
        return jsonify(new_review)
    else:
        return jsonify(load_data('weekly_reviews.json'))

@app.route('/takeaways')
def takeaways():
    return render_template('takeaways.html')

@app.route('/api/takeaways', methods=['GET', 'POST'])
def handle_takeaways():
    if request.method == 'POST':
        takeaways = load_data('takeaways.json')
        new_takeaway = request.json
        new_takeaway['id'] = str(len(takeaways) + 1)
        new_takeaway['date'] = datetime.now().isoformat()
        takeaways[new_takeaway['id']] = new_takeaway
        save_data('takeaways.json', takeaways)
        return jsonify(new_takeaway)
    else:
        return jsonify(load_data('takeaways.json'))

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/api/goals', methods=['GET', 'POST', 'PUT'])
def handle_goals():
    if request.method == 'POST':
        goals = load_data('goals.json')
        new_goal = request.json
        new_goal['id'] = str(len(goals) + 1)
        new_goal['created_at'] = datetime.now().isoformat()
        new_goal['status'] = 'in_progress'
        goals[new_goal['id']] = new_goal
        save_data('goals.json', goals)
        return jsonify(new_goal)
    elif request.method == 'PUT':
        goals = load_data('goals.json')
        goal_id = request.json['id']
        if goal_id in goals:
            goals[goal_id]['status'] = request.json['status']
            goals[goal_id]['updated_at'] = datetime.now().isoformat()
            save_data('goals.json', goals)
            return jsonify(goals[goal_id])
    return jsonify(load_data('goals.json'))

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/api/history', methods=['GET'])
def handle_history():
    # Combine all data for history view
    history = {
        'todos': load_data('todos.json'),
        'gratitude': load_data('gratitude.json'),
        'habits': load_data('habits.json'),
        'weekly_reviews': load_data('weekly_reviews.json'),
        'takeaways': load_data('takeaways.json'),
        'goals': load_data('goals.json')
    }
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 