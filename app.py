from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Initialize karne ka function
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Table banayein agar pehle se mavjood na ho
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Database setup run karein
init_db()

# 1. Main HTML Page load karne ke liye Route
@app.route('/')
def home():
    return render_template('index.html')

# 2. Database se saare tasks mangwane ki API (GET)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall() # [(1, 'Task 1'), (2, 'Task 2')]
    conn.close()
    
    # List of dictionaries mein convert kar rahe hain API response ke liye
    task_list = [{'id': row[0], 'title': row[1]} for row in tasks]
    return jsonify(task_list)

# 3. Naya task database mein add karne ki API (POST)
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    
    if title:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Task added successfully!'}), 201
    
    return jsonify({'error': 'Title is required'}), 400

app.run(debug=True)