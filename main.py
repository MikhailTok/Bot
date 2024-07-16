from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import redirect
import sqlite3

# # importing other libraries
# import requests
# from PIL import Image

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


from openai import OpenAI

client = OpenAI(
    api_key=os.environ['API_KEY'],
    base_url=os.environ['BASE_URL'],
)





def create_database():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY,
              ip TEXT,
              question TEXT NOT NULL,
              answer TEXT,
              date datetime default current_timestamp)''')

@app.route('/admin')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('admin.html', tasks=tasks)

# @app.route('/add', methods=['POST'])
# def add_task():
#     task = request.form['task']
#     conn = sqlite3.connect('todo.db')
#     c = conn.cursor()
#     c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('quryies'))

@app.route("/")
def home():

    user_ip = request.remote_addr

    user_id = request.cookies.get('user_id')
    # if 'username' in session:
    #     print(request.remote_addr)
    # else:
    #     session['username'] = request.remote_addr


    return render_template('base.html')


@app.route('/question', methods=['POST'])
def question():

    data = request.json['question']

    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": data}]
    )

    answer = chat_completion.choices[0].message.content

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (ip, question, answer) VALUES (?, ?, ?)",  (request.remote_addr, data, answer))
    conn.commit()
    conn.close()


    print(request.remote_addr, data, answer)

    return {'answer': answer}

    return {'answer': 'Answer from BOT'}

if __name__ == '__main__':
    create_database()
    port = 60
    app.run(host='0.0.0.0', port=port, debug=True)




